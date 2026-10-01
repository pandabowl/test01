# Kiln Shelf Size Filter Handoff

As of October 1, 2026

The Shopify side is finished and checked: all 65 active and draft kiln shelves have consistent titles and size, shape and thickness filter values. What's left is switching the filters and search synonyms on in Experro, and identifying one Olympic shelf.

## Done in Shopify

All Shopify work is finished. Each change was read back from the live store and matched the plan.

| Date | Change | Shelves | Result |
| --- | --- | --- | --- |
| 2026-10-01 | Restored meta descriptions | 33 | The Sept 25 update had cleared them by mistake; all restored word for word |
| 2026-10-01 | Fixed wrong sizes | 5 | 3 descriptions (Spectrum 13 x 26 x 3/4", Advancer 13 x 26, Advancer 14 x 28) and 2 meta descriptions (both 26 1/2" half shelves) |
| 2026-10-01 | Moved the CoreLite octagon | 1 | Retitled 15" x 16" and filed under 15" Diameter with the other 15" octagons |
| 2026-09-25 | Standardized titles and SEO titles | 65 | One format across all brands; product URLs unchanged |
| 2026-09-25 | Created and filled the filter fields | 65 | Kiln Shelf Size, Kiln Shelf Shape and Kiln Shelf Thickness: 195 values |
| 2026-09-25 | Added missing category tags | 32 | Kiln Shelves and Posts: 94 to 114 products. Kiln Room: 174 to 206. ADVANCER Silicon Carbide Kiln Shelves: 14 to 25 |

## Experro setup

Nothing has been changed in Experro yet. These steps follow the left-hand menu of Experro Discovery and take about 20 minutes.

- [ ] **Field Settings:** find Kiln Shelf Size, Kiln Shelf Shape and Kiln Shelf Thickness, and turn on their filter or facet option.
  - Not listed: open **Store Connection**, run a sync, then check again.
  - Still missing: ask Experro support to include the Shopify product metafields `custom.kiln_shelf_size`, `custom.kiln_shelf_shape` and `custom.kiln_shelf_thickness` in the catalog sync.
- [ ] **Facets:** open the existing facet set named **All** (Brand, Product Type, Price and 9 more) and add the three facets in the table below. Skip the Add Facet button: it makes a set for one category or collection, which probably replaces All on that page.
- [ ] Make each new facet a checkbox (multi-select) filter, and set its value order to manual using the lists in the next section.
- [ ] Order the facets Shelf Size, then Shelf Shape, then Thickness, and save.
- [ ] **Search & Autocomplete > Synonyms:** add the 20 synonym groups from the next section, each as one two-way entry.
- [ ] **Cache:** clear it so the storefront picks up the changes, then run the tests below.

| Field to choose | Display name customers see |
| --- | --- |
| Kiln Shelf Size (`custom.kiln_shelf_size`) | Shelf Size |
| Kiln Shelf Shape (`custom.kiln_shelf_shape`) | Shelf Shape |
| Kiln Shelf Thickness (`custom.kiln_shelf_thickness`) | Thickness |

A facet only appears when the products on screen have a value for it, so these show on kiln shelf pages and searches and stay hidden everywhere else.

## Values to enter in Experro

The filter values come from the products automatically; only their order and the synonyms are entered by hand. Skip any value Experro doesn't list: 14" x 18" and 10 1/2" x 21" are only on shelves hidden from the storefront.

**Shelf Size**, smallest first:

1. 10" x 20"
2. 10 1/2" x 21"
3. 11" x 22"
4. 12" x 12"
5. 12" x 24"
6. 13" Diameter
7. 13" x 16"
8. 13" x 26"
9. 14" x 18"
10. 14" x 28"
11. 15" Diameter
12. 15 1/2" Diameter
13. 16" x 16"
14. 18" x 18"
15. 18" x 24"
16. 20" Diameter
17. 20" x 20"
18. 20 3/4" Diameter
19. 21" Diameter
20. 22" x 22"
21. 24" x 24"
22. 25" Diameter
23. 26" Diameter
24. 26 1/2" Diameter

**Shelf Shape:**

1. Full Round
2. Half Round
3. Full 8-Sided
4. Half 8-Sided
5. Full 10-Sided
6. Half 10-Sided
7. Half 12-Sided
8. Rectangle
9. Square

**Thickness:**

1. 5/16"
2. 5/8"
3. 3/4"
4. 1"

**Synonyms**, one two-way group per line, so that 12x24, 24 x 12 or 10.5x21 finds titles written 12" x 24":

