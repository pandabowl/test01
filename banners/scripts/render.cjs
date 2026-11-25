#!/usr/bin/env node
/**
 * Render Sheffield Pottery category header banners.
 *
 * Usage:
 *   node banners/scripts/render.cjs [key ...]      # default: every banner in banners.json
 *
 * Reads banners/banners.json, composites the product cutouts in
 * banners/cutouts/ (WebP with alpha, made by cutout.py) onto a textured background, sets the category name in the
 * old-site "glossy" lettering (orange-red bevelled fill, cream rim, drop
 * shadow) and writes banners/out/<key>.jpg at 2000x640 (the same 3.125:1
 * shape as the original 235x75 Volusion-era banners).
 *
 * Needs Playwright with a Chromium build (preinstalled in Claude Code cloud
 * sessions; elsewhere: npm i playwright && npx playwright install chromium)
 * and network access to Google Fonts for the Ribeye typeface.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const W = 2000, H = 640;
const FONT = 'Ribeye';

const spec = JSON.parse(fs.readFileSync(path.join(ROOT, 'banners.json'), 'utf8'));

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function productsHtml(b) {
  return (b.products || []).map(p => {
    const src = 'file://' + path.join(ROOT, 'cutouts', p.file);
    const style = [
      `left:${(p.x * W).toFixed(0)}px`,
      `top:${(p.y * H).toFixed(0)}px`,
      `height:${Math.round(p.h * H)}px`,
      // rectangular photos (clay/glaze swatches) get a fixed box, cropped to fill
      p.w != null ? `width:${Math.round(p.w * W)}px;object-fit:cover` : '',
      p.radius != null ? `border-radius:${p.radius}px` : '',
      `transform:translate(-50%,-50%) rotate(${p.rot || 0}deg)${p.flip ? ' scaleX(-1)' : ''}`,
      `z-index:${p.z || 1}`,
      p.opacity != null ? `opacity:${p.opacity}` : '',
      p.brightness != null ? `filter:brightness(${p.brightness}) drop-shadow(14px 20px 16px rgba(20,6,0,.6))` : '',
    ].filter(Boolean).join(';');
    return `<img class="p" src="${src}" style="${style}">`;
  }).join('\n');
}

// Small deterministic PRNG so patterns render identically every run.
function rng(seed) {
  let t = seed >>> 0;
  return () => { t += 0x6D2B79F5; let r = Math.imul(t ^ t >>> 15, 1 | t); r ^= r + Math.imul(r ^ r >>> 7, 61 | r); return ((r ^ r >>> 14) >>> 0) / 4294967296; };
}

// Optional generated background: a firebrick wall, or a grid of colour chips.
function patternSvg(b) {
  const pat = b.pattern;
  if (!pat) return '';
  const rnd = rng(pat.seed || 11);
  const pick = a => a[Math.floor(rnd() * a.length)];
  let out = '';
  if (pat.type === 'bricks') {
    const bh = pat.brickH || 74, bw = pat.brickW || 236, m = pat.mortar || 9;
    out += `<rect width="${W}" height="${H}" fill="${pat.mortarColor || '#3a2c22'}"/>`;
    for (let row = 0, y = -20; y < H; row++, y += bh + m) {
      for (let x = (row % 2 ? -bw / 2 : 0) - 30; x < W; x += bw + m) {
        const j = (rnd() - 0.5) * 0.16;
        out += `<rect x="${x.toFixed(1)}" y="${y}" width="${bw}" height="${bh}" rx="4" fill="${pick(pat.colors)}" style="filter:brightness(${(1 + j).toFixed(3)})"/>`;
      }
    }
  } else if (pat.type === 'chips') {
    const sz = pat.size || 120, g = pat.gap || 14;
    out += `<g transform="rotate(${pat.rot ?? -7} ${W / 2} ${H / 2})">`;
    for (let y = -H; y < H * 2; y += sz + g)
      for (let x = -200; x < W + 200; x += sz + g)
        out += `<rect x="${x}" y="${y}" width="${sz}" height="${sz}" rx="${pat.rx ?? 10}" fill="${pick(pat.colors)}"/>`;
    out += '</g>';
  }
  return `<g opacity="${pat.opacity ?? 1}">${out}</g>`;
}

function html(b) {
  const bg = b.bg || ['#c0602c', '#7a2a10', '#2e0d04'];
  const t = b.text || {};
  const title = esc(b.title);
  const x = t.x ?? 60, y = t.y ?? 575, size = t.size ?? 250, maxW = t.maxWidth ?? 1300;
  return `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=${FONT}&display=block">
<style>
  html,body{margin:0;padding:0;background:#000}
  #b{position:relative;width:${W}px;height:${H}px;overflow:hidden;
     background:radial-gradient(ellipse 75% 95% at ${b.glow || '68% 38%'}, ${bg[0]} 0%, ${bg[1]} 55%, ${bg[2]} 100%)}
  .layer{position:absolute;inset:0;width:${W}px;height:${H}px}
  .p{position:absolute;filter:drop-shadow(14px 20px 16px rgba(20,6,0,.6)) drop-shadow(3px 4px 3px rgba(20,6,0,.45))}
  #vig{background:radial-gradient(ellipse 80% 110% at 55% 45%, rgba(0,0,0,0) 55%, rgba(10,3,0,.55) 100%);z-index:50}
  #scrim{background:linear-gradient(to top, rgba(12,4,0,${(0.55 * (b.scrim ?? 1)).toFixed(2)}) 0%, rgba(12,4,0,0) 45%),
                     linear-gradient(to right, rgba(12,4,0,${(0.35 * (b.scrim ?? 1)).toFixed(2)}) 0%, rgba(12,4,0,0) 55%);z-index:51}
  #title{z-index:60}
</style></head><body>
<div id="b">
  <svg class="layer" style="z-index:0" xmlns="http://www.w3.org/2000/svg">
    ${patternSvg(b)}
    <filter id="mottle"><feTurbulence type="fractalNoise" baseFrequency="0.0035 0.006" numOctaves="4" seed="${b.seed || 7}"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.05"/></filter>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/>
      <feColorMatrix type="saturate" values="0"/></filter>
    <rect width="100%" height="100%" filter="url(#mottle)" opacity="${b.mottle ?? 0.45}" style="mix-blend-mode:multiply"/>
    <rect width="100%" height="100%" filter="url(#grain)" opacity="0.10" style="mix-blend-mode:overlay"/>
  </svg>
  ${productsHtml(b)}
  <div id="vig" class="layer"></div>
  <div id="scrim" class="layer"></div>
  <svg id="title" class="layer" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="fillG" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffd08a"/>
        <stop offset=".2" stop-color="#ff8a3a"/>
        <stop offset=".46" stop-color="#f4501a"/>
        <stop offset=".76" stop-color="#cc2c0c"/>
        <stop offset="1" stop-color="#861604"/>
      </linearGradient>
      <linearGradient id="rimG" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#fffaf0"/>
        <stop offset=".5" stop-color="#f6e4bd"/>
        <stop offset="1" stop-color="#d2a466"/>
      </linearGradient>
      <filter id="bevel" x="-5%" y="-20%" width="110%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="blur"/>
        <feSpecularLighting in="blur" surfaceScale="7" specularConstant="1.1" specularExponent="24" lighting-color="#ffffff" result="spec">
          <feDistantLight azimuth="225" elevation="32"/>
        </feSpecularLighting>
        <feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
        <feDiffuseLighting in="blur" surfaceScale="7" diffuseConstant="1" lighting-color="#ffffff" result="diff">
          <feDistantLight azimuth="225" elevation="60"/>
        </feDiffuseLighting>
        <feComposite in="SourceGraphic" in2="diff" operator="arithmetic" k1="1.15" k2="0" k3="0" k4="0" result="shaded"/>
        <feComposite in="shaded" in2="specIn" operator="arithmetic" k1="0" k2="1" k3="0.9" k4="0" result="lit"/>
        <feComposite in="lit" in2="SourceAlpha" operator="in"/>
      </filter>
      <filter id="rimBevel" x="-5%" y="-20%" width="110%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
        <feDiffuseLighting in="blur" surfaceScale="5" diffuseConstant="1.1" lighting-color="#ffffff" result="diff">
          <feDistantLight azimuth="225" elevation="55"/>
        </feDiffuseLighting>
        <feComposite in="SourceGraphic" in2="diff" operator="arithmetic" k1="1.1" k2="0" k3="0" k4="0" result="shaded"/>
        <feComposite in="shaded" in2="SourceAlpha" operator="in"/>
      </filter>
      <filter id="shadow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
      <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
    </defs>
    <g id="t" font-family="${FONT}" font-size="${size}" style="font-kerning:normal">
      <text x="${x + 10}" y="${y + 14}" fill="#1a0701" stroke="#1a0701" stroke-width="44" stroke-linejoin="round" opacity=".8" filter="url(#shadow)">${title}</text>
      <text x="${x}" y="${y}" fill="#ffe9b8" stroke="#ffe9b8" stroke-width="48" stroke-linejoin="round" opacity=".45" filter="url(#glow)">${title}</text>
      <text x="${x}" y="${y}" fill="#3b1405" stroke="#3b1405" stroke-width="42" stroke-linejoin="round" opacity=".85">${title}</text>
      <text x="${x}" y="${y}" fill="url(#rimG)" stroke="url(#rimG)" stroke-width="34" stroke-linejoin="round" filter="url(#rimBevel)">${title}</text>
      <text x="${x}" y="${y}" fill="#6e1203" stroke="#6e1203" stroke-width="7" stroke-linejoin="round">${title}</text>
      <text x="${x}" y="${y}" fill="url(#fillG)" filter="url(#bevel)">${title}</text>
    </g>
  </svg>
</div>
<script>
  // shrink the title to fit its box if the category name is long
  window.fitTitle = () => {
    const g = document.getElementById('t');
    const w = g.querySelector('text:last-child').getComputedTextLength();
    if (w > ${maxW}) g.setAttribute('font-size', ${size} * ${maxW} / w);
    return w;
  };
</script>
</body></html>`;
}

(async () => {
  const want = process.argv.slice(2);
  const banners = spec.banners.filter(b => !want.length || want.includes(b.key));
  if (!banners.length) { console.error('no matching banners'); process.exit(1); }
  fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  for (const b of banners) {
    const file = path.join(ROOT, 'out', `.${b.key}.html`);
    fs.writeFileSync(file, html(b));
    await page.goto('file://' + file, { waitUntil: 'networkidle' });
    await page.evaluate(async f => { await document.fonts.load(`200px "${f}"`); await document.fonts.ready; }, FONT);
    const ok = await page.evaluate(f => document.fonts.check(`200px "${f}"`), FONT);
    if (!ok) throw new Error(`font ${FONT} did not load`);
    await page.evaluate(() => window.fitTitle());
    const out = path.join(ROOT, 'out', `${b.key}.jpg`);
    await page.locator('#b').screenshot({ path: out, type: 'jpeg', quality: 88 });
    fs.unlinkSync(file);
    console.log('wrote', path.relative(process.cwd(), out));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
