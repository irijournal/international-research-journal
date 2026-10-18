import { chromium } from '/tmp/claude-0/-home-user-international-research-journal/55c29a40-3aee-5b96-9c75-9672107bc1f3/scratchpad/shot/node_modules/playwright/index.mjs';
const jobs = JSON.parse(process.argv[2]);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage();
for (const [html, pdf] of jobs) {
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
}
await browser.close();
