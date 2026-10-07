// Checks slide.html's baked-in text and button against the live theme's
// slideshow chrome at every viewport width from 320 to 2560px:
//   - the navigation dots (bottom-left, over the image), and
//   - the slide link, which only covers the centred content strip.
// Geometry comes from the theme's assets/theme.css (see README "Safe zones").
//
//   npm run check
import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const ARTBOARDS = { desktop: { w: 1900, h: 550 }, mobile: { w: 617, h: 800 } };
const MOBILE_BELOW = 720;   // theme swaps to the mobile image below 720px
const MAX_WIDTH = 1400;     // --max-width
const DOTS = 4;             // enabled slides
const DOT_TAP = 24;         // each dot button: 12px padding around the dot
const MIN_GAP = 12;         // px of clearance we want between button and dots

const browser = await chromium.launch();
let boxes;
try {
  const page = await browser.newPage({ viewport: { width: 1900, height: 1400 } });
  await page.goto(pathToFileURL(path.join(here, "slide.html")).href);
  await page.evaluate(() => document.fonts.ready);
  boxes = await page.evaluate(() => {
    const out = {};
    for (const id of ["desktop", "mobile"]) {
      const b = document.getElementById(id).getBoundingClientRect();
      const rel = (el) => {
        const r = el.getBoundingClientRect();
        return { x: r.left - b.left, y: r.top - b.top, w: r.width, h: r.height };
      };
      out[id] = Object.fromEntries(
        ["eyebrow", "headline", "sub", "cta"].map((c) => [c, rel(document.querySelector(`#${id} .${c}`))]),
      );
    }
    return out;
  });
} finally {
  await browser.close();
}

const overlaps = (a, b) => !(a.x + a.w <= b.x || b.x + b.w <= a.x || a.y + a.h <= b.y || b.y + b.h <= a.y);
const problems = [];
let closest = { gap: Infinity };
for (let vw = 320; vw <= 2560; vw++) {
  const board = vw >= MOBILE_BELOW ? "desktop" : "mobile";
  const k = vw / ARTBOARDS[board].w;
  const slideH = ARTBOARDS[board].h * k;
  const gutter = vw >= MOBILE_BELOW ? 0.033 * vw : Math.max(18, 0.033 * vw);  // --space-outer
  const strip = Math.min(vw, MAX_WIDTH + 2 * gutter);
  const stripL = (vw - strip) / 2;
  // dots row: 32px above the slide bottom, 26px tall, starts gutter + 8px margin + 2px padding in
  const dots = { x: stripL + gutter + 10, y: slideH - 32 - 26 + 1, w: DOTS * DOT_TAP, h: DOT_TAP };
  for (const [name, b] of Object.entries(boxes[board])) {
    const v = { x: b.x * k, y: b.y * k, w: b.w * k, h: b.h * k };
    if (overlaps(v, dots)) problems.push(`${vw}px: ${board} ${name} is under the slideshow dots`);
    if (name !== "cta") continue;
    if (v.x < stripL || v.x + v.w > stripL + strip) problems.push(`${vw}px: ${board} button is partly outside the slide link`);
    const gap = Math.max(dots.y - (v.y + v.h), v.x - (dots.x + dots.w));
    if (gap < closest.gap) closest = { gap: Math.round(gap * 10) / 10, vw, board };
  }
}
if (closest.gap < MIN_GAP) problems.push(`button comes within ${closest.gap}px of the dots at ${closest.vw}px`);

if (problems.length) {
  console.error(problems.slice(0, 20).join("\n") + (problems.length > 20 ? `\n...and ${problems.length - 20} more` : ""));
  process.exit(1);
}
console.log(`OK: text and button clear of the dots and inside the slide link at 320-2560px ` +
  `(closest: ${closest.gap}px at ${closest.vw}px, ${closest.board})`);
