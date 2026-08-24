---
name: transfer-into-notion
description: Analyze accessible URLs, local files, text, transcripts, images, audio, and video into conclusion-led multimodal learning notes in the user's chosen Notion knowledge database. Use for stateful transfer of articles, social posts or threads, webpages, PDFs, videos, podcasts, image-rich sources, and mixed-media links with evidence-aware structure, source-specific anchors, a newly designed knowledge map, executable review, and adaptive follow-up. Do not use for a plain summary that should not be written to Notion or for moving and restructuring existing Notion pages.
metadata:
  short-description: Transfer multimodal sources into structured Notion notes
---

# Transfer into Notion

Turn an accessible source into a trustworthy, reusable learning note and place it in the user's chosen Notion knowledge database. Accept text, images, audio, video, documents, social posts, and mixed-media pages. Preserve an established note system when one exists. Keep private per-user state outside the skill folder so the skill remains safe to publish and install from GitHub.

## Invocation input

Accept whatever the user provides: URL or local file, note number, screenshots or images, transcript/subtitles, pasted text, author, publication date, and special questions. Do not require fields that can be discovered reliably.

Default to **efficient standard mode** unless the user requests another mode:

- **Concise:** core conclusion, compact method, source structure, and action checklist; no knowledge-map image or broad external research unless requested.
- **Efficient standard:** complete note, one newly designed knowledge map, only the representative evidence visuals that improve understanding, a source-appropriate evidence index, review plan, and an adaptive follow-up section only when justified.
- **Deep:** chapter- or section-level analysis, multiple visuals when useful, richer evidence coverage, public-context cross-checking, and fuller evaluation of consequential follow-up resources.

Resolve every `scripts/...` and `references/...` path relative to the directory containing this `SKILL.md`, regardless of the current working directory.

## Required workflow

1. Run `python scripts/state_manager.py show` before querying Notion. When healthy state exists, use its data-source ID, semantic property map, next sequence, known authors, and compact style history; do not fetch prior note bodies or scan the full database. If no state exists, read [references/setup.md](references/setup.md) and perform its one-time bootstrap before drafting the note.
2. Query only the canonical current source URL to detect duplicates. Re-fetch the Notion data-source schema only when state is absent, older than 30 days, the user reports a schema change, or a write fails validation. Prefer Notion connectors/MCP; do not use Computer Use unless a connector cannot complete a necessary operation.
3. Classify the source as article/webpage, social post or thread, PDF/document, video, audio/podcast, image or gallery, mixed-media page, local file/bundle, or pasted material. Read [references/source-routing.md](references/source-routing.md) and follow only the relevant routes.
4. Establish a source-of-truth set from the accessible primary content and user-provided material. A title, thumbnail, social preview, search snippet, or generated summary alone is never enough. Inventory the modalities actually available and keep their roles distinct.
5. If access is blocked by DRM, permissions, expiry, login state, robots rules, or extraction limits, try available non-screen-blocking methods first. Continue from user-provided text, transcript, file, subtitles, screenshots, or images when they provide sufficient evidence; otherwise stop before drafting and request the missing material. Never fill gaps from metadata or pretend that only one platform is supported.
6. Separate three evidence lanes where relevant: **source author's claim**, **external verification**, and **Codex synthesis**. Treat comments, reposts, quoted posts, replies, linked pages, and embedded media as separate sources unless the primary author explicitly incorporates them. Do not invent timestamps, quotations, page numbers, section anchors, metadata, comments, or tool behavior.
7. Extract the thesis, problem, method, decision logic, examples, failure paths, boundaries, and executable practice. Prefer synthesis over retelling or transcript-like compression.
8. Build the note using [references/notion-note-spec.md](references/notion-note-spec.md). Read that reference before drafting or writing every note. Choose the source structure that fits: time-based timeline, article argument chain, document page map, gallery sequence, or multimodal evidence index.
9. Detect follow-up items that materially help the user understand, verify, or apply the source: knowledge resources, reference works, data or evidence, capability gaps, installable tools, and concrete outside actions. Preserve whether each item was **explicitly recommended by the author**, **mentioned without recommendation**, or **added by Codex as synthesis**. If at least one consequential item exists—or the user requests enrichment—read [references/extension-resources.md](references/extension-resources.md), include only the relevant item types, and omit the entire section otherwise.
10. Create a knowledge visualization in efficient standard/deep mode. Invent a real reference style whose family, layout, palette, and visual language are materially different from the compact style history. Do not use prebuilt style templates. Label the style and briefly explain its visual traits. For crisp SVG with less generated markup, run `python scripts/render_knowledge_map.py schema`, create a concise declarative JSON spec, then run `render` and `validate`; the renderer is style-neutral.
11. Select evidence visuals for explanatory value, not completeness. Place each next to the claim or step it supports, label its source location and significance, and preserve provenance. Use stable deep links, section links, or page references only when verified. A text article may need no source screenshots; a visually argued source may need several. Never use a fixed screenshot quota or dump all visuals at the end.
12. When the user asks to transfer or record the note, write it directly to the data source selected in local state. If the same canonical source URL already exists, update that record instead of creating a duplicate. When the verified primary author is absent from an existing mapped `select` or `multi_select` author property, automatically append exactly that author option before writing; preserve every existing option and color, verify the updated schema, and never substitute a different known author. This single-option maintenance is the only automatic schema exception. Do not create a database, properties, views, page hierarchy, author pages or folders, unrelated options or categories, or move/reparent existing Notion content without explicit authorization.
13. Verify the create/update response and run a lightweight data-source query for title, properties, canonical source URL, expected evidence-image count, and expected source-anchor count. For non-temporal sources, zero timestamp links is correct. Do not full-fetch an image-heavy page by default because signed attachment URLs inflate context. Full-fetch only after a reported render problem, a connector anomaly, or an explicit deep-verification request.
14. After the Notion write is verified, rename the calling Codex task to the exact finalized Notion title when a task-title tool is available. Target the calling task; do not create a new task or rename another task. A title-sync failure is non-fatal: report it, continue state commit, and never duplicate or roll back the Notion page.
15. Only after the Notion write and lightweight verification succeed, commit the sequence, author, source, page, and style with `python scripts/state_manager.py commit-note ...`. If the state commit fails, preserve the Notion result and report that state needs repair; never create a duplicate to compensate.

