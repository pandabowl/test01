# Cone Art kilns: Google SEO + AI-agent readiness audit

Audit of every Shopify product with vendor **Cone Art Kilns** (99 products: 40 on the
storefront, 59 hidden option products) and the seven Cone Art collections, done 2026-10-04
through the Shopify Admin API plus the live theme code (`ABZ Stiletto - Plain Home Page
banners`). The live site itself could not be crawled from the audit environment, so
everything below is based on store data and theme source.

The fixes that can be made safely from store data are scripted in
`scripts/cone_art_seo.py`. Review every change in [`plan.md`](plan.md), then apply with
`apply --execute`; roll back with `rollback --execute`. The rest needs a human decision and
is listed under [Needs a decision](#needs-a-decision-not-applied).

**Status: applied to the live store on 2026-10-04.** Every product, FAQ entry, hidden
product and collection was read back afterwards and matched `plan.json` field for field
(1,872 checks, 0 differences). [`snapshot.json`](snapshot.json) is the pre-apply backup that
`rollback` restores, so don't re-run `snapshot` unless you mean to replace it (git keeps the
original either way).

## How Google and AI agents read these pages

* **`<title>` and meta description** come from Shopify's own SEO fields. Booster SEO
  renders them, but its auto-title/description rules are off, so it passes the native
  fields straight through. Editing `seo.title` and `seo.description` changes what Google sees.
* **Structured data:** every product page outputs two Product JSON-LD blocks, one inline in
  `layout/theme.liquid` and one from Booster (`snippets/booster-seo.liquid`). Booster also
  outputs FAQPage JSON-LD from a `custom.faqs` metafield, though no Cone Art product had one.
* **On-page FAQ:** the product template already has an "ABZ Faq" section that renders
  `custom.product_faqs`. That field was empty on every Cone Art product.
* **AI shopping agents:** these include Shopify Catalog / UCP (ChatGPT, Copilot, Perplexity…),
  Google AI Mode, and browser agents using Shopify's WebMCP tools. They read the product
  title and description, the standard category and category attributes, variants,
  availability, and the product's collections with their descriptions. Anything wrong in
  those fields gets repeated to shoppers.

## Findings

### 1. Titles and meta descriptions (all 40 storefront products)

* **Wrong model on the page.**
  * BX1818D used the BX1822D's title and description, which made the two pages duplicates.
  * The GX4227D package showed "Cone Art BX4227D Oval Kiln".
  * The GX2327D-SQ package showed the BX2327DSQ's.
  * The BX2318D-SQ had a generic "Cone Art Kiln | Ceramic Cone Art Kilns | Tucker's Pottery".
* **Format problems.**
  * Most titles were over 60 characters, so Google truncates them.
  * Some were ALL CAPS ("CONEART BX2827  KILN").
  * Many started with "Order a Tucker's…".
  * Doubled spaces throughout.
* **Weak meta descriptions.** Many just repeated the title. One was the cut-off string
  `'22\'`. Most ended "…from Sheffield Pottery Ceramic Supllies." (typo).
* **Fix:** a unique, spec-led title (≤ 60 characters) and meta description (≤ 155) for every
  product, all written from the store's own spec tables.

### 2. Wrong or contradictory facts that agents would repeat

