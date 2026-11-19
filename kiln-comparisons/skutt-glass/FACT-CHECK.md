# Skutt glass kilns: fact-check

Page: https://www.sheffield-pottery.com/collections/skutt-glass-kilns
(collection `gid://shopify/Collection/441790693698`).

**Since 2026-11-19 07:45 UTC the comparison is shared blocks** (see `SHARED-BLOCKS.md`):
`custom.comparison_blocks` = `skutt-glass` (`Metaobject/685610336627`),
`skutt-glass-picks` (`Metaobject/685610369395`), `kiln-compare-cta`
(`Metaobject/685569474931`). Repo copies: `blocks/`. The "Learn more" link in the
collection description points at `#skutt-glass`. To fix a spec, edit the block entry
(Content > Metaobjects > Kiln comparison block) and the copy in `blocks/`.

From 04:51 to 07:45 UTC it was embedded in `custom.abz_collection_below_descrption`
right after `<h3 id="SkuttGlass-guide">` (`superseded_…_with_embedded_section_…html`).

## Which collection

There are two "Skutt Glass Kilns" collections:

| | `skutt-glass-kilns` (441790693698) | `skutt-glass-kilns-1` (687783739763) |
|---|---|---|
| Products | 30 (kilns + accessories, furniture kits, packages) | 14 (kilns only) |
| SEO title / meta description | Custom ("Skutt Glass Kilns \| Glass Kilns for Sale \| Sheffield Glass Kilns") | Default |
| Top description | Yes, with "Learn more" → `#SkuttGlass-guide` | Empty |
| Below-products content | Yes (`SkuttGlass-guide`) | None (metafield not set) |
| Linked from | Skutt Kilns page description ("Click here for Skutt Glass Kilns") | Main menu, mobile drawer, Skutt Kilns quick-link chips |

Both are in the sitemap, and each has a self-referencing canonical tag.

**Decision (user, 2026-11-19):** use `skutt-glass-kilns`, point the navigation at it, and
hide `-1` (and the obsolete Scarab collection) with redirects. See "Changes made" below.

## Changes made (2026-11-19)

| What | Before | After | Backup |
|---|---|---|---|
| `custom.abz_collection_below_descrption` on `skutt-glass-kilns` | old guide only (digest `486d969f…`) | comparison inserted after `<h3 id="SkuttGlass-guide">` (digest `7064ff7a…`), verified byte for byte on the live page | `backup_abz_collection_below_descrption_before_2026-11-19.html` |
| Menu `main-menu-draft-nav-fix` (**the menu the live theme shows**, desktop + mobile drawer) | Kilns › Shop by Type › Glass Kilns → `/collections/skutt-glass-kilns-1` | → `/collections/skutt-glass-kilns` (diffed: 1 change, 174 items intact) | `backup_menu_main-menu-draft-nav-fix_before_2026-11-19.json` |
| Menu `main-menu-new` (not shown on the site) | same item → `-1` | → `skutt-glass-kilns` (diffed: 1 change, 173 items intact) | `backup_menu_main-menu-new_before_2026-11-19.json` |
| Quick-link metaobject `quick_link_object/skutt-glass-kilns` (Skutt Kilns page chip) | `…/collections/skutt-glass-kilns-1` | `…/collections/skutt-glass-kilns` | (one field) |
| New redirect | – | `/collections/skutt-glass-kilns-1` → `/collections/skutt-glass-kilns` | – |
| New redirect | – | `/collections/skutt-scarb-lampworking-kilns` → `/collections/skutt-glass-kilns` | – |
| Redirect `/collections/skutt-scarab-lampworking-glass-kilns` | → `/collections/skutt-scarb-lampworking-kilns` | → `/collections/skutt-glass-kilns` | – |
| Redirect `/skutt-scarb-lampworking-kilns-s/812.htm` | → `/collections/skutt-scarb-lampworking-kilns` | → `/collections/skutt-glass-kilns` | – |

### Move to shared blocks (2026-11-19, approved by the user)

