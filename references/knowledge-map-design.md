# Knowledge-map art direction and quality gate

Read this reference before creating a knowledge map in efficient-standard or deep mode.

## Select the generation mode

Read `visualization_mode` from `state_manager.py show`.

- Missing or null: treat it as `hybrid`. New profiles are initialized this way.
- `hybrid` (default): compose the complete information structure as deterministic local SVG, then use the user's currently available built-in image-generation or aesthetic-enhancement tool for one bounded, text-free style accent. The AI layer is an enhancement, not the canvas. This consumes the user's current tool allowance; never switch to a paid API, install a provider, or request a new purchase without explicit authorization.
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

## Visual complexity budget

Calibrate ordinary knowledge maps to a clean editorial infographic, not a poster or cinematic scene:

- one title zone, one focal relationship, three to six primary modules, and at most one boundary/footer callout;
- one dominant style motif plus, when useful, one quieter supporting motif;
- two to four palette roles and three typographic levels;
- generous empty space around every major group;
- AI-generated imagery normally occupies no more than roughly 10–15% of the canvas.

Do not equate stronger style with more decoration. Full-canvas AI backgrounds, dense ornamental borders, multiple competing textures, glowing poster effects, and scene-filling illustration are blocking failures for an ordinary knowledge map. Use them only when the source itself requires a primarily illustrative scene and the user has asked for that direction.

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

- Build layout, grouping, hierarchy, connectors, whitespace, and every exact label locally first.
- Ask the image model for one text-free identifying accent such as a small icon, emblem, object, or restrained texture crop. Default to placing it in a header or focal zone and keep it within the visual complexity budget.
- Do not generate a full-canvas background or poster scene for an ordinary knowledge map.
- Do not ask it to render Chinese labels, logos, precise metrics, quotations, or logical arrows.
- Keep the knowledge structure, exact labels, connectors, and provenance in local SVG.
- Apply the same validate, audit, thumbnail, and visual-review gates.
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

Use compact style history to avoid repeating a prior composition, but do not optimize for novel names. A new style must be materially different in its visible grammar. When updating an existing note, preserve its accepted style name while improving materialization.
