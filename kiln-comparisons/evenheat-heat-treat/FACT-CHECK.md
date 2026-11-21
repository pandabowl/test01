# Evenheat heat treat ovens and small kilns: fact-check

**Status: live since 2026-11-21 (user's OK).** Entries: `evenheat-heat-treat` (`gid://shopify/Metaobject/696365580659`),
`evenheat-lb` (`…/696365613427`), `evenheat-small-kilns` (`…/696365646195`). Lists set as in the table below, and on the
main page [`evenheat-ceramic`, `evenheat-glass`, `evenheat-heat-treat`, `evenheat-lb`, `evenheat-small-kilns`,
`kiln-compare-cta`]. Product `custom.comparison_blocks`: the 13 KH/KO/KF/HT/LT products → `evenheat-heat-treat`,
LB 18/22.5/27 → `evenheat-lb`, STP and both V8 listings → `evenheat-small-kilns` (were `evenheat-glass`; the Copper
keeps `evenheat-glass`). Verified exact on all four live pages; all 22 links return 200.

| Block | File | Pages (proposed `custom.comparison_blocks`) |
|---|---|---|
| `evenheat-heat-treat` | `blocks/evenheat-heat-treat.html` | `evenheat-metal-kilns`: [`evenheat-heat-treat`, `evenheat-lb`, `kiln-compare-cta`] |
| `evenheat-lb` | `blocks/evenheat-lb.html` | `evenheat-kilns-lb-long-blade-heat-treating-ovens`: [`evenheat-lb`, `kiln-compare-cta`] |
| `evenheat-small-kilns` | `blocks/evenheat-small-kilns.html` | `evenheat-pmc-metal-clay-kilns`: [`evenheat-small-kilns`, `kiln-compare-cta`] |

Main `evenheat-kilns` page (lists every Evenheat block): [`evenheat-ceramic`, `evenheat-glass`,
`evenheat-heat-treat`, `evenheat-lb`, `evenheat-small-kilns`, `kiln-compare-cta`].

Picks come before the table (the site-wide order since 2026-11-19 07:4x UTC). No claim about how
long Sheffield has sold kilns.

## Sources (read 2026-11-19)

- Evenheat series pages (each holds the specs for every model in the series):
  https://www.evenheat-kiln.com/kh-knife-ovens, /ko-knife-ovens, /lb-knife-ovens,
  /kf-extreme-knife-ovens, /ht-knife-ovens, /lt-tempering-ovens
- Small kilns: https://www.evenheat-kiln.com/studio-pro-stp, /v8-vitrigraph
- Controls: https://www.evenheat-kiln.com/controls

## What's on the page, and where each claim comes from

- Inside (depth × width × height), cu ft, max temp, volts/amps, plug: each series page's
  Specifications. KO is **2350°F (1288°C)**; KH, LB and KF 2200°F; HT 2000°F; LT 1200°F.
- Side-opening (swing-out) doors: KH, KO, LB, HT and LT pages; KF has "dual doors, front and back".
- "Built completely of firebrick": KH page ("Like all our heat treat ovens"). KO: "thicker firebrick
  structure ... more speed and power per cubic foot for high mass loads".
- Quiet Drive solid-state relays standard: KH, KO, LB, KF, HT and LT pages.
- Side-only elements: LB, KF ("share the side-element-only design of the LB Series") and KH 418.
  KH 414 has a wrap-around element design with a back-wall element.
- KH: about twice as long to reach temperature as a comparable 240V model; 120V only (100V by
  request). KO, LB, KF, HT: 200/208/220/230V by request.
- Badges quote Evenheat: KH 418 "our deepest and most popular KH"; KO 18 "our most popular KO";
  KO 27 "our deepest model ... long, heavy work"; LB 18 "our most popular LB model ... the sales
  leader"; LB 22.5 "runs a close second in popularity".
- LB: "Whether you're making culinary, tactical, fixed blades, folders ..."; built from feedback from
  "the knife making community as well as culinary and long-blade makers".
- KF users: "sword makers, volume knife and heat treaters, Damascus steel makers".
- HT: "tool makers to prototypes to color case hardening".
- LT: fits on top of the LB, KO and KF of the same depth, or on a bench; "NOT designed to be placed on
  our KH models"; Icon control.
- Controllers: Icon, TAP II, Rampmaster 3 (KH, KO, LB, KF, HT). Loud Alarm: 80 dB option.
- Small kilns: STP 8"×8"×4.5", 0.17 cu ft, 1800°F, 120V 12A NEMA 5-15, Dual Access, optional 2"×4"
  window, Icon; V8 8"×8"×6.5", 0.24 cu ft, 2300°F, 120V 12A NEMA 5-15, stackable, vitrigraph base
  with 2-3/4" hole, pots up to 7-1/2", base without the hole for other glass and ceramic work.
- Evenheat's site lists metal clay among its markets but no longer says which model is for metal
  clay, so the block says only "small kilns for metal clay, jewelry and glass" (the store's own page
  grouping) and gives each kiln's maximum temperature. The Copper has no Evenheat spec page; it is
  named with no numbers.

## Errors found in the store's data (not fixed; for the user)

| Product / place | Field | Store says | Evenheat says |
|---|---|---|---|
| KO-18, KO-22.5, KO27 | descriptions | 2400°F (1316°C) | **2350°F (1288°C)** |
| KO-18, KO27, KO-22.5 | finder notes | "2400°F" | **2350°F** |
| KO-22.5 | description and finder note | "the deepest" KO | **KO 27** is the deepest |
| KO27 | description | opens with the KO 22.5's paragraph ("The KO 22.5 ... is the deepest") | — |
| KO-22.5 | finder facts / description | "Test size" / 0.64 cu ft | **0.65 cu ft** |
| HT-1 | description plug | NEMA 6-20P | **NEMA 6-30** |
| LB 18/22.5/27, KF 31.5–49.5 | descriptions | 6.5" high | **6.25"** |
| LB22.5 | description | "standard equipped with 3 key digital controller" | Current controls: Icon, TAP II, Rampmaster 3 |
| Main `evenheat-kilns` page | overview table and heat-treat cards | KO "2400°F", "Up to 2400°F", "Genesis or TAP" | **2350°F**; Icon, TAP II, Rampmaster 3 |
| `evenheat-metal-kilns` below text | "KO: 3\" Brick, High Temperature 2400F"; "six types" (lists seven, incl. "Artisan"); Set-Pro/RM3/Genesis/TAP | | 2350°F, "thicker firebrick" (no thickness given); current controls as above |
| `evenheat-kilns-lb-long-blade-heat-treating-ovens` text | "Standard equipment ... 3 key SetPro Controller"; Quiet Drive "recommended" | | Quiet Drive is standard on LB; current controls as above |
| Studio Pro STP | finder note / SEO | "10 preset metal clay programs" | Not on Evenheat's current page (STP comes with the Icon) |
| `evenheat-pmc-metal-clay-kilns` below text | "Set Pro 3 key controller has 15 preset metal clay programs" | | Not on Evenheat's current pages |
