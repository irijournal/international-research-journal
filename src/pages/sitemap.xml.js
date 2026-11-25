import { getCollection } from 'astro:content';

export async function GET({ site }) {
  const base = (site ?? new URL('https://example.org')).origin;
  const [pages, articles, issues, announcements, sections] = await Promise.all([
    getCollection('pages'),
    getCollection('articles'),
    getCollection('issues'),
    getCollection('announcements'),
    getCollection('sections'),
  ]);

  const iso = (d) => {
    const t = new Date(`${d} UTC`);
    return Number.isNaN(t.getTime()) ? undefined : t.toISOString().slice(0, 10);
  };
  const lastmod = new Map([
    ...pages.map((p) => [`/${p.id}`, iso(p.data.updated)]),
    ...articles.map((a) => [`/articles/${a.id}`, iso(a.data.publishedDate ?? '')]),
    ...announcements.map((a) => [`/announcements/${a.id}`, iso(a.data.date)]),
  ]);
  const urls = [
    '/',
    '/current',
    '/archives',
    '/sections',
    '/announcements',
    '/editorial-board',
    ...pages.map((p) => `/${p.id}`),
    ...articles.map((a) => `/articles/${a.id}`),
    ...issues.map((i) => `/archives/${i.id}`),
    ...announcements.map((a) => `/announcements/${a.id}`),
    ...sections.map((s) => `/sections/${s.id}`),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `  <url><loc>${base}${url}</loc>${lastmod.get(url) ? `<lastmod>${lastmod.get(url)}</lastmod>` : ''}</url>`).join('\n')}
</urlset>`;

  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