| What | Before | After | Backup / copy |
|---|---|---|---|
| Block entries | – | `skutt-glass` (heading, intro, model-number box, table, footnote) and `skutt-glass-picks` (which to buy + lid-and-side vs. side-fired). Same wording as the embedded version; the long phone-card cell relabelled "Inside"; no `<style>`; no phone line | `blocks/skutt-glass.html`, `blocks/skutt-glass-picks.html` (read back from the store: exact) |
| `custom.comparison_blocks` | not set | `[skutt-glass, skutt-glass-picks, kiln-compare-cta]` | – |
| `custom.abz_collection_below_descrption` (same `metafieldsSet` call, `compareDigest` `a90d4843…`) | embedded section (the shared-blocks chat had removed its "since 1946" sentence at 07:10) | the original guide text, byte for byte (digest back to `486d969f…`) | `backup_…_before_blocks_2026-11-19.html`; now `live_…_after_blocks_2026-11-19.html` |
| Collection description "Learn more" | `#SkuttGlass-guide` | `#skutt-glass` (user's choice) | `backup_descriptionHtml_before_2026-11-19.html`, `live_descriptionHtml_2026-11-19.html` |

Verified on the live page: `kiln-compare-styles`, both blocks, `kiln-compare-cta` and the
below text each render exactly; the old `#sp-skutt-glass-compare` is gone; the blocks sit
directly above the below text; all 13 product links return 200; no sideways scrolling.

Rule from the user (via the shared-blocks chat): never claim how long Sheffield has sold
kilns ("since 1946"). Neither block contains it; the shared call-to-action no longer does either.

**Not done (blocked):** unpublishing `skutt-glass-kilns-1` and `skutt-scarb-lampworking-kilns`
from the Online Store. The Shopify connector refuses `publishableUnpublish` by policy.
Do it in Shopify admin (collection → Sales channels → uncheck Online Store). Until then
both pages still load, because Shopify only applies a redirect once the path stops resolving.

Left alone: `main-menu-1` (the old 291-item menu, not shown on the site) still has
Kilns › Skutt Kilns › Skutt Glass Kilns → `-1`; it appears only in the Qikify navigator's
link-list data and will follow the redirect.

## Sources (read 2026-11-19)

- Skutt *Glass Kiln Catalog* (Rev. 3/20/2018; file dated Jan 2021):
  https://skutt.com/images/Glass-Kiln-Catalog.pdf
  (embedded on https://skutt.com/skutt-resources/catalogs/glass-kilns/)
- Skutt model pages, https://skutt.com/products-page/glassmaster-kilns/<model>/
  for firebox-8x4, firebox-8x6-lt, firebox-14, gm-814, gm-1014, gm-1214, gm-1414,
  gm-818, gm-1018, gm-1227 (and the matching gmt-* pages: identical specs)
- Skutt spec sheets for the FireBox 8 family:
  `https://skutt.com/product_pdf_generator_prod_page.php?ItemNo=0297&...model=FIREBOX 8x4 LT`
  (also ItemNo 0287 = 8x6 LT, 0380 = FireBox 8 MTS)
- Skutt glass kiln shelf chart: https://skutt.com/images/Glass-Kiln-Shelf-Chart.jpg
  (on https://skutt.com/glass-kilns/kiln-accessories/furniture-kits/) and
  https://skutt.com/images/shelves-table.jpg (FireBox 8x4 and 8x6 shelf)
- Skutt manuals: GlassMaster LT manual (HotStart Pro, FB14, FB8 w GMLT, 2017):
  https://skutt.com/images/GlassMaster-LT-Operating-Manual-HotStart-Pro-FB14-FB8-w-GMLT-1.pdf
  and FireBox manual (2011): https://skutt.com/images/FireBox-8-1.pdf
- Skutt flameworking page: https://skutt.com/flame-working-kilns/
  ("Scarab kilns have been discontinued as of December 2025")

## What's on the page and where it comes from

| Column | Source |
|---|---|
| Interior W × L × D | Model pages' spec table ("Opening" × "Depth"); FireBox 8 family from the spec sheets |
| Shelf size | Skutt shelf chart (FireBox 8x4/8x6: shelves table). GM1214-3/GM1227-3: two 13" × 26" half shelves per layer. GM1414: three-piece layer (two 10.5" × 22" halves + 18" × 22"), or a 22" × 39" full shelf |
| Max temp | Model pages / spec sheets. GM kilns 1800°F on 240V and 208V. FireBox 14 1700°F. FireBox 8x4 LT cone 10 (2350°F), 8x6 LT cone 6 (2250°F), FireBox 8 GMLT 2000°F (GMLT manual electrical table) |
| Elements | Studio GM kilns: "lid elements and side elements" (model pages, catalog). Production GM818/1018/1227-3: side-fired, zone control (model pages, catalog). FireBox 14: element in lid (catalog; GMLT manual: "FireBox 14 two element lid design"). FireBox 8: coiled elements in the walls, plain lid (photo on the FireBox manual cover); the 8x4/8x6 LT share the FireBox 8 GMLT wiring diagram |
| Power / plug | Model pages and spec sheets, 240V single-phase for GM, 115V for FireBox |
| Best for | Skutt's own descriptions (e.g. FireBox 14 "ideal for tile and sushi plates", 1 sq ft of tile or a 12" square plate; GM1014 "fit the majority of projects"; GM1018 up to 3 layers; GM1227-3 up to 4 layers; GM1414 "likely the most widely used kiln by professional glass instructors") |
| "Best seller" badge (FireBox 8x6 LT) | Shopify sales, Skutt glass kilns, last 36 months: FireBox 8x6 LT 6 units, GM1414 5, GM1014 3. "Classroom standard" on the GM1414 is Skutt's own heading for it |
| Model number box | Derived from Skutt's specs, not quoted: Skutt doesn't publish a glass naming key. GM = GlassMaster, GMT = GlassMaster Touchscreen, 8/10/12 sides (shelf chart), depth 14 → 13.5", 18, 27; -3 = 3" brick (catalog: "energy-saving 3” brick") |

## Skutt's own sources disagree

- Opening widths: catalog 17.5" (GM814/818), 23.5" (GM1014/1018), 41.5" × 24.5" (GM1414),
  14.5" (FireBox 14); model pages 18", 23", 42" × 25", 15". The page uses the model pages.
- GM818 at 240V: catalog 26.7 A / 6400 W, model page 27.8 A / 6600 W. The page uses
  the model page (27.8 A). Note 6400 W / 240 V = 26.7 A, so the catalog figure is the
  internally consistent one; the model page may have copied the GM814's amps.
- FireBox 8 capacity: catalog 0.17 cu ft, spec sheets 0.2. Skutt's FireBox 8 page shows
  the 8x6 LT's capacity table (6.5" deep, 0.22) for the whole family. Capacity is not on our page.
- The FireBox 8 GMLT is not in Skutt's current lineup online: the FireBox 8 page lists
  8x6 LT, 8x4 LT and "FireBox 8 MTS" (2000°F, Mini Touchscreen). The GMLT version is in
  the 2018 catalog and the 2017 GMLT manual.

## Errors in the store's product data (not fixed; for the user)

| Product | Field | Store says | Skutt says |
|---|---|---|---|
| GM1214-3 | spec table, 3-phase 208V amps | 48 | **29.4** |
| GM818 | spec table, 208V watts | 6600 | **5500** |
| GM814 | spec table, watts (both rows) | 6600 | **6660** |
| FireBox 8x4 LT, 8x6 LT, 8 GMLT | shared spec table, depth for the "FIREBOX 8x4 LT", "FIREBOX 8X4 GMLT" and "FIREBOX 8" rows | 6.5" | **4.5"** (only the 8x6 LT is 6.5") |
| FireBox 8x4 LT, FireBox 8 GMLT | capacity table | 6.5" deep, 0.22 cu ft (the 8x6 LT's numbers) | **4.5" deep, 0.2 cu ft** (catalog: 0.17) |
| FireBox 8x4 LT, FireBox 8 GMLT | description spec card "Capacity" | 0.22 cu ft | **0.2 cu ft** (catalog: 0.17) |
| FireBox 8 GMLT (and the FireBox compare tables in all 4 FireBox descriptions) | Max temp | "Glass only" | **2000°F** |
| FireBox kilns | finder facts / descriptions | 120 V | Skutt's spec tables say **115 V** (its prose says "any spare 120V outlet") |
| GM814, GM1014, GM1214-3, GM818, GM1018, GM1227-3 | `custom.kiln_power`, `kiln_size` | empty | 240/208V; sizes as above |

Other things noticed:

- **FireBox 8 GMLT**: Skutt's site no longer lists a GMLT version (current: FireBox 8 MTS). Worth checking with Skutt that it can still be ordered.
- **Skutt GM1014 Glass Kiln Package**: ACTIVE but not published to the Online Store, so it isn't linked.
- **Scarab**: Skutt discontinued the Scarab line in December 2025. `skutt-scarb-lampworking-kilns` holds only 3 archived products (an empty page); it now has a redirect to `skutt-glass-kilns` and is waiting to be unpublished (see above). Both glass collections still contain the archived Scarabs (not shown on the storefront).
- The Skutt Kilns page text links "flame-working" to `/collections/skutt-scarab-lampworking-glass-kilns`, which now redirects to `skutt-glass-kilns`.
- The existing below-products text still has a "lead times may be up to 18 weeks" notice. Left as is.
- The GM814's URL handle is `skutt-kilns-glass-fusing-kiln-furniture-kit-skgm814` (says "furniture kit"). Changing it would need a redirect.
