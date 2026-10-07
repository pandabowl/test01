// Renders slide.html's artboards to the JPGs uploaded to Shopify.
//
//   npm install && npm run render
//
// Output is @2x of the existing slideshow sizes (1900x550 desktop, 617x800
// mobile) so the baked-in text stays sharp on retina screens while keeping
// the same aspect ratio as the other slides.
import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const SCALE = 2;
const ARTBOARDS = [
  { selector: "#desktop", file: "bth-d3-gift-certificate-desktop.jpg" },
  { selector: "#mobile", file: "bth-d3-gift-certificate-mobile.jpg" },
];
const FONTS = [
  '800 10px "Barlow Condensed"',
  '500 10px "Barlow"',
  '600 10px "Barlow"',
  '700 10px "Barlow"',
  '700 10px "Playfair Display"',
  '900 10px "Playfair Display"',
  'italic 400 10px "Playfair Display"',
];

const browser = await chromium.launch();
try {
  const page = await browser.newPage({
    viewport: { width: 1900, height: 1400 },
    deviceScaleFactor: SCALE,
  });
  await page.goto(pathToFileURL(path.join(here, "slide.html")).href);

  const missing = await page.evaluate(async (fonts) => {
    const results = await Promise.all(fonts.map((f) => document.fonts.load(f)));
    return fonts.filter((_, i) => results[i].length === 0);
  }, FONTS);
  if (missing.length) {
    throw new Error(`Fonts failed to load (run \`npm install\` first): ${missing.join(", ")}`);
  }

  for (const { selector, file } of ARTBOARDS) {
    const out = path.join(here, file);
    await page.locator(selector).screenshot({ path: out, type: "jpeg", quality: 90 });
    console.log(`wrote ${file}`);
  }
} finally {
  await browser.close();
}
