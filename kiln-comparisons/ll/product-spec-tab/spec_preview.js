// Preview the spec-tab move on the unpublished theme copy, in the browser only.
// node spec_preview.js <handle> <draft.description.html> <draft.specifications.html> <out-prefix>
const { chromium, devices } = require('playwright');
const fs = require('fs');
const [handle, descFile, specFile, out] = process.argv.slice(2);
const desc = fs.readFileSync(descFile, 'utf8'), spec = fs.readFileSync(specFile, 'utf8');
const url = `https://www.sheffield-pottery.com/products/${handle}?preview_theme_id=197922586995`;
(async () => {
  const launch = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {};
  const browser = await chromium.launch(launch);
  for (const [name, opts] of [['desktop', { viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 }], ['mobile', devices['iPhone 13']]]) {
    const ctx = await browser.newContext(opts); const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForTimeout(5000);
    const info = await page.evaluate(([desc, spec]) => {
      const d = document.getElementById('tabProductDescription');
      const jump = d.querySelector('.sp-spec-jump-wrap');
      while (jump && jump.nextSibling) jump.nextSibling.remove();
      d.insertAdjacentHTML('beforeend', desc);
      const t = document.querySelector('.sp-specs-tab');
      const old = t.querySelector('.hk-specs-table-wrap'); if (old) old.remove();
      t.insertAdjacentHTML('afterbegin', '<div class="rte hk-specs-table-wrap">' + spec + '</div>');
      for (const n of document.querySelectorAll('body *')) {
        const p = getComputedStyle(n).position;
        if (p === 'fixed' || (p === 'sticky' && !n.closest('table'))) n.style.setProperty('visibility', 'hidden', 'important');
      }
      return { theme: (window.Shopify && Shopify.theme && Shopify.theme.name) || '?' };
    }, [desc, spec]);
    const d = await page.$('#tabProductDescription');
    await d.scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
    await d.screenshot({ path: `${out}-${name}-description.png` });
    await page.click('a[href^="#tab-specifications"]').catch(() => {});
    await page.waitForTimeout(800);
    const t = await page.$('.sp-specs-tab');
    await t.scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
    await t.screenshot({ path: `${out}-${name}-spectab.png` });
    const w = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
    console.log(`${handle} ${name}: theme=${info.theme} scrollWidth=${w[0]} innerWidth=${w[1]}`);
    await ctx.close();
  }
  await browser.close();
})();
