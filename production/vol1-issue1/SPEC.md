# Volume 1, Issue 1 (September 2026) — production spec

Everyone working on this issue reads this file first. `issue.yaml` (same folder) holds all metadata values.
Paths below are relative to the issue folder:
`/tmp/claude-0/-home-user-international-research-journal/55c29a40-3aee-5b96-9c75-9672107bc1f3/scratchpad/issue/`
(written `$ISSUE` below). The scratchpad root is its parent (`$SP`). The website repository is
`/home/user/international-research-journal` (branch `issue-1-september-2026`, Astro 5 site; `npm run build` builds it).

## What the journal owner asked for

1. Four manuscripts (Word files) are to be formatted the way the reference paper (Chanchal Khatri, published in the
   journal *Research Ambition*, Vol. 11, Issue I, May 2026) is formatted, but branded for **our** journal,
   *International Research Insights: Multidisciplinary e-Journal*, using our logo.
2. They form **Volume 1, Issue 1, September 2026** (period July–September 2026). This is the founding issue needed for
   the ISSN application to the ISSN National Centre for India (NSL, CSIR-NIScPR).
3. Upload everything to the website (article pages, PDFs, current issue, archive, index/contents table).
4. One consolidated issue PDF (cover page, front matter, contents, all articles) suitable for printing.
5. Everything in English, properly formatted, every heading consistent.
6. The journal is **online only** (digital). It is NOT published in print. Any earlier "print and online" wording on the
   website must go back to online only.
7. Flag anything dubious.

## Source files ($SP)

| Slug | Source docx | Pandoc markdown | LibreOffice PDF render of the original |
|---|---|---|---|
| case-pendency-indian-high-courts | `src/p1_case_pendency.docx` | `md/p1_case_pendency.md` | `pdf/p1_case_pendency.pdf` |
| stress-among-bsc-nursing-students-guwahati | `src/p2_stress_nursing.docx` | `md/p2_stress_nursing.md` (images in `md/media_p2_stress_nursing/media/`) | `pdf/p2_stress_nursing.pdf` |
| patient-safety-knowledge-skills-practice-nursing-students | `src/p3_patient_safety.docx` | `md/p3_patient_safety.md` (images in `md/media_p3_patient_safety/media/`) | `pdf/p3_patient_safety.pdf` |
| neuropsychiatric-disorders-comprehensive-overview | `src/p4_neuropsychiatric.docx` | `md/p4_neuropsychiatric.md` | `pdf/p4_neuropsychiatric.pdf` |

Reference layout: `src/ref_khatri.docx`, rendered `pdf/ref_khatri.pdf`, page images `png/khatri-*.png`, `png/k90-1.png`.
Reference issue index (contents table): `src/ref_index.docx`, `pdf/ref_index.pdf`, `png/index-1.png`.
The reference paper is ONLY a layout model. It is already published elsewhere and must NOT be included in our issue.

Notes on sources:
- p1 contains ~10 native Word charts (`word/charts/chartN.xml`, data cached in the XML and in `word/embeddings/*.xlsx`).
  Pandoc does not extract them. Re-draw each with matplotlib from the cached chart data (same chart type, categories,
  series, values, axis titles, chart title), or crop from the LibreOffice render if a chart cannot be parsed.
