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

  const urls = [
    '/',
    '/current',
    '/archives',
    '/sections',
    '/announcements',
    '/editorial-board',
    '/search',
    ...pages.map((p) => `/${p.id}`),
    ...articles.map((a) => `/articles/${a.id}`),
    ...issues.map((i) => `/archives/${i.id}`),
    ...announcements.map((a) => `/announcements/${a.id}`),
    ...sections.map((s) => `/sections/${s.id}`),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `  <url><loc>${base}${url}</loc></url>`).join('\n')}
</urlset>`;

  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
