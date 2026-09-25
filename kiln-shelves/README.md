# Kiln shelves: consistent titles and an Experro size filter

This folder standardizes the titles of every kiln shelf in the Shopify catalog
and adds the product data that Experro needs to let customers **filter kiln
shelves by size, shape and thickness**.

## Status: live since 2026-09-25

The plan has been applied to the live store for 65 shelves (every row marked
`approve = yes`):

- **Metafield definitions:** `custom.kiln_shelf_size`, `custom.kiln_shelf_shape`
  and `custom.kiln_shelf_thickness` were created, each with a fixed list of
  allowed values, filterable in admin and usable in smart collections.
- **Titles and SEO titles:** all 65 were updated. Handles and URLs are
  unchanged.
- **Filter values:** 195 were set, three per shelf.
- **Category tags:** added to 32 shelves. Collection counts went up:

  | Collection | Before | After |
  |---|---|---|
  | Kiln Shelves and Posts | 94 | 114 |
  | Kiln Room | 174 | 206 |
  | ADVANCER Silicon Carbide Kiln Shelves | 14 | 25 |

Afterwards, every shelf was read back from Shopify and compared with
`plan.csv`: title, SEO title, filter values, handle, status and tags. They all
matched, and no existing tag was removed.

**Still to do:**

- **Set up the filter in Experro.** This can't be done from Shopify; see
  [Setting up the filter in Experro](#setting-up-the-filter-in-experro).
- **Olympic `olympic 21" x 1/2 shelf`:** unchanged until someone confirms what
  it is (see [Review before applying](#review-before-applying)).

`snapshot.json` keeps the titles as they were before the change, so
`restore` can still put them back.

## What was wrong

The catalog has 73 kiln shelves (61 active, 5 draft, 7 archived) across
Advancer, Spectrum, Cedar Heights CoreLite, Gillespie and Olympic. Before the
change, the titles didn't follow one format, so they were hard to compare and
hard to search:

| Old title | Problem |
|---|---|
| `11 x22 x3/4" Rectangle High Alumina Kiln Shelf` | No brand, odd spacing |
| `24" X 12" X 1" Corelite Square Kiln Shelves By Cedar Heights` | A 24 x 12 shelf was labeled "Square" |
| `Advancer Kiln Shelf 22 x 22 x 5/16" ... Rectangle` | A 22 x 22 shelf was labeled "Rectangle" |
| `Advancer Kiln Shelf 20" Full 10 Sided ...` | Thickness was missing |
| `olympic 21" x 1/2 shelf` | Lowercase; unclear whether it's a half shelf or 1/2" thick (still unchanged) |
| Spectrum listed `24" x 12"`, Advancer listed `12 x 24` | The same size was written two ways |

The SEO titles (what Google shows) were worse. Some had the wrong size: both
26 1/2" half shelves said "27 1/2"". Ten Advancer shelves shared one generic
SEO title, eleven had none, and one Spectrum shelf's was just "KILN SHELF".

**21 active shelves weren't in the Kiln Shelves category.** The storefront's
"Kiln Shelves and Posts" collection includes only products tagged
`Kiln Shelves`. Eleven Advancer shelves, all nine Gillespie shelves and the
Olympic shelf didn't have that tag, so they never appeared on the kiln shelf
category page, and a size filter there would have missed them too. The 20
approved shelves now have the tag; the Olympic shelf gets it once its row is
approved.

## The title format

```
<Brand / line> Kiln Shelf - <size> <shape>, <thickness> Thick
```

| Brand / line | Example |
|---|---|
| Advancer | `Advancer Silicon Carbide Kiln Shelf - 12" x 24" Rectangle, 5/16" Thick` |
| Spectrum | `Spectrum High Alumina Kiln Shelf - 21" Half Round, 3/4" Thick` |
| Cedar Heights | `Cedar Heights CoreLite Semi-Hollow Kiln Shelf - 11" x 22" Rectangle, 1" Thick` |
| Gillespie | `Gillespie Hollow Core Kiln Shelf - 20 3/4" Half 10-Sided, 3/4" Thick` |
| Crystolon | `Crystolon Oxide-Bonded Silicon Carbide Kiln Shelf - 12" x 24" Rectangle, 3/4" Thick` |

Rules:

- Rectangles and squares list the **short side first** (`12" x 24"`, never
  `24" x 12"`), so the same size reads the same across brands.
- Round and multi-sided shelves list the diameter, then `Full` or `Half` and
  the shape (`21" Half Round`, `20" Full 10-Sided`).
- Fractions are written `15 1/2"`, not `15.5"`.
- SEO titles use the industry "L x W x T" form that people type into Google,
  with `| Sheffield Pottery` added when it fits in 70 characters:
  `Advancer Kiln Shelf 12" x 24" x 5/16" Rectangle | Sheffield Pottery`.
- **URLs (handles) do not change**, so existing links, Google rankings and ads
  keep working.

## The size filter

Each shelf gets three product metafields. Each has a fixed list of allowed
values, the same setup the store already uses for `custom.kiln_type` and
`custom.voltage`:

| Metafield | Filter label | Values |
|---|---|---|
| `custom.kiln_shelf_size` | Shelf Size | `10" x 20"` … `24" x 24"` for rectangles/squares; `13" Diameter` … `26 1/2" Diameter` for round and multi-sided |
| `custom.kiln_shelf_shape` | Shelf Shape | Full Round, Half Round, Full 8-Sided, Half 8-Sided, Full 10-Sided, Half 10-Sided, Half 12-Sided, Rectangle, Square |
| `custom.kiln_shelf_thickness` | Thickness | `5/16"`, `5/8"`, `3/4"`, `1"` |

A customer with a 23" ten-sided kiln picks **21" Diameter**, and sees every
21" full and half shelf from every brand. They can then narrow by Shape
(Half 10-Sided) or Thickness. Someone replacing a 12 x 24 shelf picks
**12" x 24"** and gets Advancer, Spectrum, CoreLite, Gillespie and Crystolon
side by side.

Full value list, in the order to show them:

- **Shelf Size:** 10" x 20", 10 1/2" x 21", 11" x 22", 12" x 12", 12" x 24",
  13" Diameter, 13" x 16", 13" x 26", 14" x 18", 14" x 28", 15" Diameter,
  15 1/2" Diameter, 16" Diameter, 16" x 16", 18" x 18", 18" x 24",
  20" Diameter, 20" x 20", 20 3/4" Diameter, 21" Diameter, 22" x 22",
  24" x 24", 25" Diameter, 26" Diameter, 26 1/2" Diameter
- **Shelf Shape:** Full Round, Half Round, Full 8-Sided, Half 8-Sided,
  Full 10-Sided, Half 10-Sided, Half 12-Sided, Rectangle, Square
- **Thickness:** 5/16", 5/8", 3/4", 1"

## Files

| File | What it is |
|---|---|
| `plan.xlsx` / `plan.csv` | The review sheet. One row per shelf: current vs. new title and SEO title, the three filter values, tags to add, and notes. Red rows need a decision; yellow rows have a note worth reading. |
| `snapshot.json` | Every kiln shelf's title, SEO title, tags and collections as they were on 2026-09-24. `restore` uses it to put titles back. |
| `experro-synonyms.csv` | Search synonyms for Experro, so `12x24`, `24 x 12` and `10.5x21` find the right shelves. |
| `../scripts/kiln_shelves.py` | Builds the plan and applies it through the Shopify Admin API. |

## Review before applying

This section describes the review done before the 2026-09-25 apply. Use the
same steps when you re-run the plan for new shelves.

Open `plan.xlsx` (or `plan.csv`) and check the `new_title` and filter columns.
To skip a shelf, set `approve` to `no`. You can also edit any proposed title or
value in the CSV; `apply` uses whatever the CSV says.

These rows need a decision or a fact check:

1. **Olympic `olympic 21" x 1/2 shelf`** (SKU OLHS21, marked `approve = no`).
   The listing doesn't say whether this is a 21" *half* shelf or a 21" shelf
   that's 1/2" thick, or whether it's round or 10-sided. At $59 it's most
   likely a half shelf. Fill in `shelf_shape`, `shelf_thickness` and
   `new_title`, then set `approve` to `yes`.
2. **Advancer 20", 21" and 26" multi-sided shelves.** Their titles don't give
   a thickness. The plan uses 5/16", Advancer's standard thickness. Confirm.
3. **CoreLite 16" x 15" octagon.** Filed under `16" Diameter`. Confirm that's
   the dimension a customer would measure.

The notes column also flags problems in the product *descriptions* that the
title change doesn't fix:

- Spectrum 13 x 26 x 3/4 says 1" thick.
- The Advancer 13 x 26 and 14 x 28 descriptions open with the wrong size.
- The meta descriptions on both 26 1/2" half shelves say 28 1/2".
- A few vendor part numbers are duplicated between products.

## Applying

Run these from the repo root:

```bash
export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx   # needs read_products + write_products

python3 scripts/kiln_shelves.py apply             # dry run: prints every change
python3 scripts/kiln_shelves.py apply --confirm   # writes to Shopify
```

`apply --confirm` does four things, in this order:

1. It creates the three metafield definitions, or adds any new values to them
   if they already exist.
2. It updates the title and SEO title of each approved shelf.
3. It sets the three size-filter metafields on each shelf.
4. It adds the missing category tags (`Kiln Shelves`,
   `Kiln Shelves - Posts - Cones and Kiln Firing Accessories`, and the brand
   collection tag). That puts 20 of the missing shelves in the Kiln Shelves
   category; the Olympic shelf joins once its row is approved. Tags are only
   ever added, never removed. Products hidden by the options app
   (`OPTIONS_HIDDEN_PRODUCT`) and drafts don't get tags.

To apply only some parts, use `--only`, e.g.
`--only metafields,tags` to add the filter without touching titles.

If someone renamed a shelf after the plan was made, `apply` skips that shelf
and prints its name. Pass `--force` to overwrite the rename.

To undo the title changes:

```bash
python3 scripts/kiln_shelves.py restore             # dry run
python3 scripts/kiln_shelves.py restore --confirm
```

This puts titles and SEO titles back to what `snapshot.json` recorded,
overwriting any edits made since. It leaves the metafields and added tags in
place. They're invisible until Experro uses them, and they're harmless.

## Setting up the filter in Experro

The metafields are now on the products, so these steps can be done any time:

1. **Check Experro has the fields.** In Experro's product catalog, open any
   kiln shelf and look for `kiln_shelf_size`, `kiln_shelf_shape` and
   `kiln_shelf_thickness`. If they're missing, re-sync the Shopify catalog.
   If they still don't appear, ask Experro support to add these three
   `custom` product metafields to the Shopify sync. They're built the same way
   as the store's existing `custom.kiln_type` and `custom.voltage` fields, so
   if those already work as Experro filters, these will too.
2. **Add three facets** in Experro's facet settings (Experro's help article
   "Update Facets"):
   - `custom.kiln_shelf_size`, labeled **Shelf Size**
   - `custom.kiln_shelf_shape`, labeled **Shelf Shape**
   - `custom.kiln_shelf_thickness`, labeled **Thickness**

   Use checkbox (multi-select) facets, so a customer can tick two sizes at
   once. If Experro lets you choose which categories a facet appears on,
   show these on Kiln Shelves and Posts, ADVANCER Silicon Carbide Kiln
   Shelves, High Alumina Cone 11 Kiln Shelves, Semi Hollow CoreLite Kiln
   Shelves and Hamill & Gillespie Shelves And Posts. Otherwise they'll only
   appear when the results contain kiln shelves.
3. **Put the values in size order.** Alphabetical order puts `10 1/2"` before
   `10"` and mixes diameters with rectangles. Set a manual order using the
   lists above (Experro's help article "Rearrange facets and facet values").
   Put Shelf Size first, then Shelf Shape, then Thickness.
4. **Add the synonyms** in `experro-synonyms.csv` to Experro's search
   synonyms. Each line is a two-way synonym set. They make `12x24`,
   `24 x 12` and `10.5x21` match titles written `12" x 24"`.
5. **Test** on the storefront:
   - Search `12x24 kiln shelf`: you should get every 12 x 24 shelf.
   - Search `21 half shelf`: you should get the 21" half round and half
     10-sided shelves.
   - Open the Kiln Shelves category and filter Shelf Size = `20" Diameter`:
     you should get 7 shelves (2 Advancer, 2 Gillespie, 3 Spectrum).

## Adding a new shelf later

You can do it either way:

- **By hand in Shopify:** give it a title in the format above, and fill in
  *Kiln Shelf Size / Shape / Thickness* in the product's Metafields section.
  Each field is a dropdown of the allowed values; add a new size under
  Settings > Custom data > Products first. Add the tag `Kiln Shelves`.
- **With the script:** `fetch` pulls the current shelves, `plan` rebuilds the
  sheet (existing shelves show no change), and `apply` pushes the new one. A
  size that's new to the store is added to the metafield's allowed values
  automatically.
