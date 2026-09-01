# Knowledge-map art direction and quality gate

Read this reference before creating a knowledge map in efficient-standard or deep mode.

## Select the generation mode

Read `visualization_mode` from `state_manager.py show`.

- Missing or null: ask the user once which default to use, then persist it with `state_manager.py set-visualization-mode MODE`.
- `local_svg`: use the portable local SVG pipeline.
- `hybrid`: when an image-generation tool is available, create a text-free visual base and overlay exact vector labels locally. If unavailable, disclose the fallback and use local SVG; do not install or purchase anything.
- `ask_each_time`: ask before this map and do not silently change the saved preference.

Offer three user-facing choices: 本地高级 SVG, 混合增强（SVG + 图片生成）, or 每次询问. Explain that local SVG is portable and text-accurate; hybrid can add illustrative texture but remains optional.

## Start with art direction, not boxes

Write a compact visual brief before geometry:

1. What relationship must the image make easier to understand?
2. What single visual metaphor belongs to the source?
3. What real design family will govern composition, type, line, color, and ornament?
4. Which two or more motifs visibly prove that family was used?
5. Which generic treatments would betray the concept?

The style name is not evidence of style fidelity. A declared style is valid only when its motifs, composition, typography roles, and palette roles are materialized by actual scene objects.

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

Use hybrid mode only when selected and an image-generation tool is already available.

- Ask the image model for a text-free illustration, material field, or atmospheric base.
- Do not ask it to render Chinese labels, logos, precise metrics, quotations, or logical arrows.
- Keep the knowledge structure, exact labels, connectors, and provenance in local SVG.
- Apply the same validate, audit, thumbnail, and visual-review gates.

## Visual review rubric

Score each dimension from 1–5 and revise any dimension below 4:

- **Style fidelity:** the declared family is visible without reading its name.
- **Composition:** there is a clear focal point and intentional eye path.
- **Typography:** line breaks, scale, spacing, and contrast support hierarchy.
- **Palette:** roles are coherent and accents are controlled.
- **Thematic specificity:** the image belongs to this source, not any workflow.
- **Thumbnail readability:** the main relationship survives at reduced size.
- **Craft:** curves, alignments, spacing, and ornament feel intentional.

Generic office-flowchart appearance is a blocking failure regardless of the average score.

## Style-history rule

Use compact style history to avoid repeating a prior composition, but do not optimize for novel names. A new style must be materially different in its visible grammar. When updating an existing note, preserve its accepted style name while improving materialization.
