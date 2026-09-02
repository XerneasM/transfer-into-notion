#!/usr/bin/env python3
"""Select a source-fit knowledge-map style with adjacent-style guards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


RETRO_MARKERS = {
    "retro", "historical", "historic", "vintage", "period", "victorian",
    "art deco", "secession", "jugendstil", "mid-century", "1960s", "1920s",
    "song dynasty", "复古", "历史", "古典", "年代", "宋代", "维多利亚",
}


def load_json(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def tokens(value: Any) -> set[str]:
    return {item for item in re.split(r"[^\w\u4e00-\u9fff]+", normalize(value)) if item}


def overlap(left: Any, right: Any) -> float:
    a, b = tokens(left), tokens(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def is_retro(style: dict[str, Any]) -> bool:
    haystack = " ".join(normalize(style.get(key)) for key in ("era", "family", "name"))
    return any(marker in haystack for marker in RETRO_MARKERS)


def previous_style(history: Any) -> dict[str, Any] | None:
    if isinstance(history, dict):
        if isinstance(history.get("used_styles"), list):
            history = history["used_styles"]
        elif isinstance(history.get("visualization"), dict):
            history = history["visualization"].get("used_styles", [])
    if not isinstance(history, list) or not history:
        return None
    valid = [item for item in history if isinstance(item, dict)]
    return max(valid, key=lambda item: int(item.get("sequence", 0))) if valid else None


def rejection_reason(candidate: dict[str, Any], previous: dict[str, Any] | None) -> str | None:
    if not previous:
        return None
    if is_retro(candidate) and is_retro(previous):
        return "retro styles cannot be adjacent"
    family = normalize(candidate.get("family"))
    if family and family == normalize(previous.get("family")):
        return "same family as previous style"
    layout = overlap(candidate.get("layout"), previous.get("layout"))
    palette = overlap(candidate.get("palette"), previous.get("palette"))
    motif = overlap(candidate.get("motif"), previous.get("motif"))
    if layout >= 0.5 and max(palette, motif) >= 0.4:
        return "layout and palette/motif are too similar to previous style"
    return None


def select_style(
    candidates: list[dict[str, Any]],
    history: Any,
    source_url: str,
    sequence: int,
) -> dict[str, Any]:
    previous = previous_style(history)
    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for candidate in candidates:
        reason = rejection_reason(candidate, previous)
        if reason:
            rejected.append({"name": str(candidate.get("name", "")), "reason": reason})
        else:
            eligible.append(candidate)
    if not eligible:
        raise ValueError("No eligible style remains; generate new source-appropriate candidates")
    best_fit = max(float(item.get("content_fit", 0)) for item in eligible)
    finalists = sorted(
        (item for item in eligible if float(item.get("content_fit", 0)) == best_fit),
        key=lambda item: normalize(item.get("name")),
    )
    digest = hashlib.sha256(f"{source_url}|{sequence}".encode("utf-8")).digest()
    selected = finalists[int.from_bytes(digest[:8], "big") % len(finalists)]
    return {
        "selected": selected,
        "previous": previous,
        "eligible_count": len(eligible),
        "finalist_count": len(finalists),
        "rejected": rejected,
        "seed_basis": "canonical_source_url|sequence",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", required=True, help="JSON list or object with a candidates list")
    parser.add_argument("--history", required=True, help="state_manager show/full JSON or a used_styles list")
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--sequence", required=True, type=int)
    args = parser.parse_args()
    raw_candidates = load_json(args.candidates)
    if isinstance(raw_candidates, dict):
        raw_candidates = raw_candidates.get("candidates")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise SystemExit("candidates must be a non-empty JSON list")
    try:
        result = select_style(raw_candidates, load_json(args.history), args.source_url, args.sequence)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
