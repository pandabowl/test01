# AMACO / Brent 2027 price list vs. Shopify

AMACO's 2027 retail price list (effective **Jan 1, 2027**) compared against
every Sheffield Shopify product with vendor Amaco or Brent, or an AMACO
(`039672…`) barcode: 174 products / 808 variants, pulled Nov 24, 2026.

**Nothing has been written to Shopify.** The workbook is for review.

## The workbook: `AMACO_Brent_2027_Shopify_Review.xlsx`

| Tab | What it's for |
|---|---|
| Summary | Counts and how to read the rest |
| Jan 1 Price Update | 364 variants where our price = AMACO 2026 list → move to 2027 list. Brent wheels excluded (on hold). |
| Price Review | 29 variants where our price ≠ list, needs a decision. Includes likely data errors (Easy-Lift kit prices look swapped; $709 "standard die set" vs $89 list). |
| GTIN & MPN | Per-variant barcode (AMACO UPC → Google GTIN) and AMACO Item # (→ MPN). 538 live variants can get a barcode they don't have today. |
| AMACO Discontinued | Live on our site, but on AMACO's "Discontinued & FD" tab (all LUG 2 oz, the Shino line, many Celadon 10 lb pails…) |
| Not on AMACO 2027 List | Live variants that aren't in the list at all, so there's no 2027 price for them |
| Data Issues | Wrong or duplicate barcodes, test values in MPN fields, a duplicate UPC in AMACO's own sheet, etc. |

## How variants were matched

In order of strength:

1. **Barcode**: Shopify barcode (restoring a stripped leading zero) = AMACO UPC.
2. **Part #**: product metafield `custom.pdp_vendor_part_no` (or SKU `A#####X`)
   = AMACO Item # (single-variant products only).
3. **Glaze code + size**: e.g. variant `V-301 IVORY BEIGE / PINT` ↔ sheet
   `Ug Liq V-301 Pt Ivory Beige` (37501K). Every code match was also checked
   for an overlapping colour name.
4. Two hand-checked matches in `MANUAL` in `scripts/match.py`.

No variant matched two different AMACO items. Barcode-only hits on class
packs and bundles are treated as wrong barcodes, not matches.

## Re-running

```bash
python3 scripts/match.py data/AMACO-brent_2027_Retail_Price_List_effective_January_1.xlsx data/shopify_amaco_brent_variants_2026-11-24.json /tmp/amaco
```

```bash
python3 scripts/plan.py /tmp/amaco
```

```bash
python3 scripts/build_xlsx.py /tmp/amaco AMACO_Brent_2027_Shopify_Review.xlsx
```

`data/shopify_amaco_brent_variants_2026-11-24.json` is a snapshot. Re-pull it
from Shopify before applying anything on Jan 1, because prices may have
changed since.

## Where things live in Shopify

- Barcode / GTIN: variant `barcode`.
- MPN: today only product-level `custom.pdp_vendor_part_no`, a single part # per
  product, so a 47-colour glaze product carries one part # for every variant.
  Variant-level options are `mm-google-shopping.mpn` ("Google: MPN", used by
  the Google & YouTube channel) and `custom.pdp_mpn_number` (theme spec field).
