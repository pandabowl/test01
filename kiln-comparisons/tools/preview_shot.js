// Screenshot a comparison section on the live storefront, desktop + phone.
//
// Preview a draft (nothing is published; the HTML is injected in the browser only):
//   node preview_shot.js <page-url> <section-selector> <out-prefix> <draft.html> <insert-after-element-id> [position]
//   (position is an insertAdjacentHTML position: afterend by default; use beforebegin to put the
//   draft just before the element, e.g. at the very top of the below-grid block)
// Screenshot what is already live:
//   node preview_shot.js <page-url> <section-selector> <out-prefix>
//
// Example:
//   node preview_shot.js https://www.sheffield-pottery.com/collections/skutt-ceramic-kilns \
//     '#sp-skutt-compare' preview template/comparison-section.html SkuttPoetry-guide
//
// Writes <out-prefix>-desktop.png and <out-prefix>-mobile.png and prints
// scrollWidth/innerWidth (they must be equal: no sideways scrolling).
const { chromium, devices } = require('playwright');
const fs = require('fs');

const [url, selector, outPrefix, draftFile, afterId, position = 'afterend'] = process.argv.slice(2);
if (!url || !selector || !outPrefix) {
  console.error('usage: node preview_shot.js <url> <selector> <out-prefix> [draft.html insert-after-id [position]]');
  process.exit(2);
}
const draft = draftFile ? fs.readFileSync(draftFile, 'utf8') : null;

(async () => {
  const launch = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {};
  const browser = await chromium.launch(launch);
  const targets = [
    ['desktop', { viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 }],
    ['mobile', devices['iPhone 13']],
  ];
  for (const [name, opts] of targets) {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(4000);
    if (draft) {
      const ok = await page.evaluate(([html, id, pos]) => {
        const el = document.getElementById(id);
        if (!el) return false;
        el.insertAdjacentHTML(pos, html);
        return true;
      }, [draft, afterId, position]);
      if (!ok) throw new Error(`element #${afterId} not found on page`);
    }
    // Hide sticky headers, popups and chat bubbles so they don't cover the shot.
    await page.evaluate(() => {
      for (const n of document.querySelectorAll('body *')) {
        const p = getComputedStyle(n).position;
        if (p === 'fixed' || p === 'sticky') n.style.setProperty('visibility', 'hidden', 'important');
      }
    });
    const el = await page.$(selector);
    if (!el) throw new Error(`${selector} not found on page`);
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);
    await el.screenshot({ path: `${outPrefix}-${name}.png` });
    const w = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
    console.log(`${name}: scrollWidth=${w[0]} innerWidth=${w[1]}${w[0] > w[1] ? '  <-- HORIZONTAL SCROLL' : ''}`);
    await ctx.close();
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
