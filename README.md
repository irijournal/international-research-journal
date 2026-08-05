# International Research Insights: Multidisciplinary e-Journal

The complete website for the journal: front end, content, editorial policies, search, sitemap and a browser based CMS. Built with Astro. Hosted free on GitHub Pages with a domain from GoDaddy and no hosting plan.

## Start here

| Document | What it covers |
| --- | --- |
| `docs/DEPLOY.md` | Getting the site live on GitHub Pages with the GoDaddy domain, connecting the CMS, and turning on the contact form |
| `docs/CMS-GUIDE.md` | Running the journal day to day without touching code |
| `docs/ISSN-CHECKLIST.md` | What the ISSN National Centre requires and the order to do it in |
| `docs/sample-article.md` | The shape of an article file, field by field |

## What is on the site

Home, current issue, archives by volume and issue, article pages with abstracts and citation blocks, seven research sections, editorial board, announcements, site search, and thirteen written policy pages: about, submission guidelines, author declaration, peer review, publication ethics, plagiarism, copyright and licensing, self archiving, for reviewers, terms, indexing and preservation, open access and charges, privacy, contact and disclaimer.

Every page is written in full. There are no placeholders and no dead links.

## How it is put together

```
src/data/settings.json     Journal title, domain, emails, ISSN, frequency, licence. One file, whole site follows.
src/content/articles/      One markdown file per article
src/content/issues/        One file per issue, its body is the editorial note
src/content/board/         One file per board member
src/content/sections/      One file per research section
src/content/announcements/ One file per notice
src/content/pages/         Every policy and information page
src/components/            Header, footer, page head, issue view, contact form
src/layouts/Base.astro     HTML shell, metadata, fonts, structured data
src/pages/                 Routes, built from the content above
src/styles/global.css      Design tokens and all styling
.pages.yml                 CMS field definitions
.github/workflows/         Build and deploy on every commit
```

The navigation, the footer, the search index and the sitemap all build themselves from the content collections. Adding a page or a section puts it in the menu with no code change.

## Design

Deep teal `#134e4a`, dark teal `#042f2e`, bright teal accent `#14b8a6`, soft tint `#f0f7f6` on white. Playfair Display for headings, Inter for body text, Lato for labels. The palette and type follow the INSIGHTS house identity.

Change any token in `src/styles/global.css` and the whole site follows.

## Running it locally

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # writes dist/
```

Node 18.20 or newer is required.

## Known and intended

The build prints a note that the articles collection is empty. That is correct: no article has been published yet. The note disappears the moment the first article is added, and nothing on the site is broken by it. Until then, issue pages show the call for submissions instead of a table of contents, which is the honest state of a journal that has just opened.

## Before launch

1. Set the real domain in `astro.config.mjs`, `public/CNAME` and `src/data/settings.json`.
2. Add the official institutional email address of each board member, which the ISSN application requires.
3. Confirm the editorial office postal address.
4. Have the Editor in Chief read the founding editorial note and the policy pages, and adjust the wording to his own voice where he wants to.
5. Decide the mailbox arrangement for the journal addresses, and test that mail actually arrives.
