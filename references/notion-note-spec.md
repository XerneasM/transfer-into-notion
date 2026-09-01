# Notion multimodal-note specification

Read this file before drafting or writing every note.

## Destination and properties

Use the Notion data source selected during first-run setup. Healthy local state is authoritative for its IDs and semantic property map. Re-fetch the data source only when state is absent, older than 30 days, the user reports a schema change, or a write fails validation.

Populate mapped semantic roles when present; never assume these exact property names:

- title — note title; required by Notion and may be named 标题, Name, or something else.
- author — primary source author or creator.
- platform — source platform or container.
- source_url — canonical source link.
- content_type — use the database's existing equivalent for article, social post, document, video, audio, image, or other.
- timeliness — durability or version sensitivity.

Preserve automatic creation/update fields. Do not add new properties merely because a value could be useful. Do not move or reparent the database, the created record, or any unrelated page.

Use the title pattern:

NNN｜YYYY-MM-DD｜结论型简洁标题

- NNN is zero-padded and unique.
- The date is the primary source publication date, not the note creation date.
- If a mixed source has multiple dates, use the primary source date and record other dates inside the note.
- The final phrase should reveal the central conclusion, not repeat the source title.
- The finalized title is also the expected Codex task title after a successful Notion write.

Groupability should use the mapped author property and existing database views. Do not create separate author pages unless the current database already requires them.

### New author option handling

Treat a verified new primary author as routine record maintenance only when the mapped author property already has type `select` or `multi_select`:

1. If compact state lists the author, write the existing value normally. If the author is absent, fetch the current data-source schema immediately before changing it.
2. Append exactly one option whose name matches the source's verified primary author. Reconstruct the property definition with every existing option name and color unchanged; add the new author with one valid color, preferring an unused color when practical. Never rename, drop, reorder semantically, merge, or substitute existing authors.
3. Re-fetch or inspect the update response to confirm the old options remain and the new author exists, then create or update the note. Stop after one failed schema mutation and report the blocker; do not broaden or repeat the change speculatively.
4. This automatic exception does not apply to `person`, `relation`, `status`, formula, rollup, or ambiguously mapped properties. For those types, omit the optional author value or request authorization when the missing value blocks the user's required organization.

Do not create author pages, folders, relations, alternate author taxonomies, or options in any other property as part of this exception.

## Body order

Adapt detail to information density, but preserve this information hierarchy:

1. **核心结论** — a short callout stating the most reusable conclusion and applicable scenario.
2. **知识可视化图** — standard/deep mode only; immediately below the conclusion. Add 知识图设计风格 and a concise caption. Use more than one figure only when one would become crowded.
3. **来源与适用范围** — canonical source link, author, platform, publication date, source type, duration/page count/item count when relevant, timeliness, intended audience/scenario, evidence set, access limitations, and synthesis date.
4. **它解决了什么问题** — pain point, desired outcome, and overall approach.
5. **核心方法与判断依据** — workflow, comparisons, experiments, prompts, examples, and why each choice works. Use tables where repeated fields benefit from comparison.
6. **失败路径、边界与风险** — what did not work, common mistakes, what the method cannot replace, and version-sensitive assumptions.
7. **可直接复用的材料** — prompts, code, templates, parameters, checklists, or observation frameworks when genuinely present or clearly labeled as Codex synthesis.
8. **来源结构与证据索引** — choose exactly the structure that fits the primary source:
   - temporal media: 关键时间轴;
   - article or social thread: 关键论证链 or 小节地图;
   - PDF/document: 页码地图;
   - image/gallery: 视觉序列 or comparison matrix;
   - mixed-media page: 多模态证据索引.
9. **一句话复述与理解检查** — one-sentence restatement plus 3–5 questions that test comprehension rather than recall.
10. **复盘建议** — a time-boxed practice plan with actions, estimated time, deliverable, and an observable completion standard.
11. **延伸资源与补充行动** — conditional; include only when the source contains or genuinely requires consequential resources, evidence, capability building, tools, or outside actions. Omit the section when it would be empty or generic.

The exact subsection names inside 核心方法 may change to match the source. Do not force a short post or image into a bloated template. Do not force non-temporal sources into a fake timeline.

## Source structure patterns

### Temporal timeline

Use a table with 时间｜内容｜关键结论/用途. Make start times clickable only when the platform has verified stable deep links. Do not guess.

### Article argument chain

Use a table with 论证节点或小节｜证据/例子｜结论/用途. Link headings only when a stable section fragment is verified. It is valid to have no clickable section anchors.

### Document page map

Use a table with 页码｜小节/证据｜结论/用途. Say PDF p. N when PDF indexing differs from printed numbering. Mark OCR uncertainty.

### Visual sequence

Use panel/image order and a comparison matrix when the source communicates through composition, sequence, or contrast. Separate visible observation from interpretation.

### Multimodal evidence index

Use 来源位置｜模态｜支持的主张｜证据强度/限制. Include only modalities that add non-redundant information.

## Adaptive follow-up section

延伸资源与补充行动 covers useful dependencies outside the note rather than defaulting to software installation. Use only the item types supported by the source:

