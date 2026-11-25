// Renders HTML jobs to PDF/PNG with Chromium. Playwright is loaded from PLAYWRIGHT_MODULE.
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE);
const jobs = JSON.parse(process.argv[2]);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const j of jobs) {
  const p = await b.newPage({ viewport: { width: j.w || 1000, height: j.h || 1000 }, deviceScaleFactor: j.scale || 1 });
  await p.goto('file://' + j.html, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  if (j.pdf) await p.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
  if (j.png) await p.screenshot({ path: j.png });
  if (j.sel) await (await p.$(j.sel)).screenshot({ path: j.selpng });
  await p.close();
}
await b.close();
