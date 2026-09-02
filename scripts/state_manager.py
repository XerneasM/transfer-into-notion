#!/usr/bin/env python3
"""Private, cross-platform state for transfer-into-notion.

State lives outside the skill checkout so a GitHub-published skill never carries
Notion IDs or note history. The script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
PROPERTY_ROLES = {"title", "author", "platform", "source_url", "content_type", "timeliness"}
VISUALIZATION_MODES = {"local_svg", "hybrid", "ask_each_time"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def state_root() -> Path:
    override = os.environ.get("TRANSFER_INTO_NOTION_STATE_DIR") or os.environ.get("VIDEO_TRANSFER_NOTION_STATE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    default = Path.home() / ".codex" / "state" / "transfer-into-notion"
    legacy = Path.home() / ".codex" / "state" / "video-transfer-notion"
    if default.exists() or not legacy.exists():
        return default
    return legacy


def profile_id(profile_key: str) -> str:
    return hashlib.sha256(profile_key.encode("utf-8")).hexdigest()[:16]


def active_path() -> Path:
    return state_root() / "active.json"


def state_path(profile_key: str) -> Path:
    return state_root() / f"profile-{profile_id(profile_key)}.json"


def backup_path(profile_key: str) -> Path:
    return state_root() / f"profile-{profile_id(profile_key)}.backup.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def atomic_write(path: Path, value: dict[str, Any], backup: Path | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup and path.exists():
        shutil.copy2(path, backup)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def set_active(profile_key: str) -> None:
    atomic_write(active_path(), {"profile_key": profile_key, "updated_at": now_iso()})


def resolve_profile_key(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    if active_path().exists():
        return str(read_json(active_path()).get("profile_key") or "") or None
    return None


def load_state(profile_key: str) -> dict[str, Any]:
    path = state_path(profile_key)
    if not path.exists():
        raise FileNotFoundError(path)
    state = read_json(path)
    errors = validate_state(state, profile_key)
    if errors:
        raise ValueError("; ".join(errors))
    return state


def validate_state(state: dict[str, Any], profile_key: str | None = None) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"unsupported schema_version={state.get('schema_version')!r}")
    if profile_key and state.get("profile_key") != profile_key:
        errors.append("profile_key mismatch")
    if not isinstance(state.get("next_sequence"), int) or state.get("next_sequence", 0) < 1:
        errors.append("next_sequence must be a positive integer")
    notion = state.get("notion")
    if not isinstance(notion, dict) or not notion.get("data_source_id"):
        errors.append("notion.data_source_id is required")
    elif not isinstance(notion.get("property_map", {}), dict):
        errors.append("notion.property_map must be an object")
    visual = state.get("visualization")
    if not isinstance(visual, dict) or not isinstance(visual.get("used_styles"), list):
        errors.append("visualization.used_styles must be a list")
    elif visual.get("mode") is not None and visual.get("mode") not in VISUALIZATION_MODES:
        errors.append("visualization.mode must be local_svg, hybrid, ask_each_time, or null")
    return errors


def parse_style(raw: str) -> dict[str, Any]:
    parts = raw.split("|")
    if len(parts) not in {5, 7}:
        raise argparse.ArgumentTypeError("style must be SEQUENCE|NAME|FAMILY|LAYOUT|PALETTE[|ERA|MOTIF]")
    try:
        sequence = int(parts[0])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("style sequence must be an integer") from exc
    style = {
        "sequence": sequence,
        "name": parts[1].strip(),
        "family": parts[2].strip(),
        "layout": parts[3].strip(),
        "palette": parts[4].strip(),
    }
    if len(parts) == 7:
        style["era"] = parts[5].strip()
        style["motif"] = parts[6].strip()
    return style


def parse_property(raw: str) -> tuple[str, str]:
    role, separator, name = raw.partition("=")
    role = role.strip()
    name = name.strip()
    if not separator or role not in PROPERTY_ROLES or not name:
        allowed = ", ".join(sorted(PROPERTY_ROLES))
        raise argparse.ArgumentTypeError(f"property must be ROLE=NAME; ROLE is one of: {allowed}")
    return role, name


def new_state(args: argparse.Namespace) -> dict[str, Any]:
    authors = sorted({item.strip() for item in (args.author or []) if item.strip()})
    styles = sorted((args.style or []), key=lambda item: item["sequence"])
    last_note = None
    if args.last_sequence:
        last_note = {
            "sequence": args.last_sequence,
            "page_id": args.last_page_id or "",
            "page_url": args.last_page_url or "",
            "source_url": args.last_source_url or "",
            "title": args.last_title or "",
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "profile_key": args.profile_key,
        "notion": {
            "database_id": args.database_id or "",
            "data_source_id": args.data_source_id,
            "database_name": args.database_name,
            "schema_checked_at": args.schema_checked_at or now_iso(),
            "known_authors": authors,
            "property_map": dict(args.property or []),
        },
        "next_sequence": args.next_sequence,
        "visualization": {"used_styles": styles, "mode": "hybrid"},
        "recent_notes": [last_note] if last_note else [],
        "last_note": last_note,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


def compact_state(state: dict[str, Any]) -> dict[str, Any]:
    notion = state["notion"]
    return {
        "initialized": True,
        "profile_key": state["profile_key"],
        "next_sequence": state["next_sequence"],
        "notion": {
            "database_id": notion.get("database_id", ""),
            "data_source_id": notion.get("data_source_id", ""),
            "database_name": notion.get("database_name", "Inspiration"),
            "schema_checked_at": notion.get("schema_checked_at", ""),
            "known_authors": notion.get("known_authors", []),
            "property_map": notion.get("property_map", {}),
        },
        "used_styles": state["visualization"].get("used_styles", []),
        "visualization_mode": state["visualization"].get("mode") or "hybrid",
        "last_note": state.get("last_note"),
        "state_path": str(state_path(state["profile_key"])),
    }


def cmd_show(args: argparse.Namespace) -> int:
    key = resolve_profile_key(args.profile_key)
    if not key:
        print(json.dumps({"initialized": False, "reason": "no active profile", "state_dir": str(state_root())}, ensure_ascii=False))
        return 0
    try:
        state = load_state(key)
    except FileNotFoundError:
        print(json.dumps({"initialized": False, "reason": "profile state missing", "profile_key": key, "state_dir": str(state_root())}, ensure_ascii=False))
        return 0
    print(json.dumps(state if args.full else compact_state(state), ensure_ascii=False, indent=2))
    return 0


def cmd_init(args: argparse.Namespace, repairing: bool = False) -> int:
    path = state_path(args.profile_key)
    if path.exists() and not (args.force or repairing):
        raise SystemExit("State already exists. Use repair or init --force after verification.")
    state = new_state(args)
    errors = validate_state(state, args.profile_key)
    if errors:
        raise SystemExit("Invalid state: " + "; ".join(errors))
    atomic_write(path, state, backup_path(args.profile_key) if path.exists() else None)
    set_active(args.profile_key)
    print(json.dumps(compact_state(state), ensure_ascii=False, indent=2))
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    key = resolve_profile_key(args.profile_key)
    if not key:
        raise SystemExit("No active profile. Run init first.")
    state = load_state(key)
    if not args.is_update and args.sequence != state["next_sequence"]:
        raise SystemExit(f"Expected sequence {state['next_sequence']:03d}, got {args.sequence:03d}")

    styles = state["visualization"]["used_styles"]
    if args.is_update:
        styles[:] = [item for item in styles if int(item.get("sequence", 0)) != args.sequence]
    style_names = {str(item.get("name", "")).casefold() for item in styles}
    if args.style_name.casefold() in style_names and not (args.allow_style_reuse or args.is_update):
        raise SystemExit(f"Style already used: {args.style_name}")
    if args.style_name.casefold() not in style_names:
        styles.append({
            "sequence": args.sequence,
            "name": args.style_name,
            "family": args.style_family,
            "layout": args.style_layout,
            "palette": args.style_palette,
            "era": args.style_era,
            "motif": args.style_motif,
        })
        styles.sort(key=lambda item: int(item.get("sequence", 0)))

    note = {
        "sequence": args.sequence,
        "page_id": args.page_id,
        "page_url": args.page_url,
        "source_url": args.source_url,
        "title": args.title,
        "author": args.author,
        "committed_at": now_iso(),
    }
    recent = [item for item in state.get("recent_notes", []) if item.get("source_url") != args.source_url]
    recent.append(note)
    state["recent_notes"] = recent[-50:]
    state["last_note"] = note
    state["next_sequence"] = max(state["next_sequence"], args.sequence + 1)
    authors = set(state["notion"].get("known_authors", []))
    if args.author:
        authors.add(args.author)
    state["notion"]["known_authors"] = sorted(authors)
    state["updated_at"] = now_iso()
    atomic_write(state_path(key), state, backup_path(key))
    set_active(key)
    print(json.dumps(compact_state(state), ensure_ascii=False, indent=2))
    return 0


def cmd_touch_schema(args: argparse.Namespace) -> int:
    key = resolve_profile_key(args.profile_key)
    if not key:
        raise SystemExit("No active profile. Run init first.")
    state = load_state(key)
    if args.database_id is not None:
        state["notion"]["database_id"] = args.database_id
    if args.data_source_id is not None:
        state["notion"]["data_source_id"] = args.data_source_id
    if args.database_name is not None:
        state["notion"]["database_name"] = args.database_name
    if args.property:
        property_map = dict(state["notion"].get("property_map", {}))
        property_map.update(dict(args.property))
        state["notion"]["property_map"] = property_map
    state["notion"]["schema_checked_at"] = args.checked_at or now_iso()
    state["updated_at"] = now_iso()
    atomic_write(state_path(key), state, backup_path(key))
    print(json.dumps(compact_state(state), ensure_ascii=False, indent=2))
    return 0


def cmd_set_visualization_mode(args: argparse.Namespace) -> int:
    key = resolve_profile_key(args.profile_key)
    if not key:
        raise SystemExit("No active profile. Run init first.")
    state = load_state(key)
    state["visualization"]["mode"] = args.mode
    state["updated_at"] = now_iso()
    atomic_write(state_path(key), state, backup_path(key))
    set_active(key)
    print(json.dumps(compact_state(state), ensure_ascii=False, indent=2))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    key = resolve_profile_key(args.profile_key)
    if not key:
        print(json.dumps({"ok": False, "errors": ["no active profile"]}, ensure_ascii=False))
        return 1
    try:
        state = read_json(state_path(key))
        errors = validate_state(state, key)
    except Exception as exc:  # concise diagnostic for recovery
        errors = [str(exc)]
    print(json.dumps({"ok": not errors, "profile_key": key, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def add_init_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--profile-key", required=True)
    parser.add_argument("--database-id", default="")
    parser.add_argument("--data-source-id", required=True)
    parser.add_argument("--database-name", default="Knowledge Notes")
    parser.add_argument("--schema-checked-at", default="")
    parser.add_argument("--next-sequence", type=int, required=True)
    parser.add_argument("--author", action="append", default=[])
    parser.add_argument("--property", action="append", type=parse_property, default=[])
    parser.add_argument("--style", action="append", type=parse_style, default=[])
    parser.add_argument("--last-sequence", type=int)
    parser.add_argument("--last-page-id", default="")
    parser.add_argument("--last-page-url", default="")
    parser.add_argument("--last-source-url", default="")
    parser.add_argument("--last-title", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("show", help="Print compact active state")
    show.add_argument("--profile-key")
    show.add_argument("--full", action="store_true")
    show.set_defaults(func=cmd_show)

    init = sub.add_parser("init", help="Initialize a profile after one-time Notion discovery")
    add_init_arguments(init)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=lambda args: cmd_init(args, repairing=False))

    repair = sub.add_parser("repair", help="Rebuild a profile from verified lightweight metadata")
    add_init_arguments(repair)
    repair.set_defaults(func=lambda args: cmd_init(args, repairing=True))

    commit = sub.add_parser("commit-note", help="Commit state only after Notion verification succeeds")
    commit.add_argument("--profile-key")
    commit.add_argument("--sequence", type=int, required=True)
    commit.add_argument("--page-id", required=True)
    commit.add_argument("--page-url", required=True)
    commit.add_argument("--source-url", required=True)
    commit.add_argument("--title", required=True)
    commit.add_argument("--author", default="")
    commit.add_argument("--style-name", required=True)
    commit.add_argument("--style-family", required=True)
    commit.add_argument("--style-layout", required=True)
    commit.add_argument("--style-palette", required=True)
    commit.add_argument("--style-era", default="")
    commit.add_argument("--style-motif", default="")
    commit.add_argument("--is-update", action="store_true")
    commit.add_argument("--allow-style-reuse", action="store_true")
    commit.set_defaults(func=cmd_commit)

    touch = sub.add_parser("touch-schema", help="Refresh cached schema identifiers/date")
    touch.add_argument("--profile-key")
    touch.add_argument("--database-id")
    touch.add_argument("--data-source-id")
    touch.add_argument("--database-name")
    touch.add_argument("--property", action="append", type=parse_property, default=[])
    touch.add_argument("--checked-at")
    touch.set_defaults(func=cmd_touch_schema)

    visual_mode = sub.add_parser("set-visualization-mode", help="Persist the preferred knowledge-map generation mode")
    visual_mode.add_argument("--profile-key")
    visual_mode.add_argument("mode", choices=sorted(VISUALIZATION_MODES))
    visual_mode.set_defaults(func=cmd_set_visualization_mode)

    check = sub.add_parser("check", help="Validate active or selected state")
    check.add_argument("--profile-key")
    check.set_defaults(func=cmd_check)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(0)
