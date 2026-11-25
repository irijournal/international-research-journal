import { defineConfig } from 'astro/config';

// Change "site" to your live domain once the domain is connected.
// Everything else on the website reads from src/data/settings.json.
export default defineConfig({
  site: 'https://internationalresearchinsights.com',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  redirects: {
    '/announcements/call-for-papers-volume-2-issue-1': '/announcements/call-for-papers',
  },
});