- knowledge resources such as books, papers, courses, concepts, or theories;
- reference works such as films, documentaries, websites, designs, or cases;
- data and evidence such as datasets, reports, interviews, benchmarks, or tests;
- capability building such as techniques, methods, or prerequisite knowledge;
- tools and environments such as apps, plugins, Skills, MCP servers, libraries, or services;
- outside actions such as observation, collection, experiments, consultation, or contacting a person or community.

Prefer one compact table with 项目｜类型｜与核心内容的关系｜建议动作｜优先级｜来源归属. Mark source ownership as 作者明确推荐, 作者提及但未推荐, or Codex 补充. Do not promote a passing mention into a recommendation.

Keep boundaries clear:

- 可直接复用的材料 contains source-supplied or clearly labeled synthesized prompts, code, templates, parameters, checklists, or observation frames.
- 复盘建议 turns the source's core method into practice and an observable output.
- 延伸资源与补充行动 records what must or could be obtained outside the source to deepen, verify, or execute it.

Read extension-resources.md only when this conditional section is needed. Installation evaluation is one subtype, not the default shape of the section.

## Evidence-visual placement

Use source visuals as evidence, not decoration. Place each immediately after the paragraph, step, or table row it clarifies.

Adapt the caption:

- video/audio frame: 截图 NN｜[00:00](verified-link)｜画面内容 — 知识点;
- article/webpage: 图证 NN｜小节名称｜图表或界面内容 — 知识点;
- PDF/document: 图证 NN｜p. 12｜图表内容 — 知识点;
- social thread: 图证 NN｜Post 3｜画面内容 — 知识点;
- image/gallery: 图证 NN｜Panel 4｜可见内容 — 解释边界;
- local file: 图证 NN｜filename + location｜内容 — 知识点.

Rules:

- Prefer a small representative set; zero visuals is correct when text alone supports the note.
- A visually argued source may need several images, but there is no quota.
- Preserve provenance and the original source. Crop only when meaning remains intact.
- Do not imply a user-provided image has an exact time, page, section, or post location when unknown.
- Avoid consecutive visuals that communicate the same point.
- Respect access controls and copyright; do not reproduce an article, deck, book, or image collection at length.

## Knowledge-map requirements

Before choosing a style, read the compact local style history rather than prior note bodies. Invent a new reference style whose design family, layout, palette, typography, and information organization are materially different from previous entries. Do not use prebuilt style templates or merely recolor a previous layout. Record the style name and a short fingerprint after the Notion write succeeds.

Read [knowledge-map-design.md](knowledge-map-design.md) before generating the visual. The declared style must be recognizable from the rendered image without relying on its caption. Pass schema/text validation, style-materialization audit, full-size visual review, and thumbnail review. Reject pastel rectangles joined by arrows, equal-weight card grids, or ornamental framing around an otherwise generic flowchart. Validation without visual review is incomplete.

The visual must:

- encode the source's central process, comparison, argument, decision structure, or multimodal relationship rather than merely decorate the page;
- remain readable at Notion page width;
- use concise Chinese labels and a clear hierarchy;
- avoid fabricated logos, screenshots, quotations, and metrics;
- use clean transparency only when guaranteed; otherwise use an opaque background suitable for Notion;
- be split into two or more visuals if legibility would otherwise suffer.

## Timeliness values

Use the database's existing option vocabulary. When an equivalent option exists, select it instead of creating a new one. Typical reasoning:

- 长期有效: principles and durable methods dominate.
- 阶段性（工具版本相关）: workflow remains useful but interfaces, models, pricing, commands, or availability may change.
- A more volatile existing option: the note depends strongly on a current service, policy, event, market value, or release.

## Review plan

The plan must convert reading into practice. Each step needs:

- a concrete action;
- a suggested duration;
- an output artifact;
- a completion criterion observable without rereading the note.

Prefer 60–120 minutes for standard notes, but adapt to the source. Do not prescribe installing a tool before completing the tool assessment.

## Codex task-title synchronization

After the Notion create/update and lightweight verification succeed:

1. Take the exact finalized title property, including NNN and YYYY-MM-DD.
2. Rename the calling Codex task with the task-title tool, omitting a thread/task ID so only the current task is targeted.
3. Do not create a new task, rename another task, or derive a shorter alternate title.
4. If the title tool is unavailable or fails, keep the verified Notion page, continue the state commit, and report the unsynchronized task title. Never retry by creating a duplicate note.

## Final QA before handoff

- Title number and primary publication date are correct.
- Core conclusion is conclusion-led and not a synopsis.
- Claims trace to the primary source, external verification, or are labeled synthesis.
- Knowledge map appears directly below the conclusion and its style is labeled.
- Evidence visuals are contextual, non-redundant, captioned, and source-appropriate; zero is acceptable.
- Source anchors are clickable only when reliably supported; no precision is invented.
- The selected timeline, argument chain, page map, visual sequence, or evidence index matches the source.
- Review steps produce an observable artifact.
- Consequential follow-up items have clear attribution and an appropriate next action; installable items receive a dated recommendation only when assessment is warranted.
- Canonical source URL and all available mapped Notion properties are populated.
- Verify the create/update response and query the finished row's title, properties, and source URL.
- The calling Codex task title matches the finalized Notion title, or the title-sync failure is explicitly reported.
- Do not full-fetch an image-heavy page unless a render problem, connector anomaly, or explicit deep-verification request requires it.
