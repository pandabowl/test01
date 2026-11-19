# Kiln model comparison sections: playbook

> **Update 2026-11-19:** comparison tables are now published as **shared
> blocks**, not pasted into `custom.abz_collection_below_descrption`. Steps 1–3
> below (where things are, store data, fact-check) still apply; steps 4–8 are
> replaced by [`SHARED-BLOCKS.md`](SHARED-BLOCKS.md). Skutt pottery moved to
> blocks on 2026-11-19.

How to add a fact-checked "model comparison" section to a kiln brand's
collection page on sheffield-pottery.com. Skutt pottery kilns were the first
one (`/collections/skutt-ceramic-kilns`, live since 2026-11-18). Everything in
`skutt-ceramic/` is the worked example.

Why: the SEO plan (Phase 1) calls for explicit sections comparing popular
models right on the brand's collection landing page, so the page answers
"which model?" searches for the brand name.

## Ground rules

- **Show the user before publishing.** Share desktop and phone previews plus
  the list of store-data problems you found, and publish only after they say so.
- **Every number gets fact-checked against the manufacturer.** The store's own
  spec tables (`custom.specifications`) have copy/paste errors (wrong
  capacities, typos like "640 amps", a capacity table copied from another
  model). Use them as leads, never as the source.
- **Don't change product data** (spec tables, descriptions) unless the user asks.
  List the errors you find for them instead (see `skutt-ceramic/FACT-CHECK.md`).
- **Leave existing page content alone** unless the user asks you to remove it.
- **No prices in the section.** They change often and the product grid shows them.
- Back up every metafield before you overwrite it, and save the backup in this
  folder.

## 0. Setup

1. Bring this folder into your branch:
   `git fetch origin claude/elegant-bohr-1e5ynt && git checkout FETCH_HEAD -- kiln-comparisons`
2. **The manufacturer's website must be on the allowed-hosts list.** The cloud
   network blocks unknown sites, and that applies to WebFetch too (it fails with
   `ENOTFOUND`). Call `get_environment`, then `update_environment` with
   `add_allowed_hosts` (e.g. `["skutt.com","www.skutt.com"]`); the user approves
   a card. **Call `get_environment` again afterward and check that the hosts are
   listed.** The first Skutt attempt reported success but didn't persist. It can
   take 30 seconds to a few minutes before the session can reach the site; retry
   with a short background loop.
3. Tools: Shopify `graphql_query` / `graphql_mutation`. The theme tools
   (`theme_bash`) are **not** permitted on this store's live theme, so all of this
   is done through metafields. `productByHandle` is deprecated: use
   `productByIdentifier(identifier: {handle: "..."})`.

## 1. Find where the section goes

- Find the brand's collections: `collections(query: "title:*Brand*")`.
  Brands often have duplicates (e.g. `skutt-glass-kilns` and `skutt-glass-kilns-1`).
  Pick the page that's linked from the site navigation and the brand's parent
  page; ask the user if it's unclear.
- Fetch the live page (`curl -sS -A "Mozilla/5.0" -o live.html <url>`) and find
  the block **below the product grid**: section class
  `abz-collection-below-richtext`, div `#abz_below_richtxt_id`. It prints the
  collection metafield **`custom.abz_collection_below_descrption`** (the key is
  misspelled; keep it exactly). It renders raw HTML, `<style>` included.
- `custom.secondary_description` is a legacy copy that the current theme does
  **not** show. Leave it alone unless the user asks.
- The top description (`descriptionHtml`) often has a "Learn more" link to an id
  inside the below block (Skutt: `#SkuttPoetry-guide`). Insert the comparison
  right after that heading so the link lands on it.

## 2. Pull the store's product data

```graphql
query { collection(id: "gid://shopify/Collection/<ID>") { products(first: 100) { nodes {
  title handle status productType onlineStoreUrl
  priceRangeV2 { minVariantPrice { amount } }
  variants(first: 10) { nodes { title } }
  specs: metafield(namespace: "custom", key: "specifications") { value }
  facts: metafield(namespace: "finder", key: "facts") { value }
  eyebrow: metafield(namespace: "finder", key: "eyebrow") { value }
  note: metafield(namespace: "finder", key: "note") { value }
  cone: metafield(namespace: "custom", key: "kiln_top_cone") { value }
  power: metafield(namespace: "custom", key: "kiln_power") { value }
  size: metafield(namespace: "custom", key: "kiln_size") { value }
  box: metafield(namespace: "custom", key: "kiln_box") { value }
} } } }
```

The result is big, so the tool saves it to a file. Summarize it with
`python3 tools/parse_specs.py <file>`. Link only products that are ACTIVE and
have an `onlineStoreUrl`.

## 3. Fact-check against the manufacturer

- Find the manufacturer's current catalog (often a PDF embedded on a "catalogs"
  page; look for `pdfemb-data=` base64 or `.pdf` links in the HTML) and its
  per-model pages. Convert with `pdftotext -layout` and
  `python3 -I tools/html_to_text.py page.html`. Keep downloads in their own folder.
- Check each column: shape/sides, interior size, cubic feet, load capacity (Skutt
  lists "tea bowls" on model pages), max cone/temperature **per voltage and
  phase**, amps, plug (NEMA) or direct wire, brick thickness, special limits
  (e.g. three-phase only).
