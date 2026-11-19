# Evenheat store-data fixes (2026-11-19)

The user asked to fix the store-data errors found during the Evenheat fact-check
(see `../evenheat-ceramics/FACT-CHECK.md` and `../evenheat-glass/FACT-CHECK.md`).
Every value was backed up before it was overwritten (`backup_before_2026-11-19/`,
including the raw GraphQL result with compare digests). The intended new values are in
`fixed_2026-11-19/`. After writing, every value was read back from Shopify and matched
byte for byte (`fixed_2026-11-19/after_query_result.json`). The three collection
below-grid values were also checked on the live pages with `tools/verify_live.py`.

Source for every number: Evenheat's model pages on evenheat-kiln.com (read 2026-11-19).

## Product descriptions (`descriptionHtml`)

| Product | Change |
|---|---|
| RM II 810 (`...-everm810`) | The description was the **HF 810's** text: HF name throughout, the HF outside size and weight, 3" firebrick paragraphs, and "cone 5 (2300°F)". Rewrote it from Evenheat's RM 810 page: cone 5-1/2 (2200°F/1204°C), outside 22.50" D × 16.25" W × 22" H, 50 lb, no 3" brick section, "RM 810" throughout, plus "100V by request". |
| V8 with Vitrigraph Base (`...-evev8v`), V8 Base Optional (`...-evev8`) | 2350°F → **2300°F**; 120V 14A/1680W → **12A/1440W** (both places); pot size 7.25" → **7-1/2"** (both places). |
| Studio Pro 14 : 120 Volt | Plug NEMA 5-15P → **NEMA 5-20P**. |
| GTS 41 | Outer dimensions 30.25" × 56" × 29.5" (the GTS 2541's) → **35.5" L × 45.5" W × 37" H (90 × 115.5 × 94 cm)**. |
| Studio Pro 41 | "884 sq. inches" shelf (twice, with "39.3 at its widest") → Evenheat's current **38" × 22-5/8" × 1"** full shelf, plus the 19-1/8" × 23-1/4" half-shelf set. |
| GTS 18-13 | 6460W → **6480W**. |

## Titles and SEO

- RM II 810: title and SEO title "Cone 5" → **"Cone 5-1/2"**. (Its SEO meta description was
  briefly cleared by that update and then restored word for word from the backup.)
- HF 1210B: the SEO meta description described the **RM II 810** ("Cone 5.5 Kiln"). Replaced
  with: "Evenheat HF 1210B is a small 240 volt kiln built with 3" firebrick and rated to
  cone 10 (2350°F), for porcelain bisque and china painting."

## Finder metafields

- `finder.eyebrow` "… · 240/208 V" → "… · 240 V" on the 14 kilns whose Evenheat pages don't
  list 208V: RM II 1210B, 1413, 1813, 1822, 2322, 2329, 2922, 2929, 2522, 2541 and HF 1210B,
  1413, 1813, 1818. (HF 2318/2327/2918/2927 keep 240/208 V; Evenheat builds them for 208V.)
- `custom.kiln_power` was **not** changed: its definition only allows "120 V",
  "240 or 208 V" and "Gas or propane", so it's a store-wide filter bucket, not a spec.
  Shopify rejected "240 V". `custom.voltage` is the same kind of filter ("120 Volt" /
  "240 or 208") and was left alone too.
- RM II 810: eyebrow "Cone 5 · 120 V" → "Cone 5½ · 120 V"; note → "A 120 V cone 5½ kiln for
  china paint, tests and small work." (`custom.kiln_top_cone` stays 5; it's an integer filter.)
- Studio Pro 14 120V: facts "Top-loading · Test size" → "Front-loading · 0.8 cu ft".
- Studio Pro 41: note → "Front and top access to a 40.5 by 25.25 inch chamber, with a
  seamless one-piece shelf."
- GTS 23 note → "A 23.5 inch wide, all-firebrick glass kiln that holds one big 21 inch shelf."
- GTS 18-13 note → "An all-firebrick top-loader that fires one 15.5 inch shelf in a small
  footprint." (Both dropped "top and side" elements, which Evenheat's pages don't state.)

## Collection text

- `evenheat-ceramics-kilns`: "Eveheat" → "Evenheat" (description and below text); "five
  families" → "three", removing the discontinued Evolution and Classic series; controller
  list Set-Pro/RM3/Genesis/TAP → Evenheat's current Rampmaster II, TAP II, Icon+, Icon
  (TAP I on multi-zone HF).
- `evenheat-glass-kilns`: "Eveheat" typo; V8 pot 7.25" → 7-1/2"; removed the "Studio Pro 15"
  and "Fishbone" lines (not in Evenheat's lineup); "the largest glass kiln for 120 volt 20
  amp" → "Evenheat's largest …"; controller list → Rampmaster 3, TAP II, Icon+, Icon
  ("options vary by model"); Quiet Drive now noted as standard on Studio Pro, GTS and V8.
- `evenheat-pmc-metal-clay-kilns`: description "Here you will find Eveheat glass kilns" →
  "Here you will find Evenheat PMC metal clay kilns".
- `evenheat-kilns` (main page overview table): Small & Specialty "1800–2350°F" →
  "1800–2300°F"; "(the 810s need a 20A circuit)" → "(the 810s and the RM II 1210 need a 20A
  circuit)".

New compare digests after the fixes: ceramics below `a99308f1…`, glass below `bf76e5b3…`,
main below `c5cb40dc…`. Re-read the values before publishing the comparison sections.

## Left as is (not errors we could fix from Evenheat's data, or out of scope)

- Older controller names (Set-Pro, Genesis, TAP) inside several product descriptions
  (GTS 18, GTS 41, Studio Pro 14/41, V8) and the PMC page's below text.
- "Top and Side Fire Configuration" sections in the GTS 18/41 descriptions (older Evenheat
  copy; Evenheat's current pages don't say where the elements are).
- Studio Pro 14/17 240V specs (10A, 2400W) and all Copper specs: not on Evenheat's pages.
- Studio Pro 28 finder note "shipped in two sections for tight halls": not on Evenheat's page.
- Generic SEO descriptions ("great choice for a small studio or as test kiln") on large RM/HF
  kilns, handles with old names, the DRAFT duplicate GTS 23 product.
