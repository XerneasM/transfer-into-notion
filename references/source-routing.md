# Source routing and multimodal evidence

Read this file after classifying the input. Follow only the relevant routes. The goal is sufficient primary evidence, not exhaustive extraction.

## Shared intake

1. Identify the canonical source and record the provided URL unchanged.
2. Resolve redirects and remove tracking parameters only when doing so cannot change the represented item, language, edition, timestamp, or access path.
3. Inventory the available modalities: body text, captions, tables, images, audio, video, transcript, attachments, quoted or embedded sources, and user notes.
4. Choose one primary source. Treat linked, quoted, embedded, replied-to, or externally verified material as separate evidence unless the primary author explicitly incorporates it.
5. Record access limitations. A search snippet, social preview, thumbnail, generated summary, or title is metadata, not enough evidence for a note.

## Route matrix

| Source kind | Minimum trustworthy evidence | Useful structure | Evidence visuals |
|---|---|---|---|
| Article or webpage | Accessible main body plus title, author when available, publication date or explicit uncertainty, and canonical URL | Argument chain or section map | Only diagrams, figures, tables, or layout details that change understanding |
| Social post or thread | Full primary post/thread and essential quoted or replied-to context | Post sequence or argument chain | Post screenshots only when layout, images, or provenance matters |
| PDF or document | Extracted text for relevant pages plus stable page numbering | Page map or section map | Figures/tables with page labels |
| Video | Video or sufficient transcript/subtitles plus metadata; sample frames around meaningful transitions | Clickable timeline | Representative frames near supported claims |
| Audio or podcast | Audio or sufficient transcript plus metadata; chapters when reliable | Clickable timeline or topic sequence | Cover art rarely; diagrams only when supplied elsewhere |
| Image or gallery | Original images plus captions, ordering, and available creator/date context | Visual sequence or comparison matrix | The source images or justified crops are the evidence |
| Mixed-media page | Inventory of each component and a sufficient primary-content lane | Multimodal evidence index | Only components that carry unique information |
| Local file or bundle | The supplied files and their internal metadata/content | Match the contained source types | Preserve local provenance and file order |
| Pasted material | The pasted content plus user-supplied provenance | Match the content's natural structure | Use only user-provided images |

## Route-specific rules

### Article, webpage, newsletter, or blog post

- Extract the complete argument needed for the note, not navigation, ads, unrelated recommendations, or comments.
- Preserve heading order when it represents the reasoning, but synthesize instead of recreating the article.
- Use an **argument chain** with section or claim, evidence/example, and conclusion/use.
- Link a section only when a stable heading or fragment URL is verified. Otherwise name the section without fabricating an anchor.
- Source screenshots are optional. Prefer the article's original figure or table when it materially supports a claim; do not screenshot ordinary paragraphs merely to prove they exist.
- Keep quotations short and necessary. Paraphrase the rest.

### Social post, long post, or thread

- Determine thread boundaries and primary authorship. Do not silently merge replies, quote-posts, comments, or community notes into the author's position.
- Preserve post order when it carries the reasoning. Collapse repeated promotion, reaction, and engagement prompts.
- If a post points to a long-form article, use the long-form source as primary when accessible and retain the post as discovery context.
- Record deleted, unavailable, or truncated posts as gaps. Do not infer their content.
- Use screenshots when images, layout, or post identity matters; otherwise text and links are enough.

### PDF, slide deck, report, paper, or document

- Use the file's printed page number when visible; otherwise use the PDF page index and label it as such.
- Distinguish body claims, captions, footnotes, appendices, and references.
- Tables and charts require nearby labels, units, legends, and scope. Do not summarize a chart from shape alone.
- Build a **page map** with page, section/evidence, and conclusion/use.
- For scanned documents, note OCR uncertainty and verify important names, numbers, and quotations against the page image.

### Video

- Prefer supplied or platform transcripts/subtitles, then audio transcription, while checking important claims against the video.
- Sample frames around topic or scene transitions. Do not treat every frame as evidence.
- Use verified native timestamp links. Canonical Bilibili URLs use t=<whole-seconds>; YouTube uses t=<whole-seconds>s. Preserve existing query parameters.
- When exact deep linking is unavailable, link the timestamp to the source and label the jump as non-exact.
- Do not infer on-screen text, code, or diagrams from transcript alone.

### Audio or podcast

- Use transcript or transcription when sufficient; verify names, numbers, quotations, and ambiguous speaker turns against audio when consequential.
- Distinguish host, guest, advertisement, inserted clip, and listener question.
- Use chapters or timestamps only when observed or derived from the audio; label approximate timing.
- A cover image is metadata, not evidence of the spoken argument.

### Image, carousel, comic, infographic, or gallery

- Preserve item order, captions, creator credit, and the relationship between panels.
- Describe visible evidence before interpreting it. Separate observation from inference.
- Do not infer off-frame events, hidden text, identity, location, or intent without support.
- Crop only to focus attention without changing meaning; retain a link or reference to the original item.
- Use a **visual sequence** or comparison matrix rather than forcing a timeline.

### Mixed-media page

- List each component and assign its role: primary claim, supporting evidence, demonstration, navigation, promotion, or external reference.
- Choose the dominant structure from the primary lane. Add a **multimodal evidence index** only when different modalities carry non-redundant information.
- Reconcile conflicts explicitly: text may say one thing while a chart, image, or demonstration shows another.
- Do not recursively follow every embedded or related link. Open only what is necessary to understand, verify, or apply the central claim.

## Access and fallback

Try the least intrusive trustworthy path:

1. Direct source content or downloadable file.
2. Official transcript, captions, reader view, print/PDF view, or accessible mirror that preserves provenance.
3. Approved signed-in browser session.
4. User-provided text, transcript, file, screenshots, or images.

Stop before drafting when the remaining material cannot support the central claims. Ask for the smallest missing artifact. Never bypass access controls, DRM, paywalls, or permissions.

## Multimodal reconciliation

For each central claim, record which modality supports it:

- text or transcript states the claim;
- figure, table, screenshot, audio, or video demonstrates it;
- metadata establishes author, date, platform, or sequence;
- external verification confirms or challenges it;
- Codex synthesis connects the evidence into a reusable model.

When modalities conflict, preserve the conflict and lower confidence. Do not average contradictory evidence into a stronger claim.

## Source-location labels

Use only verified locations:

- video/audio: [00:00](verified-deep-link);
- PDF/document: p. 12 or PDF p. 12 when printed numbering differs;
- article: heading or section name, optionally linked to a verified fragment;
- social thread: post number or stable post link;
- gallery: image/panel number;
- local bundle: filename plus page, sheet, slide, timestamp, or panel when available.

If exact location is unavailable, state that plainly instead of inventing precision.
