#!/usr/bin/env python3
"""Portable smoke tests for the knowledge-map renderer and visualization state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RENDERER = ROOT / "render_knowledge_map.py"
STATE = ROOT / "state_manager.py"


def run(*args: str, env: dict[str, str] | None = None, expect: int = 0) -> dict:
    result = subprocess.run([sys.executable, *args], text=True, encoding="utf-8", capture_output=True, env=env)
    if result.returncode != expect:
        raise AssertionError(f"expected {expect}, got {result.returncode}: {result.stdout}\n{result.stderr}")
    return json.loads(result.stdout)


def materialized_spec() -> dict:
    return {
        "schema_version": 2,
        "canvas": {"width": 1200, "height": 800, "background": "#F5EEDC"},
        "style": {"name": "Test Atlas", "family": "statistical atlas", "layout": "radial plate", "palette": "ink, ivory, red", "traits": "engraved radial evidence plate"},
        "art_direction": {
            "metaphor": "evidence compass",
            "composition": "radial plate with curved return",
            "relationship": "three signals converge on one decision",
            "motifs": ["compass", "engraving"],
            "forbidden": ["generic cards"],
            "palette_roles": {"ground": "#F5EEDC", "ink": "#17233A", "signal": "#B74735"},
            "typography_roles": {"display": "36/900", "label": "22/700", "caption": "16/500"},
        },
        "defs": {"gradients": [{"id": "signal", "type": "radial", "stops": [{"offset": "0%", "color": "#F2C66D"}, {"offset": "100%", "color": "#B74735"}]}]},
        "shapes": [
            {"type": "circle", "cx": 600, "cy": 410, "r": 190, "fill": "url(#signal)", "motif": "compass", "palette_role": "signal"},
            {"type": "path", "d": "M170 520 C320 700 880 700 1030 520", "stroke": "#17233A", "stroke_width": 6, "motif": "engraving", "palette_role": "ink"},
            {"type": "polygon", "points": "600,160 635,240 600,220 565,240", "fill": "#17233A", "motif": "compass", "palette_role": "ink"},
            {"type": "ellipse", "cx": 600, "cy": 410, "rx": 330, "ry": 250, "fill": "none", "stroke": "#17233A", "stroke_width": 2, "motif": "engraving", "palette_role": "ground"},
        ],
        "connectors": [{"d": "M260 410 C360 280 470 260 540 330", "color": "#B74735", "stroke_width": 5, "motif": "compass", "palette_role": "signal"}],
        "texts": [
            {"x": 80, "y": 90, "text": "证据罗盘", "font_size": 42, "weight": 900, "role": "display", "palette_role": "ink"},
            {"x": 600, "y": 405, "text": "判断", "font_size": 26, "weight": 800, "anchor": "middle", "role": "label", "palette_role": "signal"},
            {"x": 80, "y": 745, "text": "三条证据汇入一个决策", "font_size": 17, "role": "caption", "palette_role": "ground"},
        ],
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        good = temp / "good.json"
        good.write_text(json.dumps(materialized_spec(), ensure_ascii=False), encoding="utf-8")
        assert run(str(RENDERER), "validate", str(good))["ok"]
        assert run(str(RENDERER), "audit", str(good))["ok"]
        output = temp / "good.svg"
        assert run(str(RENDERER), "render", str(good), str(output))["ok"] and output.exists()

        generic = materialized_spec()
        generic["blocks"] = [
            {"x": 40 + i * 220, "y": 260, "w": 190, "h": 180, "title": f"Step {i}", "body": ["generic card"]}
            for i in range(5)
        ]
        generic["shapes"] = []
        generic["connectors"] = [{"x1": 100, "y1": 100 + i * 30, "x2": 1000, "y2": 100 + i * 30} for i in range(4)]
        bad = temp / "generic.json"
        bad.write_text(json.dumps(generic, ensure_ascii=False), encoding="utf-8")
        audit = run(str(RENDERER), "audit", str(bad), expect=1)
        assert any("generic-flowchart" in item for item in audit["warnings"])

        env = os.environ.copy()
        env["TRANSFER_INTO_NOTION_STATE_DIR"] = str(temp / "state")
        init = run(
            str(STATE), "init", "--profile-key", "test", "--data-source-id", "ds", "--next-sequence", "1",
            env=env,
        )
        assert init["visualization_mode"] == "hybrid"
        selected = run(str(STATE), "set-visualization-mode", "local_svg", env=env)
        assert selected["visualization_mode"] == "local_svg"
        shown = run(str(STATE), "show", env=env)
        assert shown["visualization_mode"] == "local_svg"
        restored = run(str(STATE), "set-visualization-mode", "hybrid", env=env)
        assert restored["visualization_mode"] == "hybrid"

    print(json.dumps({"ok": True, "tests": ["v2_validate", "v2_audit", "generic_rejection", "visualization_mode"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
