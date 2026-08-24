# First-run Notion setup

Read this file only when state_manager.py show reports no healthy active profile, or when the cached data-source schema is no longer valid.

## Requirements

- A connected Notion app or MCP capability with read and write access to the target database.
- Python 3.10 or newer for the state and SVG helper scripts.
- A Notion database chosen by the user. Do not create a database, properties, views, or page hierarchy without explicit authorization.

## Select and inspect the destination

1. If the user supplied a Notion database URL, inspect that data source. Otherwise search the user's accessible Notion databases and present only the most plausible knowledge-note candidates.
2. Reuse an existing database when practical. If no suitable database exists, ask whether the user wants one created and show the proposed properties before writing anything.
3. Fetch the selected data-source schema once. Determine its database ID, data-source ID, displayed name, property types, and available select options.
4. Preserve the database's current parent and all sibling top-level pages. Setup never moves, nests, or reparents existing Notion content.

## Map semantic property roles

Map by property type and meaning rather than exact spelling:

- title -> the data source's single title property; required.
- author -> person, text, select, or multi-select property representing the primary source creator.
- platform -> select, multi-select, or text property for the source platform or container.
- source_url -> URL or text property for the canonical source link.
- content_type -> select, multi-select, or text property; use an existing article, social, document, video, audio, image, or other equivalent option.
- timeliness -> select, multi-select, or text property for durability or version sensitivity.

Only title is universally required. If a useful optional role is missing or a non-author select lacks a source value, either omit it or ask for authorization before changing the schema. A mapped author property that already has type `select` or `multi_select` follows the guarded automatic author-option procedure in [notion-note-spec.md](notion-note-spec.md). Never silently repurpose an unrelated property.

## Bootstrap compact state

1. Query only the fields needed to detect matching canonical source URLs, the highest sequence number, known authors, and previously recorded knowledge-map style labels. Do not fetch prior note bodies or signed image URLs.
2. Start at sequence 1 when no compatible numbered notes exist. Otherwise use the next unused sequence.
3. Use a stable workspace or data-source identifier as --profile-key and initialize state. Example:

    python scripts/state_manager.py init --profile-key "<stable-key>" --database-id "<database-id>" --data-source-id "<data-source-id>" --database-name "<display-name>" --next-sequence 1 --property "title=Name" --property "source_url=Source URL"

Add other mapped roles, known authors, compact style fingerprints, and last-note metadata only when they already exist. State is written under ~/.codex/state/transfer-into-notion/ by default and must remain outside the skill checkout.

For existing video-transfer-notion users, the state helper accepts the legacy VIDEO_TRANSFER_NOTION_STATE_DIR and ~/.codex/state/video-transfer-notion/ location. Copy the verified legacy state to the new directory only when the user wants migration; keep the old directory as a backup until the new state passes check and show.

## Verify setup

Run python scripts/state_manager.py check, then show. Confirm the selected data-source ID, next sequence, and property map before creating the first note. If any mapping is uncertain, leave it unmapped and ask rather than guessing.
