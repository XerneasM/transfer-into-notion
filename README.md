# transfer-into-notion

A Codex skill that turns accessible articles, social posts and threads, webpages, PDFs, documents, videos, podcasts, images, local files, and mixed-media links into conclusion-led learning notes in a user-selected Notion database. Evidence collection adapts to the permissions the user has actually provided instead of assuming every source must be publicly extractable.

It preserves evidence provenance, chooses a source-appropriate structure, creates a fresh knowledge-map visual style for each standard/deep note, adds executable review, avoids duplicate source URLs, and synchronizes the current Codex task title to the finalized Notion title.

## Highlights

- Routes articles, threads, PDFs, videos, audio, images, and mixed-media pages through source-specific evidence rules.
- Selects among public/supplied evidence, an approved signed-in browser, and approved full local processing; it automatically falls back when a higher tier is unavailable.
- Can finish videos without public subtitles when the user has supplied media or authorized browser/local processing, while labeling local transcription uncertainty.
- Uses timelines for temporal media, argument chains for articles, page maps for documents, visual sequences for galleries, and evidence indexes for mixed sources.
- Uses clickable source anchors only when stable and verified.
- Writes into an existing Notion database selected during first-run setup without moving or reparenting existing pages.
- Stores private IDs, sequence history, author names, and style fingerprints outside the repository.
- Avoids duplicate notes by checking the canonical source URL.
- Adds external resources or next actions only when the source justifies them.
- Defaults to AI-integrated knowledge maps: the available built-in image tool designs information structure, hierarchy, typography, connectors, visual metaphor, and complete aesthetics together. Local SVG is the allowance-saving fallback, not the default compositor.
- Renames the calling Codex task to the exact finalized Notion title after verification.

## Requirements

- Codex with access to install local or GitHub-hosted skills.
- A connected Notion app or MCP capability with permission to read and write the selected database.
- Python 3.10 or newer.

## Install

Ask Codex to install this repository with $skill-installer, or copy the repository to:

- Windows: %USERPROFILE%\.codex\skills\transfer-into-notion
- macOS/Linux: ~/.codex/skills/transfer-into-notion

Restart or refresh Codex if the skill is not discovered immediately.

## First use

Invoke the skill with a URL, local file, or supplied source material:

    Use $transfer-into-notion to analyze this source, transfer the note into my Notion knowledge database, and sync this Codex task title: <URL or file>

On first use, the skill asks you to select an existing Notion database, maps its semantic properties, and creates compact private state. Knowledge maps default to AI-integrated generation using the user's current built-in tool allowance. Adjacent notes are selected from source-appropriate styles with a stable pseudo-random rule: retro styles remain available but cannot occur twice in a row, and consecutive maps must differ materially in visible grammar. If the user later says that allowance consumption is too high or requests local-only output, the skill saves `local_svg` for subsequent maps; it never silently changes modes or adds a paid provider. During later transfers it may append one verified source author to an existing mapped author select or multi-select while preserving all current options; every other schema change, database restructuring, or page move still requires explicit authorization.

Private state defaults to:

    ~/.codex/state/transfer-into-notion/

Override it with TRANSFER_INTO_NOTION_STATE_DIR. Existing users can continue from VIDEO_TRANSFER_NOTION_STATE_DIR or ~/.codex/state/video-transfer-notion/ until state is copied and verified in the new location. State files, Notion IDs, source contents, transcripts, credentials, and generated attachments are not stored in this repository.

## Note modes

- **Concise:** conclusion, method, source structure, and action checklist.
- **Efficient standard:** full note, one new knowledge-map style, representative evidence visuals only when useful, source-appropriate evidence index, and review plan.
- **Deep:** section-level analysis, richer multimodal evidence, and broader validation when useful.

## Repository layout

    SKILL.md                         Skill entry point
    agents/openai.yaml               Codex UI metadata
    references/setup.md              First-run Notion mapping
    references/permission-routing.md Permission tiers, escalation, and local-processing boundaries
    references/source-routing.md     Multimodal source and evidence routing
    references/knowledge-map-design.md Local/hybrid modes and visual QA gate
    references/notion-note-spec.md   Note structure, title sync, and QA
    references/extension-resources.md Conditional enrichment rules
    scripts/state_manager.py         Private cross-platform state
    scripts/select_knowledge_map_style.py Stable candidate selection with adjacent-style guards
    scripts/test_style_selector.py Portable style-selection smoke tests
    scripts/render_knowledge_map.py  Local SVG v2 renderer and aesthetic audit
    scripts/test_knowledge_map.py    Portable knowledge-map smoke tests

## Privacy and permissions

- Permission tiers are capabilities, not blanket authority. The skill uses the lowest tier that can support the note and records the route when it affects completeness.
- Full local access does not authorize reading/exporting cookies, credentials, unrelated files, or hidden secrets, and it never permits DRM/paywall bypass.
- Missing local transcription/OCR dependencies are installed only with separate authorization unless the user already granted it explicitly.
- Review third-party sources under their access and copyright rules.
- Notion writes occur only when the user asks to create, transfer, record, or update a note.
- The skill creates or updates a record inside the selected database; it does not move the database or unrelated pages.
- Installation, deployment, purchases, account authorization, contact with other people, destructive Notion changes, and page moving/reparenting require separate permission.
- Before publishing a fork, scan it for API keys, Notion IDs, attachment URLs, private source content, and local absolute paths.

## License

MIT
