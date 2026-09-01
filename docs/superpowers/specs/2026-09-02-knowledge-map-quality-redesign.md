# Knowledge Map Quality Redesign

## Objective

Replace the generic card-and-arrow knowledge-map output with a portable local SVG system that materially expresses each declared design style. Keep image generation optional, preserve exact Chinese text, and add a first-use preference that controls future visualization generation.

The migration also redesigns Inspiration notes 005–012 while preserving each note's current style name and body content.

## Root cause

The current Skill requires a distinct style description but does not require that description to be materialized in the SVG scene. The renderer validates schema and estimated text fit, while the actual output remains dominated by rectangular blocks, straight connectors, one fallback font stack, and manually selected flat colors. Technical validation therefore became a false proxy for design quality.

The fix must address both layers:

1. Skill instructions must define observable aesthetic acceptance criteria and require a visual preview review.
2. The local renderer must expose enough portable SVG primitives and audit signals to build genuinely different compositions.

## Visualization mode preference

Add a private per-profile visualization preference to `state_manager.py`:

- `local_svg`: default to the portable local SVG pipeline.
- `hybrid`: use an available image-generation tool for a text-free visual base, then overlay exact vector text and diagram structure locally.
- `ask_each_time`: ask before every new knowledge map.

If an existing profile has no preference, the Skill asks once before the first knowledge-map generation and stores the answer outside the published Skill folder. Users may change the preference later. A hybrid preference never authorizes installing software, purchasing a service, or using an unavailable tool; when image generation is unavailable, report the fallback and use local SVG.

## Local SVG v2 architecture

Preserve compatibility with existing v1 JSON specs while adding a v2 art-direction contract.

### Art-direction contract

Every v2 spec declares:

- reference style and historical/design family;
- central visual metaphor;
- composition signature;
- typography roles and scale;
- palette roles rather than an unstructured color list;
- two or more style-specific motifs;
- forbidden generic treatments for that composition;
- the exact relationship the map must make easier to understand.

These fields are not decorative metadata. The audit command checks that declared colors, motifs, type roles, and composition features are represented by actual scene objects.

### Portable scene primitives

Extend the standard-library SVG renderer with:

- linear and radial gradients;
- reusable patterns;
- clipping paths and masks;
- polygons, ellipses, arcs, curved paths, and grouped transforms;
- curved connectors with controllable markers;
- labels, captions, legends, number plates, and typographic roles;
- optional embedded raster background for hybrid mode;
- named layers so background, structure, labels, and evidence are kept separate.

No browser, paid API, external font, or image model is required for the default path. SVG remains the canonical output; PNG preview generation is optional when a compatible local browser or converter exists.

## Aesthetic audit and visual QA

Add a deterministic `audit` command that reports structural warning signals, including:

- style fields that are not materialized;
- excessive reliance on rectangular information cards;
- a scene with no non-rectangular motif;
- all connectors being straight and uniform;
- insufficient typographic hierarchy;
- an unstructured palette or poor role contrast;
- excessive text density;
- repeated geometry that makes the result equivalent to a generic flowchart.

The audit does not claim to measure beauty. Therefore the Skill also requires a rendered-preview review against a short rubric:

1. style fidelity;
2. composition and focal hierarchy;
3. typography and line breaking;
4. palette coherence;
5. thematic specificity;
6. thumbnail readability;
7. absence of generic office-flowchart appearance.

Any generic-flowchart failure is blocking even when schema validation and text-fit validation pass.

Detailed guidance lives in `references/knowledge-map-design.md`; the main `SKILL.md` links it only for efficient-standard and deep visualization work.

## Content-density rule

A knowledge map should normally encode three to six primary relationships. Supporting evidence, detailed steps, and edge cases remain in the note body or move to a second visual when necessary. The renderer must not solve overcrowding by shrinking all text or adding more cards.

## Hybrid mode

Hybrid mode is optional enhancement, not the portable baseline:

1. Generate a text-free illustration, material field, or atmospheric base that matches the approved style.
2. Do not ask the image model to render Chinese text, exact metrics, logos, or logical arrows.
3. Overlay exact labels, hierarchy, connectors, and evidence in local SVG.
4. Run the same audit and visual review as local mode.

## Migration: Inspiration 005–012

Preserve the existing style names while materially redesigning their visual languages:

| Note | Style | Required materialization |
|---|---|---|
| 005 | Cybernetic Control Diagram | instrument dials, feedback loops, signal traces, control-console hierarchy |
| 006 | Vienna Secession Portfolio Garden | botanical geometry, arches, ornamental borders, garden-like narrative path |
| 007 | 宋代界画叙事手卷 | horizontal handscroll, architectural gates, ruled-line structures, seal-like accents |
| 008 | Exploded Axonometric Assembly Diagram | isometric parts, exploded spacing, numbered callouts, assembly relationships |
| 009 | 地形勘探图 | contour field, trail, stations, legend, terrain-based evidence basin |
| 010 | Victorian Statistical Atlas Plate | engraved frame, chart grammar, data bands, chromolithographic palette |
| 011 | Space-Age Handoff Route Map | curved orbital routes, terminals, docking metaphor, airline-wayfinding typography |
| 012 | Machine-Age SEO Control Board | Art Deco symmetry, stepped geometry, gauges, sunburst and machine-panel motifs |

For each note:

- retain the current knowledge content and style name;
- reduce text to the essential visual relationships;
- generate and visually inspect a new SVG;
- replace only the existing knowledge-map image block in Notion;
- preserve evidence images, note body, properties, and hierarchy;
- verify the page still contains one knowledge map and its existing evidence anchors.

## Data flow

1. `state_manager.py show` returns the visualization preference when present.
2. The Skill asks for a mode only when required by the preference state.
3. Stable note synthesis produces a compact visual brief.
4. The agent authors a v2 scene spec using the declared style grammar.
5. `validate` checks schema and text fit; `audit` checks style materialization and generic-flowchart risks.
6. `render` produces SVG; the agent visually reviews a preview.
7. Failed visual review returns to art direction or layout, not merely card resizing.
8. A verified visual is uploaded and attached to Notion.

## Error handling

- Missing visualization preference: ask once; do not silently choose hybrid mode.
- Unavailable image generation in hybrid mode: report fallback and use local SVG.
- Audit warnings: block upload until resolved or explicitly justified in the run record.
- Preview conversion unavailable: inspect SVG through any available local viewer; do not treat conversion absence as aesthetic approval.
- Notion replacement failure: preserve the old image and stop after one failed targeted update.
- GitHub release failure: keep the verified local Skill changes and report the unsynchronized repository state.

## Testing

- Existing v1 renderer smoke tests continue to pass.
- Add v2 schema, render, validate, and audit fixtures.
- Add a deliberately generic card-flow fixture that must fail the aesthetic audit.
- Add a style-materialized fixture that passes without warnings.
- Test preference initialization, persistence, `ask_each_time`, and existing-profile compatibility.
- Run Skill quick validation and sensitive-data scans.
- Render and inspect all eight migrated maps at full size and thumbnail size.
- Verify targeted Notion replacements and unchanged page properties.
- Verify the installed Skill and GitHub clone have matching public files and commit SHA after publication.

## Scope boundaries

This change does not alter source evidence collection, note structure, database schema, author taxonomy, or existing non-knowledge-map images. It does not make image generation mandatory and does not promise that deterministic checks can prove subjective beauty; visual review remains a required human/agent judgment gate.
