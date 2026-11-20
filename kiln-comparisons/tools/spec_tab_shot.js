// node spec_tab_shot.js <product-handle> <theme-id|live> <out-prefix>
const { chromium, devices } = require('playwright');
const [handle, themeId, out] = process.argv.slice(2);
(async () => {
  const launch = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {};
  const browser = await chromium.launch(launch);
  for (const [name, opts] of [['desktop', { viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 }], ['mobile', devices['iPhone 13']]]) {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    const q = themeId === 'live' ? '' : `preview_theme_id=${themeId}&`;
    await page.goto(`https://www.sheffield-pottery.com/products/${handle}?${q}v=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForTimeout(5000);
    await page.evaluate(() => { for (const n of document.querySelectorAll('body *')) { const p = getComputedStyle(n).position; if ((p === 'fixed' || p === 'sticky') && !/^(TD|TH)$/.test(n.tagName)) n.style.setProperty('visibility', 'hidden', 'important'); } });
    const sec = page.locator('.HK-Tab-Section').first();
    const btn = page.locator('[data-sp-spec-jump]').first();
    if (await btn.count()) {
      await btn.scrollIntoViewIfNeeded();
      await page.waitForTimeout(600);
      // description tab: tab bar + first ~650px
      const sb = await sec.boundingBox();
      const sy = await page.evaluate(() => scrollY);
      await page.screenshot({ path: `${out}-${name}-1desc.png`, fullPage: true, clip: { x: 0, y: sb.y + sy, width: sb.width, height: Math.min(sb.height, name === 'mobile' ? 560 : 520) } });
      await btn.click();
    } else {
      const li = page.locator('#tabs-nav a[href^="#tab-specifications"]').first();
      if (await li.count()) { await li.scrollIntoViewIfNeeded(); await li.click(); }
    }
    await page.waitForTimeout(1800);
    const st = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth,
      current: [...document.querySelectorAll('tr.spc-current td.spc-model')].map(td => td.textContent.trim().slice(0, 40)) }));
    console.log(name, JSON.stringify(st));
    await page.screenshot({ path: `${out}-${name}-2afterclick.png` });
    await sec.screenshot({ path: `${out}-${name}-3specs.png` });
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