## Local state

`scripts/state_manager.py` stores private state in `~/.codex/state/transfer-into-notion/` by default, or `TRANSFER_INTO_NOTION_STATE_DIR` when set. For backward compatibility it can read the legacy `VIDEO_TRANSFER_NOTION_STATE_DIR` and `~/.codex/state/video-transfer-notion/` location. State is outside the skill folder and must never be committed or packaged.

- `show` returns only the compact fields needed for the current note.
- On first use, follow `references/setup.md`: select an existing data source with the user, map semantic roles to its real property names, inspect only compact prior-note metadata, then run `init`. Do not store note bodies, source content, transcripts, credentials, or attachment URLs.
- Use a stable data-source or workspace identifier as `--profile-key`; profiles isolate multiple Notion workspaces.
- `commit-note` writes atomically and keeps a backup. `repair` rebuilds state from a small manually reconstructed snapshot when state is missing or inconsistent.
- If state cannot be written, continue in stateless fallback mode after one lightweight Notion lookup and tell the user. Do not weaken filesystem permissions or write inside the GitHub checkout.

## Efficiency rules

- Prefer a fresh Codex task for each source so unrelated conversation history is not retained.
- Reuse already fetched source metadata and extracted content within the task.
- Analyze long text, transcripts, documents, and media in meaningful batches. Sample frames around transitions instead of treating every frame as input.
- Use user-provided source files and visuals before generating redundant captures.
- Follow only linked sources that are necessary to understand, verify, or act on the central claim; do not recursively summarize the open web.
- Keep external research proportional. Merely naming a book, film, concept, or tool does not justify broad browsing; verify only what changes understanding or action.
- Reuse known canonical official URLs, but open current pages for ambiguous identity, availability, version-sensitive claims, data freshness, cost, permissions, or safety. Use comments and community reports only when they change a practical decision.
- Do not generate a knowledge map until the written synthesis is stable.
- Prefer one complete Notion write followed by one lightweight property query over many edits or a full page fetch.

## Reliability boundaries

- Use the source publication date—not the note creation date—in the title. If a mixed source has multiple dates, use the primary source's date and record the rest inside the note.
- If sequence number is omitted, use local state or infer the next available zero-padded number from the selected data source; never overwrite a conflicting entry.
- Mark uncertain facts as `待确认` or omit them. State when timestamps, section boundaries, page references, authorship, or dates are approximate.
- Treat version-sensitive guidance, datasets, availability, costs, and tool behavior as time-bounded and record the evaluation date when verified.
- Respect access controls and copyright. Synthesize; do not reproduce an article, transcript, book chapter, paywalled page, or image collection at length. Use only short quotations and the minimum source visuals needed for evidence.
- Writing to Notion is allowed only when the user's request asks to create, transfer, record, or update the note. A request to review or draft alone is read-only.
- Preserve unrelated Notion content and hierarchy. A transfer request authorizes adding one verified primary-author option only when the mapped author property is already `select` or `multi_select`; read [references/notion-note-spec.md](references/notion-note-spec.md) for the guarded procedure. Deletion, moving/reparenting pages, every other database schema change, installation, deployment, account changes, or paid purchases require separate explicit authorization.
