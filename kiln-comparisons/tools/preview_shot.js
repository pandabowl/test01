// Screenshot a comparison section on the live storefront, desktop + phone.
//
// Preview a draft (nothing is published; the HTML is injected in the browser only):
//   node preview_shot.js <page-url> <section-selector> <out-prefix> <draft.html> <insert-after-element-id>
// Screenshot what is already live:
//   node preview_shot.js <page-url> <section-selector> <out-prefix>
//
// Shared blocks (SHARED-BLOCKS.md): build the draft with tools/build_preview.py,
// then add "before" as a 6th argument to put it where the theme section renders
// it, directly above the section that contains the given id:
//   node preview_shot.js <page-url> '.sp-compare' preview draft.html abz_below_richtxt_id before
//
// Example:
//   node preview_shot.js https://www.sheffield-pottery.com/collections/skutt-ceramic-kilns \
//     '#sp-skutt-compare' preview template/comparison-section.html SkuttPoetry-guide
//
// Writes <out-prefix>-desktop.png and <out-prefix>-mobile.png and prints
// scrollWidth/innerWidth (they must be equal: no sideways scrolling).
const { chromium, devices } = require('playwright');
const fs = require('fs');

const [url, selector, outPrefix, draftFile, afterId, where] = process.argv.slice(2);
if (!url || !selector || !outPrefix) {
  console.error('usage: node preview_shot.js <url> <selector> <out-prefix> [draft.html insert-after-id]');
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
      const ok = await page.evaluate(([html, id, before]) => {
        const el = document.getElementById(id);
        if (!el) return false;
        if (before) (el.closest('.shopify-section') || el).insertAdjacentHTML('beforebegin', html);
        else el.insertAdjacentHTML('afterend', html);
        return true;
      }, [draft, afterId, where === 'before']);
      if (!ok) throw new Error(`element #${afterId} not found on page`);
    }
    // Hide sticky headers, popups and chat bubbles so they don't cover the shot
    // (not sticky table cells: store spec tables pin their first column).
    await page.evaluate(() => {
      for (const n of document.querySelectorAll('body *')) {
        const p = getComputedStyle(n).position;
        if ((p === 'fixed' || p === 'sticky') && !/^(TD|TH)$/.test(n.tagName)) n.style.setProperty('visibility', 'hidden', 'important');
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