**Fixed (each value checked against the product's own spec table):**

| Product | Problem | Fix |
|---|---|---|
| 117G | Headline says "CONE ART BX1809 GLASS FUSING KILN" | "Cone Art 117G Glass Fusing Kiln" |
| 2809G | Overview copied from the 2309G ("G 2309 - 2.3 Cubic ft", "40 Amp breaker", "model G2309") | 2809G, 3.3 cu ft, 60 A, as in its spec table and on the sibling 2813G |
| BX2318D-SQ | "70 or 80 Amp breaker required", copied from the 2322/2327 square kilns | "50 or 60 Amp", per its spec table (40 A / 46 A draw) |
| 4213G | Spec table amps "48 \| 45" | "48 \| 55" (11.5 kW at 208 V = 55 A, same as the 4209G) |
| BX1818D | "208 or 204 Volts" | "208 or 240 Volts" |
| BX2322D-SQ | "BX12322D SQ" | "BX2322D SQ" |
| BX2327D-SQ | "more stacking space than it's cousin the 2327D SQ" | "…than its cousin the 2327D" |
| GX4227D pkg | Body text calls it "BX4227D"; "Bartlet" | GX4227D; Bartlett |
| GX2327D & GX2327D-SQ pkgs | "Optional (Extra) Furniture Kit", though the furniture kit is in the package title | "Included Furniture Kit" |
| BX119D | Voltage filter says "240 or 208" (it is a 120 V kiln) | "120 Volt" |
| GX119D, 2309G-SQ, 2313G-SQ | Voltage / style / type filters blank | Filled in |
| BX1818D, BX2318D-SQ, GX2327D-SQ pkg | Short description under the title names another model (BX1822, "Bx2323D", BX2327DSQ) | Corrected |
| GX1813D | Short description "with Free Post set: In stock!" while the page says lead time end of next month | Neutral product summary |
| 5 spec tables + 3 package descriptions | "Inside Dimenssions" | "Inside Dimensions" |

**Disputed, so left out of all new copy. Please check against Cone Art's spec sheet:**

| Product | Store says | Also says |
|---|---|---|
| BX1813D / GX1813D | 1.7 cu ft (description) | 1.98 cu ft (spec table) |
| BX2818D | 6.5 cu ft (description) | 6.66 cu ft (spec table) |
| 2313G | 3.5 cu ft (description) | 3.4 cu ft (spec table) |
| BX2822D | "63 or 72.5 amp breaker" (those are its amp draws) | 80 A / 90 A single phase, 50 A three phase (spec table) |
| BX2827D, GX2827D package | 70 or 80 A breaker | 80 A / 90 A single phase, 50 A three phase |
| BX4222D, BX4227D, GX4227D package | 80 or 90 A breaker | 90 A single phase, 60 A three phase |
| BX4222D | 42" x 31" x 22.5" (description) | 41" x 32" x 22.5" (spec table) |
| 2809G | 2.5" firebrick walls | 3" brick walls and lid (2813G page, which covers both models) |

Breaker sizes appear in the new FAQs only where the description and spec table agree.
Every electrical answer points to the Specifications tab and a licensed electrician.

### 3. Hidden option products are indexed and searchable

59 add-on products are tagged `HideOnStorefront`: furniture kits, vents, maintenance kits,
controller upgrades and "$0.00" shelf options. They are still published to the Online Store
and have public URLs, so Google can index them, they appear in `sitemap.xml`, and they show
up in storefront search, which browser-based AI agents use. Many have thin text such as
"Product option do not apply" and a "NOT FOR INDIVIDUAL SALE" image. Two already had
`seo.hidden = 1`.

**Fix:** `seo.hidden = 1` on the other 57. This adds `noindex,nofollow` and removes them from
the sitemap and storefront search, but they stay ACTIVE, so the product-options app can still
add them to the cart.

### 4. Shopify category, product type, and collections

* **Wrong Shopify product category on 7 products:**
  * 5 kiln packages were filed as "Pottery & Sculpting Materials".
  * The 4213G glass kiln was filed as "Pottery & Sculpting Materials", with product type
    "Kiln Furniture" and Item Class "Kiln Furniture".
  * The replacement thermocouple was filed as "Pottery & Sculpting Materials".

  These now use Ceramic & Pottery Kilns, Glass Kilns, and Thermocouples. The product category
  drives Google's product category and Shopify Catalog's classification.
* **Glass collection lists pottery kilns.** 25 pottery kilns and packages carried the tag
  `Cone Art Glass Fusing Kilns`, so the **Cone Art Glass Kilns** collection listed BX/GX
  pottery kilns. Agents see that membership through the Storefront Catalog. The tag is
  removed from every non-glass product.
* **Packages collection is missing two packages.** The GX2327D-SQ and GX4227D packages lacked
  the tag that feeds **Cone Art Kilns Energy Efficient Kiln Packages**, so they were left out.
  The tag is added.
* **Brand collection includes the hidden option products.** `/collections/cone-art-kilns` is
  a vendor-rule collection, so it also contained all 59 hidden option products. It also had
  no description and no meta description. Fix: add the condition "tag is not equal to
  HideOnStorefront", a short description, and SEO fields.
* **The brand hub `/collections/tucker-s-cone-art-kilns` made claims that aren't true:**
  * "Cone Art kilns from multiple manufacturers"
  * "in stock" for the whole line, when most pages say lead time end of next month
  * "Each product page shows an expected delivery date once you select your voltage and phase"
    (only 7 products have voltage variants)
  * a stale "$1,539" price floor (the cheapest Cone Art kiln is now $1,729)
  * "Every kiln features … floor element" (glass kilns and the 119D/1813D don't have one)

  Rewritten as evergreen, factual copy with a visible FAQ, plus the same Q&A in `custom.faqs`
  for FAQPage JSON-LD.
* **Glass collection description contains chat-UI CSS classes**
  (`font-claude-response-body …`) pasted in with the text. Removed.
* **Two empty Cone Art collections are published** ("Cone Art Kilns : Upgrade to the Genesis
  Touch Screen Controller", "Cone Art Upgrade to Touch Screen"). They get `seo.hidden = 1`.

### 5. Answers and structured attributes for AI agents

* **New FAQs.** 212 product FAQ entries across 40 products. Each covers what the kiln fires,
  interior size, electrical service, controller, furniture, and efficiency. Every answer comes
  from that product's own data. They show on the page through the existing ABZ Faq section and
  as FAQPage JSON-LD through Booster.
* **Standard category attributes.** 39 kilns get kiln features, loading style, firing
  atmosphere, heating element type, power source and shape. These are the structured fields
  Shopify Catalog exposes to AI agents; without them, agents rely on Shopify's own guesses.

## What `apply` changes

| Area | Count |
|---|---|
| Product SEO title + meta description | 40 |
| Product category fixes | 7 |
| Product type fixes | 2 |
| Description text fixes | 10 products |
| Tag fixes (collection membership) | 25 removed, 2 added |
| Metafield fixes (filters, item class, short descriptions, spec tables) | 42 |
| Product FAQ entries (visible + JSON-LD) | 212 on 40 products |
| Products with standard category attributes | 39 |
| Hidden option products set to `seo.hidden` | 57 |
| Collections updated | 7 |

```bash
export SHOPIFY_STORE_DOMAIN=sheffield-pottery.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx
python3 scripts/cone_art_seo.py snapshot        # refresh the backup first (replaces the pre-apply rollback baseline)
python3 scripts/cone_art_seo.py plan            # rebuild plan.json / plan.md from it
python3 scripts/cone_art_seo.py apply           # dry run
python3 scripts/cone_art_seo.py apply --execute
python3 scripts/cone_art_seo.py rollback --execute   # undo, if ever needed
```

Not touched: prices, inventory, variants, handles/URLs, images, the theme, and app settings.

## Needs a decision (not applied)

1. **Consolidate the structured data.** Product pages emit two Product JSON-LD blocks with
   different data:
   * The theme block sets `mpn` = Sheffield's SKU (e.g. `TUCBX2327D`).
   * The Booster block sets `mpn` and `gtin14` to the barcode, which is blank, so it outputs
     `"mpn": ""` and `"gtin14": ""`.

   Keep one. [`theme/product-jsonld.liquid`](theme/product-jsonld.liquid) replaces the
   theme's inline block: per-variant offers, schema.org URLs, and spec `additionalProperty`
   values from the metafields this change fills in. Booster's Product block is switched off
   by a flag in its snippet; its BreadcrumbList and FAQPage markup stay on, and the new FAQs
   rely on the FAQPage block.

   **Status: installed on the unpublished theme copy "Copy of ABZ Stiletto - JSON-LD -
   (04-10-26)" (theme ID 195816882547) for testing. The live theme is unchanged.** The exact
   edits are in [`theme/theme-changes.patch`](theme/theme-changes.patch). Check a few
   product pages on the copy in Google's Rich Results Test before publishing it. Booster
   updates its snippet from time to time; if that happens after the copy goes live, re-apply
   the `booster_product_schema` guard from the patch.
2. **Booster merchant-listing settings are empty.** Return policy category, return days,
   fees, shipping rate, and handling/transit times are all blank. Booster still outputs a
   `MerchantReturnPolicy` without `returnPolicyCategory`, which Google reports as invalid.
   Fill these in from the real policy in the Booster app. If the theme copy from #1 is
   published, Booster's Product block is no longer output, and its return and shipping markup
   goes with it. In that case, set the return and shipping policies in Google Merchant Center
   instead.
3. **Product identifiers.**
   * Cone Art kilns have no GTIN/barcode.
   * The `custom.pdp_vendor_part_no` field is unreliable: `SCABX2327D` was copied onto
     11 other products.

   Confirm Cone Art's manufacturer part numbers (MPN). Then either set Shopify's standard
   `shopify--facts.mpn` field, or mark the products as custom products in the Google channel
   so Merchant Center stops flagging missing identifiers.
4. **Availability.**
   * Kilns sell with 0 stock (continue selling) and a lead time of "End of Next Month", but
     the structured data says `InStock`.
   * Some variant names carry stale availability text, e.g. GX2827D package
     "240/1 : Expected Early July".

   Set a Merchant Center handling time for made-to-order kilns, or switch to
   backorder + availability date (feed and page must match). Also remove dates from
   variant names.
5. **Shipping weights.** 38 kilns have a placeholder weight of 501 lb. The BX2327D-SQ shows
   1.5 lb. The spec tables list real ship weights (130–665 lb). Fix these if
   carrier-calculated rates or Merchant Center shipping use weight.
6. **BX1818D URL.** Its handle is `cone-art-bx1822d-kiln`, a different model. Rename it to
   e.g. `cone-art-bx1818d-kiln` with an automatic redirect (`redirectNewHandle`).
7. **Two brand pages.** `/collections/cone-art-kilns` and `/collections/tucker-s-cone-art-kilns`
   both target "Cone Art kilns". This change gives them distinct titles and links the vendor
   page to the hub. Long term, pick one to link from the nav and the Kilns page.
8. **Shopify Knowledge Base (agent answers).** The store has 47 AI-suggested Knowledge Base
   facts, all unpublished. "Main brands" omits Cone Art. "Founded in 1943" conflicts with the
   theme's "Ceramic Supplier since 1946" and the hub's "80th year". Review and publish the
   facts in the Knowledge Base app.
9. **Shop channel.** The Cone Art kilns are published to Online Store, POS, Google & YouTube,
   Facebook & Instagram and Inbox, but not **Shop**. Check whether that limits Shopify
   Catalog / agentic storefront reach for this store.
10. **Reviews.** Every Cone Art product has 0 reviews. Reviews (Yotpo is installed) are a
    major ranking and recommendation signal for both Google and AI agents. Turn on
    post-delivery review requests for kiln buyers.
11. **Store-wide LocalBusiness markup.** It claims the store is open 00:00–23:59, seven days
    a week, and has an empty `@id`. Correct the hours.