- When the manufacturer's sources disagree with each other (Skutt's catalog vs.
  its model pages), pick one consistently and note it.
- Write `<brand-line>/FACT-CHECK.md`: sources with URLs, what matched, what you
  corrected, and the store-data errors for the user to fix.

## 4. Draft the section

Start from `template/comparison-section.html` and keep its structure and look:

- Wrap everything in `<div id="sp-<brand>-compare">` and scope **every** CSS rule
  to that id (the template uses `#sp-skutt-compare`; rename it). Class prefix `spc-`.
- `<h2 id="<brand>-kiln-model-comparison"><Brand> Kiln Model Comparison</h2>`, then
  a short intro that says which power basis the specs use (e.g. 240V single-phase).
- A "How to read a <Brand> model number" box, if the brand has a naming system
  (quote the manufacturer's own explanation).
- The table. Pottery columns: Model, Sides, Interior (width × depth), Capacity,
  Tea bowls per load (if published), Max temp, Amps, Hookup, Best for. Glass kilns
  need different columns, e.g. interior W × L × D, shelf/firing area, max temp,
  volts/amps/plug, element placement (lid/sides), best for. Every `<td>` except
  the model cell needs `data-label` (that's what turns rows into cards on
  phones). Mark the best seller with `class="spc-pop"` and a `<span>` badge.
- A footnote on what the ratings assume (voltage/phase) and that 208V or 3-phase
  ratings can differ.
- "Which <Brand> kiln should I buy?" — 3 or 4 picks (`ul.spc-picks`).
- Short notes on the brand's options (brick, controllers, packages), smaller
  kilns, and the phone CTA: (888) 774-2529, "helping potters choose kilns since 1946".
- Plain, specific language; no hype; short sentences.

## 5. Preview

```bash
node tools/preview_shot.js <page-url> '#sp-<brand>-compare' preview draft.html <insert-after-id>
```

Look at both PNGs yourself. `scrollWidth` must equal `innerWidth` on both
(no sideways scrolling). Send the previews to the user with the store-data
problems you found, and wait for their go-ahead.

## 6. Publish (after the user says yes)

1. **Get the current value exactly.** Small values come back inline. For large
   ones, force the tool to save the output to a file by requesting the same
   metafield under ~20 aliases (`a1: metafield(...) { value } a2: ...`), then
   pull it out with python/jq. Also read `compareDigest`.
2. Save it as the backup, and prove it's exact with
   `python3 tools/verify_live.py live.html backup.html` (the live page renders it raw).
3. Build the new value with python (insert the section after the anchor heading,
   assert each anchor occurs exactly once).
4. `metafieldsSet` with `ownerId`, `namespace: "custom"`,
   `key: "abz_collection_below_descrption"`, `type: "multi_line_text_field"`,
   the full new value, and **`compareDigest`** (so Shopify refuses the write if
   someone changed it in the meantime). The value has to be typed out in full in
   the mutation; step 7 catches any transcription mistake.

## 7. Verify

- Fetch the live page with a cache-buster (`?v=$RANDOM`) and run
  `verify_live.py` against the intended value: it must be an exact match.
- Check every link in the section returns 200.
- Screenshot the live section (`preview_shot.js` without the draft args) and send it.

## 8. Save

Put `<brand-line>/live_abz_collection_below_descrption_<date>.html`, the backup,
and `FACT-CHECK.md` in this folder, commit, and push.

## Brands and pages (as of 2026-11-19)

| Brand line | Collection handle(s) | Manufacturer site (confirm) | Status |
|---|---|---|---|
| Skutt pottery | `skutt-ceramic-kilns` | skutt.com | **Done**, on shared blocks since 2026-11-19 (`skutt-pottery` + `kiln-compare-cta`) |
| Skutt glass | `skutt-glass-kilns` (30), `skutt-glass-kilns-1` (14), `skutt-scarb-lampworking-kilns` | skutt.com — catalog: https://skutt.com/skutt-resources/catalogs/glass-kilns/ | Next |
| L&L | `l-l-kilns` + series (`l-l-easy-fire-kilns`, `l-l-jupiter-series-kilns`, `l-l-equad-pro-production-kiln`, …) | hotkilns.com | To do |
| Paragon | `paragon-kilns`, `paragon-pottery-and-ceramics-kilns`, `paragon-glass-kilns` | paragonweb.com | To do |
| Olympic | `olympic-kilns` + series (`olympic-multi-sided-electric-kilns`, `olympic-fl-series-front-loading-commercial-kilns`, …) | greatkilns.com | To do |
| Evenheat | `evenheat-kilns`, `evenheat-ceramics-kilns`, `evenheat-glass-kilns` | evenheat-kiln.com | To do |
| Amaco Excel | `amaco-kilns`, `amaco-excel-kilns` (duplicates) | amaco.com | To do |
| Cone Art | `cone-art-kilns`, `tucker-s-cone-art-kilns`, `cone-art-cone-10-double-wall-automatic-electric-kilns`, `cone-art-glass-fusing-kilns` | coneartkilns.com | To do |
| Nabertherm | `nabertherm-kilns` | nabertherm.com | To do |
| Laguna | `laguna-front-loading-gas-kilns` | lagunaclay.com | To do |

Manufacturer domains in this table are best guesses: confirm each one before
asking to allow it.
