# Permission-adaptive evidence routing

Read this file before collecting source evidence. Its purpose is to choose a trustworthy path that fits the user's available and authorized permissions without turning technical access into broader authority.

## Core rule

Use the lowest tier that can support the note's central claims. Escalate only when the current tier is insufficient and the next tier is both available and already authorized. A permission profile describes what the environment can technically do; it does not authorize unrelated files, hidden credentials, new accounts, purchases, software installation, external communication, DRM/paywall bypass, or a broader task.

## Tier matrix

| Tier | Available evidence and actions | Preferred uses | Hard boundaries |
|---|---|---|---|
| 1 — Public or supplied | Public webpages and files, official public transcripts/captions, connected-source text, user-provided text/files/screenshots/audio/video | Most articles, public PDFs, pasted material, sources with adequate official captions | Do not draft from title, thumbnail, snippet, or metadata alone |
| 2 — Approved signed-in browser | Visible authenticated page state, official captions exposed in the UI, normal platform downloads, visible metadata, representative screenshots | Login-gated articles, social posts, videos with captions available only to the signed-in user | Do not read/export cookies, tokens, password stores, local storage secrets, or hidden credentials; do not bypass access controls |
| 3 — Approved full local processing | Shell/filesystem tools applied to media already legitimately available to the user; local transcription, OCR, document extraction, frame sampling, checksum/metadata inspection | Videos without adequate captions, scanned files, audio, large local bundles, format conversion | Use existing tools first; package installation needs separate authorization unless already explicitly granted; do not inspect unrelated files or broaden scope |

## Escalation ladder

1. Inventory source modalities and the current permission profile.
2. Test Tier 1 once using the primary source or user-supplied artifacts.
3. If evidence is insufficient, use Tier 2 only when a signed-in browser session is available and the task requires it.
4. If the user can normally view or download the media but captions/text remain insufficient, use Tier 3 when full local processing is available and authorized.
5. Stop escalating as soon as the thesis, method, examples, boundaries, and source structure are adequately evidenced.
6. If the next tier is unavailable or would need new authorization, ask for the smallest alternative: transcript, exported file, screenshot set, audio/video file, or permission change.
7. Record the route and limitations in 来源与适用范围.

Do not retry the same blocked method repeatedly. Do not ask the user to change permissions when a lower-tier route already supplies adequate evidence.

## Route recipes

### Article or social post

- Tier 1: read the public body/thread and essential quoted context.
- Tier 2: use the signed-in browser for content that the user can see but public extraction cannot access.
- Tier 3: use a user-approved local export, print/PDF, OCR, or attachment extraction when browser text remains incomplete.

### PDF or document

- Tier 1: use the public or supplied file with stable page numbering.
- Tier 2: use the signed-in browser's normal download/export path when the document is available only after login.
- Tier 3: extract text, render pages, and run OCR locally; verify consequential names, numbers, and quotations against page images.

### Video or audio

- Tier 1: prefer official transcript/captions, then a user-supplied transcript or media file.
- Tier 2: use the approved signed-in player for captions, visible metadata, normal downloads, and representative frames. If a caption control is visible but the caption data is not publicly exposed, treat that as a Tier 2 source rather than declaring the video unsupported.
- Tier 3: when normal playback/download is permitted and the page has already delivered the media to the user, download or process that media locally for transcription and frame sampling. Preserve the canonical page as provenance. Do not export cookies or circumvent DRM; do not treat a signed playback URL as reusable public evidence.
- Label the transcript as official, user-supplied, or locally generated. Recheck important product names, commands, numbers, and quotations against audio or frames.

### Image or gallery

- Tier 1: use original supplied/public images and captions.
- Tier 2: use signed-in browser screenshots only when they preserve inaccessible ordering, layout, or provenance.
- Tier 3: use local OCR/cropping only when it improves legibility without changing meaning; keep originals and panel order.

## Local-processing hygiene

- Prefer capabilities already present in the environment.
- If a missing dependency is necessary, explain why and obtain installation authorization unless the user already granted it explicitly.
- Store downloads and derived artifacts in an explicit task/workspace temporary directory, never in the skill repository or private-state directory.
- Track which files the run created. Cleanup may remove only those files after the Notion write is verified; preserve user-provided originals and any artifact the user asks to keep.
- Never place transcripts, source media, signed URLs, credentials, local paths, or private Notion identifiers in the published skill.

## Completion test

Before drafting, confirm:

- the evidence route is sufficient for the central claims;
- access limitations are recorded without overstating certainty;
- metadata, transcript, visuals, and external checks remain distinct evidence lanes;
- no higher permission tier was used merely because it was available;
- no action exceeded the source, destination, or authority granted by the user.
