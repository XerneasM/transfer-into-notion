#!/usr/bin/env python3
"""Render a style-neutral declarative knowledge map to an opaque SVG.

The script contains no design-style templates. Each note supplies a fresh style
brief, geometry, palette, type scale, blocks, connectors, and decorations.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable


DEFAULT_FONT = "Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def units(text: str) -> float:
    total = 0.0
    for char in text:
        if unicodedata.east_asian_width(char) in {"W", "F"}:
            total += 1.0
        elif char.isspace():
            total += 0.35
        else:
            total += 0.58
    return total


def wrap_text(text: str, width: float, font_size: float) -> list[str]:
    if not text:
        return []
    capacity = max(2.0, width / max(font_size, 1.0))
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and units(candidate) > capacity:
            lines.append(current.rstrip())
            current = char.lstrip()
        else:
            current = candidate
    if current:
        lines.append(current.rstrip())
    return lines


def require_number(obj: dict[str, Any], key: str, errors: list[str], where: str) -> float:
    value = obj.get(key)
    if not isinstance(value, (int, float)):
        errors.append(f"{where}.{key} must be numeric")
        return 0.0
    return float(value)


def validate_spec(spec: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    canvas = spec.get("canvas")
    if not isinstance(canvas, dict):
        return ["canvas must be an object"], warnings
    width = require_number(canvas, "width", errors, "canvas")
    height = require_number(canvas, "height", errors, "canvas")
    background = str(canvas.get("background", "")).strip().lower()
    if background in {"", "none", "transparent"}:
        errors.append("canvas.background must be opaque")
    style = spec.get("style")
    if not isinstance(style, dict):
        errors.append("style must be an object")
    else:
        for key in ("name", "family", "layout", "palette", "traits"):
            if not str(style.get(key, "")).strip():
                errors.append(f"style.{key} is required")

    blocks = spec.get("blocks", [])
    if not isinstance(blocks, list):
        errors.append("blocks must be a list")
        blocks = []
    for index, block in enumerate(blocks):
        where = f"blocks[{index}]"
        if not isinstance(block, dict):
            errors.append(f"{where} must be an object")
            continue
        x = require_number(block, "x", errors, where)
        y = require_number(block, "y", errors, where)
        w = require_number(block, "w", errors, where)
        h = require_number(block, "h", errors, where)
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            errors.append(f"{where} is outside canvas bounds")
        padding = float(block.get("padding", 28))
        title_size = float(block.get("title_size", 30))
        body_size = float(block.get("body_size", 21))
        leading = float(block.get("leading", 1.35))
        available = max(1.0, w - 2 * padding)
        title_lines = wrap_text(str(block.get("title", "")), available, title_size)
        body_items = block.get("body", [])
        if isinstance(body_items, str):
            body_items = [body_items]
        body_lines = sum((wrap_text(str(item), available, body_size) for item in body_items), [])
        estimated = padding + len(title_lines) * title_size * 1.25
        if title_lines and body_lines:
            estimated += body_size * 0.7
        estimated += len(body_lines) * body_size * leading + padding
        if estimated > h:
            warnings.append(f"{where} estimated text height {estimated:.0f}px exceeds block height {h:.0f}px")

    for collection in ("texts", "shapes", "connectors", "decorations"):
        if collection in spec and not isinstance(spec[collection], list):
            errors.append(f"{collection} must be a list")
    return errors, warnings


def attrs(values: dict[str, Any]) -> str:
    return " ".join(f'{key.replace("_", "-")}="{esc(value)}"' for key, value in values.items() if value is not None)


def render_text(x: float, y: float, lines: Iterable[str], font_size: float, color: str,
                weight: int | str, line_height: float, anchor: str = "start",
                family: str = DEFAULT_FONT, italic: bool = False) -> str:
    parts = [f'<text {attrs({"x": x, "y": y, "font-family": family, "font-size": font_size, "font-weight": weight, "fill": color, "text-anchor": anchor, "font-style": "italic" if italic else None})}>']
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else font_size * line_height
        parts.append(f'<tspan x="{esc(x)}" dy="{esc(dy)}">{esc(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def render_shape(shape: dict[str, Any]) -> str:
    kind = shape.get("type", "rect")
    common = {
        "fill": shape.get("fill", "none"),
        "stroke": shape.get("stroke", "none"),
        "stroke-width": shape.get("stroke_width", 0),
        "opacity": shape.get("opacity", 1),
    }
    if kind == "rect":
        return f'<rect {attrs({**common, "x": shape.get("x", 0), "y": shape.get("y", 0), "width": shape.get("w", 0), "height": shape.get("h", 0), "rx": shape.get("radius", 0), "transform": shape.get("transform")})}/>'
    if kind == "circle":
        return f'<circle {attrs({**common, "cx": shape.get("cx", 0), "cy": shape.get("cy", 0), "r": shape.get("r", 0)})}/>'
    if kind == "line":
        return f'<line {attrs({**common, "x1": shape.get("x1", 0), "y1": shape.get("y1", 0), "x2": shape.get("x2", 0), "y2": shape.get("y2", 0), "stroke-linecap": shape.get("linecap", "round")})}/>'
    if kind == "path":
        return f'<path {attrs({**common, "d": shape.get("d", ""), "stroke-linecap": shape.get("linecap", "round"), "stroke-linejoin": shape.get("linejoin", "round")})}/>'
    raise ValueError(f"Unsupported shape type: {kind}")


def render_decoration(item: dict[str, Any]) -> str:
    kind = item.get("type")
    if kind == "grid":
        x, y, w, h = (float(item.get(k, 0)) for k in ("x", "y", "w", "h"))
        step = max(4.0, float(item.get("step", 24)))
        color = item.get("color", "#111111")
        opacity = item.get("opacity", 0.12)
        stroke = item.get("stroke_width", 1)
        lines = []
        for gx in range(math.floor(x), math.ceil(x + w) + 1, math.floor(step)):
            lines.append(f'<line x1="{gx}" y1="{y}" x2="{gx}" y2="{y+h}" stroke="{esc(color)}" stroke-width="{stroke}" opacity="{opacity}"/>')
        for gy in range(math.floor(y), math.ceil(y + h) + 1, math.floor(step)):
            lines.append(f'<line x1="{x}" y1="{gy}" x2="{x+w}" y2="{gy}" stroke="{esc(color)}" stroke-width="{stroke}" opacity="{opacity}"/>')
        return "".join(lines)
    if kind == "dots":
        x, y, w, h = (float(item.get(k, 0)) for k in ("x", "y", "w", "h"))
        step = max(6.0, float(item.get("step", 24)))
        radius = float(item.get("radius", 2))
        color = item.get("color", "#111111")
        opacity = item.get("opacity", 0.15)
        dots = []
        gx = x
        while gx <= x + w:
            gy = y
            while gy <= y + h:
                dots.append(f'<circle cx="{gx}" cy="{gy}" r="{radius}" fill="{esc(color)}" opacity="{opacity}"/>')
                gy += step
            gx += step
        return "".join(dots)
    return render_shape(item)


def render_svg(spec: dict[str, Any]) -> str:
    canvas = spec["canvas"]
    width = int(canvas["width"])
    height = int(canvas["height"])
    family = spec.get("typography", {}).get("font_family", DEFAULT_FONT)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
        f'<rect width="{width}" height="{height}" fill="{esc(canvas["background"])}"/>',
    ]
    for item in spec.get("decorations", []):
        out.append(render_decoration(item))
    for shape in spec.get("shapes", []):
        out.append(render_shape(shape))
    for connector in spec.get("connectors", []):
        out.append(f'<line {attrs({"x1": connector.get("x1"), "y1": connector.get("y1"), "x2": connector.get("x2"), "y2": connector.get("y2"), "stroke": connector.get("color", "#111"), "stroke-width": connector.get("stroke_width", 4), "stroke-dasharray": connector.get("dash"), "marker-end": "url(#arrow)" if connector.get("arrow", True) else None})}/>')
    for block in spec.get("blocks", []):
        x, y, w, h = (float(block[k]) for k in ("x", "y", "w", "h"))
        shadow = block.get("shadow")
        if isinstance(shadow, dict):
            out.append(f'<rect {attrs({"x": x + float(shadow.get("dx", 8)), "y": y + float(shadow.get("dy", 8)), "width": w, "height": h, "rx": block.get("radius", 0), "fill": shadow.get("color", "#111"), "opacity": shadow.get("opacity", 1)})}/>')
        out.append(f'<rect {attrs({"x": x, "y": y, "width": w, "height": h, "rx": block.get("radius", 0), "fill": block.get("fill", "#fff"), "stroke": block.get("stroke", "#111"), "stroke-width": block.get("stroke_width", 3)})}/>')
        padding = float(block.get("padding", 28))
        title_size = float(block.get("title_size", 30))
        body_size = float(block.get("body_size", 21))
        leading = float(block.get("leading", 1.35))
        color = block.get("color", "#111")
        title_lines = wrap_text(str(block.get("title", "")), w - 2 * padding, title_size)
        cursor = y + padding + title_size
        if title_lines:
            out.append(render_text(x + padding, cursor, title_lines, title_size, block.get("title_color", color), block.get("title_weight", 800), 1.2, family=family))
            cursor += max(0, len(title_lines) - 1) * title_size * 1.2 + body_size * 1.1
        body = block.get("body", [])
        if isinstance(body, str):
            body = [body]
        for item in body:
            lines = wrap_text(str(item), w - 2 * padding, body_size)
            if not lines:
                continue
            prefix = block.get("bullet", "")
            if prefix:
                lines[0] = f"{prefix}{lines[0]}"
            out.append(render_text(x + padding, cursor, lines, body_size, color, block.get("body_weight", 500), leading, family=family))
            cursor += len(lines) * body_size * leading + body_size * 0.35
    for text in spec.get("texts", []):
        size = float(text.get("font_size", 24))
        width_limit = float(text.get("w", spec["canvas"]["width"]))
        lines = wrap_text(str(text.get("text", "")), width_limit, size)
        max_lines = int(text.get("max_lines", len(lines) or 1))
        out.append(render_text(float(text.get("x", 0)), float(text.get("y", 0)), lines[:max_lines], size, text.get("color", "#111"), text.get("weight", 600), float(text.get("leading", 1.25)), anchor=text.get("anchor", "start"), family=family, italic=bool(text.get("italic", False))))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def load_spec(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Spec root must be an object")
    return value


def schema_summary() -> dict[str, Any]:
    return {
        "purpose": "Fresh style brief + arbitrary geometry; no style presets",
        "required": {
            "canvas": {"width": 1600, "height": 1000, "background": "opaque color"},
            "style": {"name": "real style name", "family": "distinct family", "layout": "layout signature", "palette": "palette signature", "traits": "one-sentence traits"},
            "blocks": [{"x": 60, "y": 180, "w": 440, "h": 260, "title": "...", "body": ["..."], "fill": "#FFFFFF", "stroke": "#111111"}],
        },
        "optional": {
            "typography": {"font_family": DEFAULT_FONT},
            "texts": ["absolute text objects"],
            "shapes": ["rect, circle, line, or path objects"],
            "connectors": ["x1, y1, x2, y2, color, arrow"],
            "decorations": ["grid, dots, rect, circle, line, or path"],
        },
        "rule": "Choose all style and geometry values per note; validate until warnings are resolved.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("schema", help="Print compact declarative schema")
    validate = sub.add_parser("validate", help="Validate a JSON spec without rendering")
    validate.add_argument("spec")
    render = sub.add_parser("render", help="Validate and render a JSON spec")
    render.add_argument("spec")
    render.add_argument("output")
    render.add_argument("--allow-warnings", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "schema":
        print(json.dumps(schema_summary(), ensure_ascii=False, indent=2))
        return 0
    spec = load_spec(args.spec)
    errors, warnings = validate_spec(spec)
    result = {"ok": not errors and not warnings, "errors": errors, "warnings": warnings}
    if args.command == "validate":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not errors and not warnings else 1
    if errors or (warnings and not args.allow_warnings):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    svg = render_svg(spec)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8", newline="\n")
    result.update({"ok": True, "output": str(output.resolve()), "bytes": output.stat().st_size, "style": spec["style"]})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