- p1 also contains web-paste artifacts ("Top of Form", "Bottom of Form").
- p4 contains a diagram drawn with Word shapes (Venn-style "structures of the clinical manifestations of cerebral
  disorders"). Pandoc loses it. Re-create it as a clean PNG (matplotlib) with the same text, or crop it from the render.
- p2 and p3 contain chart images (png/jpeg) and real Word tables.

## Known author details (from the journal's own editorial board records; use only if the paper itself lacks them)

- Dr. Ravi Kumar — Editor in Chief of this journal. Ph.D. (Law). Head of Department, Indraprastha Law College,
  Greater Noida, Uttar Pradesh, India.
- Dr. Ramavatar Singh Tyagi — Managing Editor of this journal. Ph.D. (Nursing). Vice Principal, Department of Nursing,
  J.S. University, Shikohabad, Uttar Pradesh, India.
No emails or ORCIDs are known for them. Never invent an email, ORCID, affiliation, date or DOI.

## Canonical cleaned paper format: `$ISSUE/papers/<slug>/paper.md`

Pandoc markdown with YAML front matter. Figures in `$ISSUE/papers/<slug>/fig/` (PNG, ≥ 1600 px wide for charts,
white background), referenced relatively as `fig/fig1.png`.

```yaml
---
slug: case-pendency-indian-high-courts
title: "Title in Title Case (no trailing full stop)"
short_title: "Short running head, max ~60 characters"
article_type: "Research Article"        # or "Review Article", from issue.yaml
section: "Law and Constitutional Studies"   # from issue.yaml
authors:
  - name: "Dr. Ravi Kumar"
    affiliations: ["a"]
    corresponding: true                 # exactly one corresponding author per paper (the first author unless the source says otherwise)
    email: ""                           # only if present in the source
    orcid: ""                           # only if present in the source
    degree: "Ph.D. (Law)"               # if the source gives one
affiliations:
  - id: "a"
    text: "Head of Department, Indraprastha Law College, Greater Noida, Uttar Pradesh, India"
keywords: ["Case Pendency", "High Courts", "..."]   # from the source, cleaned, 4–10 items, consistent capitalisation
abstract: |
  First paragraph...

  Second paragraph... (structured abstracts keep labels as **Background:** etc.)
received: ""      # only if stated in the source
accepted: ""
---
```

Body rules:
- Headings: `## Heading` for main sections, `### Subheading`, `#### Minor` (rare). Unnumbered. Title Case for `##`,
  Sentence case is fine for `###`. Do not repeat the title, authors, abstract or keywords in the body.
- Standard order: Introduction … (Methods / Results / Discussion as the paper has them) … Conclusion, then any
  Suggestions / Recommendations / Limitations, then Acknowledgements / Declarations only if the source has them,
  then `## References` last.
- Paragraphs: plain text, no hard line breaks inside a paragraph.
- Lists: `-` or `1.` markdown lists.
- Tables: pandoc pipe tables (or grid tables if a cell needs multiple lines), each with a caption line directly above:
  `Table: Table 1. Distribution of students by age (N = 42)`. Number tables consecutively from 1.
  Keep every number exactly as in the source. Put a table's source note (if any) as a paragraph right after it,
  starting `*Source:*`.
- Figures: a paragraph containing only `![Figure 1. Caption text](fig/fig1.png)`. Number consecutively.
  Every figure must be referred to in the text or have a caption that stands alone.
- In-text citations: keep the author's style (author–year or numbers). Superscript reference numbers as `^1^`.
- References: `## References`, then one entry per list item (`1.` numbered if the paper uses numeric citations,
  otherwise `-` bullets in alphabetical order as the source gives them). Clean punctuation/spacing/italics only.
  Do not invent missing details. Remove duplicates only if they are exact duplicates (record it).

## Copy-editing policy (light, transparent)

Do:
- Fix spelling, typos, obvious grammar, punctuation, spacing, capitalisation, heading names
  (e.g. "REFERANCES" → "References", "SSUMPTIONS" → "Assumptions"), inconsistent abbreviations (B.Sc.),
  numbering of tables/figures, stray artifacts (Top of Form, Bottom of Form, empty headings, page numbers, field codes).
- Normalise ALL-CAPS headings to Title Case.
- Where wording is garbled but the intended meaning is unambiguous (e.g. paraphrasing-tool "tortured phrases" such as
  "maniacal clutters" for "manic disorders"), correct it to the standard term AND record it in the report as a
  `plagiarism_signal` flag with original and corrected text.

Do not:
- Change meaning, data, numbers, claims, conclusions, or the authors' argument.
- Add content (no new paragraphs, no invented declarations, ethics statements, funding statements, dates, emails).
- Delete substantive content. Proposal-style or redundant sections stay, but are flagged with a recommendation.

Record every non-trivial change (anything beyond pure typo/spacing fixes) in `report.json`.

## Report: `$ISSUE/papers/<slug>/report.json`

```json
{
  "slug": "...",
  "title": "...",
  "authors": [{"name": "...", "affiliation": "...", "email": "..."}],
  "counts": {"words_body": 0, "tables": 0, "figures": 0, "references": 0},
  "changes": [{"type": "heading|language|structure|table|figure|reference|artifact", "location": "...", "original": "...", "revised": "..."}],
  "flags": [{"severity": "high|medium|low", "category": "plagiarism_signal|prior_publication|missing_info|data_inconsistency|ethics|citation|structure|figure|conflict_of_interest|other", "detail": "..."}]
}
```

Things to check and flag: citations in text with no reference entry and vice versa; numbers in text that disagree
with tables; percentages that do not add up; sample size inconsistencies; missing ethics approval / informed consent
statements for studies on human participants; missing affiliation/email; any sign the paper was already published
(journal headers, DOIs, "published in", old dates); paraphrasing-tool language; copied web text; references that look
fabricated (e.g. impossible years, mismatched volumes) — flag only, do not remove.

## Typesetting (article PDFs and the full issue PDF)

Built by a Python pipeline in `$ISSUE/build/` (entry point `$ISSUE/build/build.py`), outputs in `$ISSUE/out/`.
HTML + CSS rendered by Chromium through Playwright (Node package already installed at `$SP/shot/node_modules/playwright`;
launch with `executablePath: '/opt/pw-browsers/chromium'`, never run `playwright install`), then running headers,
footers and page numbers stamped onto every page with reportlab + pypdf so that page numbers run continuously across
the issue. pandoc converts `paper.md` to HTML. Fonts installed locally: Liberation Serif (Times-compatible body),
Caladea (Cambria-compatible headings), Carlito, Inter. Do not depend on internet fonts.

Article layout — follow the reference (`png/k90-1.png`, `png/sheet_khatri.png`), branded for our journal:
- A4. First page header block: emblem (left), a bordered box in the centre with
  "International Research Insights" (large, bold, navy), "A Multidisciplinary e-Journal", "(Peer-reviewed, Open Access)",
  "Journal home page: www.internationalresearchinsights.com", the ISSN line from issue.yaml (or nothing),
  "Vol. 1, Issue 1, September 2026" in blue; at right a small thumbnail of our issue cover. Then a thick navy rule.
- Title centred, bold, uppercase, navy. Authors bold with superscript affiliation letters, `*` for the corresponding
  author. Affiliations in italics.
- KEYWORDS | ABSTRACT block: two columns (≈30% / 70%) with ruled top, header and bottom lines, like the reference.
- Body in two justified columns with hyphenation; bold navy section headings; tables with booktabs-style rules, header
  row tinted, caption above ("Table 1." bold); figures with caption below ("Figure 1." bold). Wide tables/figures span
  both columns. Tables never overflow the page.
- Running header from page 2: author name(s) left, short title right (italic, blue), thin rule.
  Footer on every page: "International Research Insights: Multidisciplinary e-Journal" left, "Vol. 1, Issue 1,
  September 2026" right, page number centred (continuous across the issue).
- First-page footnote area: `*Corresponding author:` name and e-mail (if known); "Published online: <date from
  issue.yaml>" (received/accepted only if known); "© 2026 The Author(s). Published by International Research Insights
  Editorial Board. This is an open access article under the CC BY 4.0 licence." and the article URL
  `https://internationalresearchinsights.com/articles/<slug>`.
- "How to cite" line at the end of the article (before References): Authors (2026). Title. *International Research
  Insights: Multidisciplinary e-Journal*, 1(1), first–last. URL.
- References in two columns, smaller type, hanging indent. End-of-article marker `* * * * *`.
- Each article starts on a new page.

Full issue PDF (`$ISSUE/out/<full_issue_pdf_name>`) — front matter in roman page numbers, articles from page 1:
1. Front cover (no page number): full logo, title, subtitle, descriptor line, "Volume 1 · Issue 1 · July–September
   2026", ISSN line (from issue.yaml), the contents (article titles + authors), publisher name and address, website.
   Navy/blue design, print-safe, A4.
2. Journal information / imprint page: title, type (Journal), subject, frequency, language, format (Online),
   starting year, publisher + address, place of publication, editor in chief, contact e-mails, website, licence,
   review model, access model, disclaimer ("Views expressed are those of the authors..."), copyright notice.
3. Editorial board page: every member from the website's board records (`src/content/board/*.md` in the repo) with
   role, name, qualification, designation, department, institution, address, e-mail, profile — whatever is present.
4. Contents / Index: table with S.No., Title, Author(s), Section, Article type, Page No. (like `png/index-1.png`).
5. Editorial note from the Editor in Chief (body of `src/content/issues/volume-1-issue-1.md` in the repo).
6. The articles.
7. Back matter: a "Call for Papers" page for Volume 1, Issue 2 (December 2026) using issue.yaml next_issue, with the
   submission e-mail and website, then a back cover (logo, website, publisher address).

Also output: `$ISSUE/out/articles/<slug>.pdf` (each article alone, same page numbers as in the full issue),
`$ISSUE/out/cover.png` (front cover, ~1240 px wide) and `$ISSUE/out/cover-thumb.png` (~300 px wide),
`$ISSUE/out/pages.json` = `{"<slug>": {"first": 1, "last": 14}, ...}` plus front-matter page counts.

## Website

Repository `/home/user/international-research-journal`, branch `issue-1-september-2026`. Astro content collections
in `src/content/`, site settings in `src/data/settings.json`, helpers in `src/lib/site.ts`, CMS field definitions in
`.pages.yml`. Article files go in `src/content/articles/<slug>.md` (schema in `src/content.config.ts`).
Public files in `public/` (served from `/`). Issue files under `public/uploads/vol1-issue1/`.
