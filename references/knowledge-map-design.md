# Knowledge-map art direction and quality gate

Read this reference before creating a knowledge map in efficient-standard or deep mode.

## Select the generation mode

Read `visualization_mode` from `state_manager.py show`.

- Missing or null: treat it as `hybrid`. New profiles are initialized this way.
- `hybrid` (default): use the user's currently available built-in image-generation or aesthetic-enhancement tool as the primary renderer for one integrated knowledge map. Ask it to design the information structure, hierarchy, composition, typography, connectors, visual metaphor, and complete aesthetic as one system. Local editing may repair exact labels after generation, but must not replace the AI-designed structure by default. This consumes the user's current tool allowance; never switch to a paid API, install a provider, or request a new purchase without explicit authorization.
- `local_svg`: use the portable local SVG pipeline. Persist this downgrade only when the user explicitly asks to save allowance, says the AI-image cost is too high, or directly requests local-only output.
- `ask_each_time`: ask before this map and do not silently change the saved preference.

Do not ask a first-use mode question. Start with the AI-enhanced default. If the built-in tool is unavailable or exhausted, disclose that the default cannot run and ask before changing the saved mode; do not silently downgrade. Users may still select 本地高级 SVG, AI 审美增强, or 每次询问 at any time.

## Start with art direction, not boxes

Write a compact visual brief before geometry:

1. What relationship must the image make easier to understand?
2. What single visual metaphor belongs to the source?
3. What real design family will govern composition, type, line, color, and ornament?
4. Which one or two motifs visibly prove that family was used?
5. Which generic treatments would betray the concept?

The style name is not evidence of style fidelity. A declared style is valid only when its motifs, composition, typography roles, and palette roles are materialized by actual scene objects.

## Readability and aesthetic balance

Calibrate ordinary knowledge maps to a polished editorial infographic whose visual language and information architecture feel inseparable:

- one title zone, one focal relationship, three to six primary modules, and at most one boundary/footer callout;
- a clear dominant visual idea, controlled supporting detail, and at least three typographic levels;
- generous empty space around every major group;
- readable labels and relationships at Notion page width.

Do not impose a fixed limit on how much of the canvas AI may generate. Full-canvas composition, illustration, texture, or atmosphere is allowed when it supports the hierarchy. Reject only when decoration, effects, or scene detail compete with the content, when labels become hard to scan, or when the relationship is less clear than a simpler treatment.

## Density and hierarchy

- Encode three to six primary relationships in one image.
- Move detailed evidence, edge cases, and secondary steps back to the note body.
- Prefer one focal structure plus supporting annotations over equal-weight cards.
- Use at least three typographic levels: display, structural label, and caption.
- Write labels for scanning. Do not shrink text to rescue overcrowding.
- Split into a second visual when one composition cannot remain legible at Notion page width.

## Avoid generic-flowchart output

Reject the result when any of these remain true after removing the style caption:

- it could be described as pastel rectangles joined by arrows;
- the declared historical/design family is not recognizable from the image itself;
- every idea receives the same box, weight, and visual priority;
- changing only the palette would make it equivalent to a previous map;
- the diagram explains sequence but has no visual metaphor;
- decoration is added around an unchanged office-flowchart core.

Cards may be used sparingly for bounded evidence, not as the default representation of every concept.

## Local SVG v2 workflow

1. Run `python scripts/render_knowledge_map.py schema`.
2. Author a `schema_version: 2` spec with `art_direction` and style-tagged scene objects.
3. Use gradients, patterns, paths, polygons, ellipses, curved connectors, labels, legends, and layered motifs as the concept requires.
4. Run `validate`; resolve every error and text-fit warning.
5. Run `audit`; resolve every style-materialization or generic-flowchart warning.
6. Run `render` and generate a local preview when possible.
7. Inspect at full size and thumbnail size. If it looks generic, revise the art direction or composition instead of merely resizing cards.

The renderer's audit is a warning system, not proof of beauty. Visual review is mandatory.

## Hybrid workflow

Use hybrid mode by default when an image-generation tool is already available.

- Freeze an exact-content brief first: thesis, required modules, relationships, mandatory labels, and prohibited additions.
- Ask the image model to generate the complete knowledge map as one integrated design. It may determine the layout, grouping, connectors, typography, motifs, and full-canvas treatment as long as the exact-content brief remains intact.
- Inspect the generated result at full and thumbnail size. Regenerate when the structure, hierarchy, or readability fails; do not silently substitute a locally designed structure.
- Prefer another AI edit or regeneration when Chinese labels, metrics, or relationships are wrong. A local overlay may make surgical text corrections only after the integrated composition is accepted and only when the correction does not redesign the information structure.
- Keep provenance outside the image when dense provenance would reduce readability.
- If the user says allowance consumption is too high, finish the current safe step, persist `local_svg`, and use local advanced SVG for subsequent maps. Do not infer this preference from ordinary quality feedback.

## Visual review rubric

Score each dimension from 1–5 and revise any dimension below 4:

- **Style fidelity:** the declared family is visible without reading its name.
- **Composition:** there is a clear focal point and intentional eye path.
- **Typography:** line breaks, scale, spacing, and contrast support hierarchy.
- **Palette:** roles are coherent and accents are controlled.
- **Thematic specificity:** the image belongs to this source, not any workflow.
- **Thumbnail readability:** the main relationship survives at reduced size.
- **Craft:** curves, alignments, spacing, and ornament feel intentional.
- **Restraint:** decoration never competes with the title, structure, or labels.

Generic office-flowchart appearance and decorative overload are both blocking failures regardless of the average score.

## Style-history rule

Use compact style history to prevent adjacent notes from looking like the same visual family. Do not ban retro or historical styles globally: they may recur after an intervening non-retro style. The hard rule is that two clearly retro/historical styles must not appear consecutively.

Before generation, create three to five source-appropriate candidates with `name`, `family`, `era`, `layout`, `palette`, `motif`, and `content_fit`. Compare them with the immediately preceding style:

- reject a retro/historical candidate when the immediately preceding style is also retro/historical;
- reject a candidate whose family is the same, or whose layout plus palette/motif are substantially similar, to the immediately preceding style;
- do not reject a retro candidate merely because an older non-adjacent note used a retro style;
- among the remaining highest-fit candidates, select stably and pseudo-randomly from the canonical source URL plus sequence number so identical inputs produce the same choice.

Use `scripts/select_knowledge_map_style.py` for this selection. When updating an existing note, preserve an accepted style only if the user asks to keep it; otherwise rerun candidate selection when the purpose is to correct adjacent similarity.
