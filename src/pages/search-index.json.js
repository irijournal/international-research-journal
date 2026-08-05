import { getCollection } from 'astro:content';

const clean = (value = '') =>
  value
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/[#>*_`|-]/g, ' ')
    .replace(/\[(.*?)\]\((.*?)\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();

export async function GET() {
  const [articles, issues, announcements, pages, sections, board] = await Promise.all([
    getCollection('articles'),
    getCollection('issues'),
    getCollection('announcements'),
    getCollection('pages'),
    getCollection('sections'),
    getCollection('board'),
  ]);

  const entries = [
    ...articles.map((item) => ({
      type: `${item.data.articleType} · ${item.data.section}`,
      title: item.data.title,
      summary: item.data.abstract.slice(0, 220),
      url: `/articles/${item.id}`,
      body: clean(`${item.data.authors.join(' ')} ${item.data.keywords.join(' ')} ${item.body}`),
    })),
    ...issues.map((item) => ({
      type: 'Issue',
      title: `Volume ${item.data.volume}, Number ${item.data.number}, ${item.data.period} ${item.data.year}`,
      summary: item.data.summary,
      url: `/archives/${item.id}`,
      body: clean(`${item.data.editorialTitle} ${item.body}`),
    })),
    ...announcements.map((item) => ({
      type: 'Announcement',
      title: item.data.title,
      summary: item.data.summary,
      url: `/announcements/${item.id}`,
      body: clean(item.body),
    })),
    ...pages.map((item) => ({
      type: 'Journal policy',
      title: item.data.title,
      summary: item.data.summary,
      url: `/${item.id}`,
      body: clean(item.body),
    })),
    ...sections.map((item) => ({
      type: 'Research section',
      title: item.data.title,
      summary: item.data.summary,
      url: `/sections/${item.id}`,
      body: clean(item.body),
    })),
    ...board.map((item) => ({
      type: 'Editorial board',
      title: item.data.name,
      summary: `${item.data.role}. ${item.data.designation}`,
      url: '/editorial-board',
      body: clean(`${item.data.qualification} ${item.data.institution ?? ''}`),
    })),
  ];

  return new Response(JSON.stringify(entries), {
    headers: { 'Content-Type': 'application/json' },
  });
}