```text
10x20, 10 x 20, 20x10, 20 x 10
10.5x21, 10.5 x 21, 21x10.5, 21 x 10.5, 10 1/2 x 21, 21 x 10 1/2
11x22, 11 x 22, 22x11, 22 x 11
12x12, 12 x 12
12x24, 12 x 24, 24x12, 24 x 12
13x16, 13 x 16, 16x13, 16 x 13
13x26, 13 x 26, 26x13, 26 x 13
14x18, 14 x 18, 18x14, 18 x 14
14x28, 14 x 28, 28x14, 28 x 14
16x16, 16 x 16
18x18, 18 x 18
18x24, 18 x 24, 24x18, 24 x 18
20x20, 20 x 20
22x22, 22 x 22
24x24, 24 x 24
8-sided, 8 sided, octagon, octagonal
10-sided, 10 sided, decagon
12-sided, 12 sided, dodecagon
silicon carbide, sic
semi-hollow, semi hollow, hollow core
```

## Testing

After clearing the cache, try these on the live site. Searches may also show other products; the shelves listed should be among the results.

| Try | Expected |
| --- | --- |
| Search: 12x24 kiln shelf | 5 shelves: the Advancer, Crystolon, CoreLite, Gillespie and Spectrum 12" x 24" |
| Search: 24 x 12 kiln shelf | The same 5 shelves (checks the synonyms) |
| Kiln Shelves and Posts, Shelf Size = 15" Diameter | 6 shelves: 3 Advancer, 2 CoreLite (one is the octagon), 1 Gillespie |
| Kiln Shelves and Posts, Shelf Size = 20" Diameter | 7 shelves: 2 Advancer, 2 Gillespie, 3 Spectrum |
| Kiln Shelves and Posts, Shelf Size = 21" Diameter | 4 shelves: Advancer full and half 10-sided, Spectrum full and half round |
| Same, plus Shelf Shape = Half 10-Sided | 1 shelf: the Advancer 21" Half 10-Sided |

## Open items

- [ ] **Olympic shelf, SKU OLHS21** (titled "olympic 21" x 1/2 shelf", $59): still unchanged, has no filter values, and isn't on the Kiln Shelves page. Someone needs to check the actual shelf: half or full, round or 10-sided, and how thick. Then in Shopify:
  - Retitle it in the standard format, for example: `Olympic Kiln Shelf - 21" Half Round, [thickness] Thick`.
  - Set Kiln Shelf Size to 21" Diameter, plus its Kiln Shelf Shape and Kiln Shelf Thickness.
  - Add the tags Kiln Shelves, Kiln Shelves - Posts - Cones and Kiln Firing Accessories, and Olympic Kiln Shelves and Furniture Kits.
- [ ] **Duplicated vendor part numbers** in the vendor part no. field. The correct numbers need to come from the supplier:
  - Advancer 21" Full 10-Sided shows AKS-ADV2020F10S-1, the 20" shelf's number.
  - Advancer 13" x 16" shows AKS-ADV1326X5/16-I, the 13" x 26" shelf's number.
  - Spectrum 20" Half Round and 20" Half 10-Sided both show #20H.

## Reference

**Title format:** `[brand or line] Kiln Shelf - [size] [shape], [thickness] Thick`. For example: Advancer Silicon Carbide Kiln Shelf - 12" x 24" Rectangle, 5/16" Thick.

- Rectangles and squares put the short side first: 12" x 24", never 24" x 12".
- Round and multi-sided shelves give the diameter, then Full or Half and the shape: 21" Half Round, 20" Full 10-Sided.
- Fractions are written 15 1/2", not 15.5".

**Adding a new shelf in Shopify:**

1. Title it in the format above.
2. In the product's Metafields section, pick its Kiln Shelf Size, Kiln Shelf Shape and Kiln Shelf Thickness from the dropdowns. A size that isn't listed is added first under Settings > Custom data > Products > Kiln Shelf Size.
3. Add the tags Kiln Shelves and Kiln Shelves - Posts - Cones and Kiln Firing Accessories, plus the brand tag: ADVANCER Kiln Shelves, High Alumina Cone 11 Kiln Shelves or Semi Hollow CoreLite Kiln Shelves.

**Records** are in the GitHub repo [pandabowl/test01](https://github.com/pandabowl/test01/tree/claude/compassionate-goodall-iay7ps), branch `claude/compassionate-goodall-iay7ps`:

| File | What it holds |
| --- | --- |
| `kiln-shelves/README.md` | Full project notes, including the Experro steps |
| `kiln-shelves/plan.xlsx` | Every shelf's old and new title, SEO title and filter values |
| `kiln-shelves/changes-2026-10-01.json` | Exact before and after text of the Oct 1 edits, for undoing them |
| `kiln-shelves/snapshot.json` | Titles as they were before Sept 25, used to restore them |
| `scripts/kiln_shelves.py` | Script that rebuilds the plan and applies it through the Shopify API |
