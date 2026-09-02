#!/usr/bin/env python3
"""Portable smoke tests for adjacent knowledge-map style selection."""

from select_knowledge_map_style import rejection_reason, select_style


def run() -> None:
    previous = {
        "sequence": 12,
        "name": "Machine-Age SEO Control Board",
        "family": "1920s Art Deco machine-age information design",
        "era": "retro",
        "layout": "stepped pipeline",
        "palette": "navy gold jade",
        "motif": "ziggurat gauge",
    }
    retro = {
        "name": "Victorian Plate",
        "family": "Victorian statistical atlas",
        "era": "historical",
        "layout": "radial plate",
        "palette": "ivory oxblood",
        "motif": "engraved chart",
        "content_fit": 5,
    }
    modern_a = {
        "name": "Contemporary Signal Field",
        "family": "contemporary data editorial",
        "era": "contemporary",
        "layout": "open signal field",
        "palette": "white cobalt lime",
        "motif": "live data pulse",
        "content_fit": 5,
    }
    modern_b = {
        "name": "Spatial Product Canvas",
        "family": "contemporary spatial product design",
        "era": "contemporary",
        "layout": "layered spatial canvas",
        "palette": "graphite cyan coral",
        "motif": "floating interface planes",
        "content_fit": 5,
    }
    assert rejection_reason(retro, previous) == "retro styles cannot be adjacent"
    history = {"used_styles": [previous]}
    first = select_style([retro, modern_a, modern_b], history, "https://example.com/source", 13)
    second = select_style([retro, modern_a, modern_b], history, "https://example.com/source", 13)
    assert first["selected"] == second["selected"]
    assert first["selected"]["era"] == "contemporary"
    print('{"ok": true, "tests": ["retro_adjacency", "stable_seed", "eligible_selection"]}')


if __name__ == "__main__":
    run()
