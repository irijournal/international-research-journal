import { getCollection } from 'astro:content';
import settings from '../data/settings.json';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const when = (d) => {
  const t = new Date(`${d} UTC`);
  return Number.isNaN(t.getTime()) ? new Date() : t;
};

export async function GET({ site }) {
  const base = (site ?? new URL('https://internationalresearchinsights.com')).origin;
  const [articles, announcements] = await Promise.all([getCollection('articles'), getCollection('announcements')]);
  const items = [
    ...articles.map((a) => ({
      title: a.data.title,
      link: `${base}/articles/${a.id}`,
      date: when(a.data.publishedDate ?? ''),
      description: `${a.data.authors.join(', ')}. ${a.data.abstract}`,
      category: a.data.articleType,
    })),
    ...announcements.map((a) => ({
      title: a.data.title,
      link: `${base}/announcements/${a.id}`,
      date: when(a.data.date),
      description: a.data.summary,
      category: 'Announcement',
    })),
  ].sort((x, y) => y.date - x.date);

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>${esc(settings.journalTitle)}</title>
  <link>${base}/</link>
  <atom:link href="${base}/rss.xml" rel="self" type="application/rss+xml" />
  <description>${esc(settings.tagline)}. ISSN (Online) ${esc(settings.issnOnline)}.</description>
  <language>en-in</language>
${items
  .map(
    (i) => `  <item>
    <title>${esc(i.title)}</title>
    <link>${i.link}</link>
    <guid isPermaLink="true">${i.link}</guid>
    <pubDate>${i.date.toUTCString()}</pubDate>
    <category>${esc(i.category)}</category>
    <description>${esc(i.description)}</description>
  </item>`,
  )
  .join('\n')}
</channel>
</rss>`;

  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
