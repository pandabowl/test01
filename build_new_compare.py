# -*- coding: utf-8 -*-
"""Add a 'new compare' column to the Sheffield store export, populated from the
2026 Olympic pricelist we built. Prices are looked up from the workbook by key,
never re-typed."""
import csv, re, html, openpyxl

SRC_CSV = "/root/.claude/uploads/fee27d32-e784-56b7-9d28-abaa5e92df20/aeb5f0dd-olympic-oct26-title-down.csv"
PRICELIST = "/home/user/test01/Olympic_Kilns_2026_Pricelist.xlsx"
OUT_CSV = "/home/user/test01/olympic-oct26-new-compare.csv"
OUT_AUDIT = "/home/user/test01/olympic-new-compare-audit.xlsx"

wb = openpyxl.load_workbook(PRICELIST, data_only=True)
kiln = {r[1]: (r[3], r[2]) for r in wb["Kilns"].iter_rows(min_row=2, values_only=True)}
kit = {(r[0], r[1]): r[4] for r in wb["Furniture Kits"].iter_rows(min_row=2, values_only=True)}
acc = {}
for r in wb["Accessories"].iter_rows(min_row=2, values_only=True):
    acc.setdefault(r[0], []).append((str(r[1] or ""), r[2]))
shelf = {r[0]: r[4] for r in wb["Kiln Shelves"].iter_rows(min_row=2, values_only=True)}
relay = {r[0]: {"1ph": r[2], "zone": r[3], "3ph": r[4]} for r in wb["Solid State Relays"].iter_rows(min_row=2, values_only=True)}

def K(model):                       # kiln base price
    p, ctl = kiln[model]
    return p, f"Kilns: {model} (base = {ctl})"
def F(section, fits):               # furniture kit
    return kit[(section, fits)], f"Furniture Kits: {section} — {fits}"
def A(item, want=""):               # accessory (want = substring of its description)
    cands = [(d, p) for d, p in acc[item] if want.lower() in d.lower()]
    assert len(cands) == 1, (item, want, cands)
    d, p = cands[0]
    return p, f"Accessories: {item}" + (f" ({d[:38]})" if len(acc[item]) > 1 else "")
def S(name):
    return shelf[name], f"Kiln Shelves: {name}"
def R(amps, col, label):
    return relay[amps][col], f"Solid State Relays: {amps}, {label}"

# ---- SKU -> pricelist item. ('note' marks anything a human should eyeball) ----
EXACT, LIKELY, REVIEW = "exact", "likely", "review"
M = {}
def m(sku, spec, conf=EXACT, note=""):
    M[sku] = (spec, conf, note)

for sku, model in [
    ("OL1214120","1214-120E"), ("OL1214ERAKU","1214 Raku E"), ("OL129","129E"),
    ("OL1414HE","1414HE"), ("OL146GFETLC","Square 146GFETLC"), ("OL1818","1818E"),
    ("OL1818H","1818HE"), ("OL1823","1823E"), ("OL1823ERAKU","1823 Raku E"),
    ("OL1823H","1823HE"), ("OL1827","1827E"), ("OL1827G","1827G"), ("OL1827H","1827HE"),
    ("OL186GFETLC","Square 186GFETLC"), ("OL18RAKU","18 Raku"), ("OL2318","2318E"),
    ("OL2318H","2318HE"), ("OL2323H","2323HE"), ("OL2327","2327E"), ("OL2327G","2327G"),
    ("OL2327H","2327HE"), ("OL2331G","2331G"), ("OL2331H","2331HE"), ("OL23RAKU","23 Raku"),
    ("OL2818H","2818HE"), ("OL2823H","2823HE"), ("OL2827G","2827G"), ("OL2827H","2827HE"),
    ("OL2831G","2831G"), ("OL2831H","2831HE"), ("OL28RAKU","28 Raku"), ("OLCHAMP","Champ"),
    ("OLCHAMPXL","Champ XL"), ("OLDD9","DD9"), ("OLDD12","DD12"), ("OLDD14","DD14"),
    ("OLDD17","DD17"), ("OLDD20","DD20"), ("OLDD24","DD24"), ("OLDD30","DD30"),
    ("OLDD40","DD40"), ("OLDM1818HE","DM1818HE"), ("OLDM1823HE","DM1823HE"),
    ("OLDM2318HE","DM2318HE"), ("OLDM2323HE","DM2323HE"), ("OLDM2327HE","DM2327HE"),
    ("OLDM2523HE","DM2523HE"), ("OLDM2818HE","DM2818HE"), ("OLDM2823HE","DM2823HE"),
    ("OLDM2827HE","DM2827HE"), ("OLDM3018HE","DM3018HE"), ("OLDM3023HE","DM3023HE"),
    ("OLF1414HE","F1414HE Pkg."), ("OLF1823HE","F1823HE Pkg."), ("OLF2323HE","F2323HE Pkg."),
    ("OLF2327HE","F2327HE Pkg."), ("OLF2527HE","F2527HE Pkg."), ("OLF2823HE","F2823HE Pkg."),
    ("OLF2827HE","F2827HE Pkg."), ("OLFL8","FL8E"), ("OLFL10","FL10E"), ("OLFL12","FL12E"),
    ("OLFL17","FL17E"), ("OLFL20","FL20E"), ("OLFL24","FL24E"), ("OLFL24-old","FL24E"),
    ("OLFL27","FL27E"), ("OLFL31","FL31E"), ("OLFL36","FL36E"), ("OLFL42","FL42E"),
    ("OLFL53","FL53E"), ("OLFL45","FL4.5E"), ("OLFL55","FL5.5E"), ("OLGF2ETLC","GF2ETLC"),
    ("OLGF3ETLC","GF3ETLC"), ("OLHB","HotboxE"), ("OLHB64","HB64E"), ("OLHB84","HB84E"),
    ("OLHB86","HB86E"), ("OLHB86V","HB86 Vitrigraph"), ("OLHB89","HB89E"),
    ("OLMAS1818HE","MAS 1818HE"), ("OLMAS1823HE","MAS 1823HE"), ("OLMAS2323HE","MAS 2323HE"),
    ("OLMAS2327HE","MAS 2327HE"), ("OLMAS2823HE","MAS 2823HE"), ("OLMAS2827HE","MAS 2827HE"),
    ("OLO2018H","2018HE"), ("OLO2023H","2023HE"), ("OLO2027H","2027HE"), ("OLO2518H","2518HE"),
    ("OLO2523H","2523HE"), ("OLO2527H","2527HE"), ("OLO2531H","2531HE"), ("OLO3018H","3018HE"),
    ("OLO3023H","3023HE"), ("OLO3027H","3027HE"), ("OLO3031H","3031HE"), ("OLODT","Doll/Test"),
    ("OLTL20E","TL20E"), ("OLTL5432E","TL5432E"), ("OLTRAV","Traveler"),
]:
    m(sku, lambda mo=model: K(mo))

m("OL1414HE", lambda: K("1414HE"), EXACT,
  'store part no. says "F1414HE" but the listing is the standard 1414HE test kiln, not the Freedom package')
m("OLGF2ETLC", lambda: K("GF2ETLC"), EXACT, 'store part no. says "OL146GFETLC"; listing text is GF2ETLC')
m("OLTL5432E", lambda: K("TL5432E"), EXACT, 'store part no. says "OLTL20E"; listing text is TL5432')
m("OLMAS2823HE", lambda: K("MAS 2823HE"), EXACT, 'store part no. says "OLMAS2323HE"; listing text is MAS 2823HE')
m("OLFL55", lambda: K("FL5.5E"), EXACT, 'listing reads "FL-5"; matched to FL5.5E')

for sku, args in [
    ("OL186GFETLCFK", ("120 Volt Kilns", '18" Square')),
    ("OL146GFETLCFK", ("120 Volt Kilns", '14" Square')),
    ("OLHBFK", ("120 Volt Kilns", "HB64E, HOTBOX E")),
    ("OLHB64E", ("120 Volt Kilns", "HB64E, HOTBOX E")),
    ("OLHB8FK", ("120 Volt Kilns", "HB84E, HB86E, HB89E")),
    ("OLDTFK", ("120 Volt Kilns", "DOLL E/TEST E")),
    ("OL12FK", ("120 Volt Kilns", "129E, 1214-120E, 1214-120HE")),
    ("OLTRAVFK", ("120 Volt Kilns", "TRAVELER")),
    ("OL18HFK", ('18" Wide Kilns', '18" Wide Stackable')),
    ("OL23FK", ('23" Wide Stackable Kilns', '23"')),
    ("OL23HFK", ('23" Wide Stackable Kilns', '23H"')),
    ("OL28FK", ('28" Wide Stackable Kilns', '28"')),
    ("OL28HFK", ('28" Wide Stackable Kilns', '28H"')),
    ("OLGF2ETLCSK", ('20" & 25" Wide Square Kilns', "GF2s")),
    ("OLGF3ETLCSK", ('20" & 25" Wide Square Kilns', "GF3s")),
    ("OL25HOFK", ("Oval Kilns", "2518HE, 2523HE, 2527HE, 2531HE")),
    ("OL30HEFK", ("Oval Kilns", "3018HE, 3023HE, 3027HE, 3031HE")),
    ("OL1214ERAFK", ("Electric Raku & TopHat Kilns", "1214 Raku E")),
    ("OL1823EFK", ("Electric Raku & TopHat Kilns", "1823 E Raku & TopHat 189E")),
    ("OL18RAFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "18 Raku")),
    ("OL23RAFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "23 Raku")),
    ("OL28RAFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "28 Raku")),
    ("OL1827GFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "18 Torchbearer")),
    ("OL2731GFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "23 Torchbearer")),
    ("OL2827GFK", ("UpDraft Gas Kilns (Raku & Torchbearer)", "28 Torchbearer")),
    ("OLDM1823FK", ("Dual Media Kilns", '18/18H"')),
    ("OLDM182327FK", ("Dual Media Kilns", '23H"')),
    ("OLDM2818FK", ("Dual Media Kilns", '28H"')),
    ("OLDM2327FK", ("Dual Media Kilns", '28H"')),
    ("OLDM2523FK", ("Dual Media Kilns", "25H Ovals")),
    ("OLDM301823FK", ("Dual Media Kilns", "30H Ovals")),
    ("OLMAS28SFK", ("Medallion Artist Series", '28H"')),
    ("OLDD9FK", ("DownDraft (DD) Gas Kilns", "DD9")),
    ("OLDD12FK", ("DownDraft (DD) Gas Kilns", "DD12")),
    ("OLDD14FK", ("DownDraft (DD) Gas Kilns", "DD14")),
    ("OLDD17FK", ("DownDraft (DD) Gas Kilns", "DD17")),
    ("OLDD20FK", ("DownDraft (DD) Gas Kilns", "DD20")),
    ("OLDD24FK", ("DownDraft (DD) Gas Kilns", "DD24")),
    ("OLDD30FK", ("DownDraft (DD) Gas Kilns", "DD30")),
    ("OLDD40FK", ("DownDraft (DD) Gas Kilns", "DD40")),
    ("OLTL20FK", ("Large Capacity Kilns", "TL20E")),
    ("OLTL5432FK", ("Large Capacity Kilns", "TL5428E, TL5432E")),
    ("OLFL20FK", ("Large Capacity Kilns", "FL17E, FL20E")),
    ("OLFL45FK", ("Large Capacity Kilns", "FL4.5E")),
    ("OLFL55FK", ("Large Capacity Kilns", "FL5.5E")),
    ("OLFL8FK", ("Large Capacity Kilns", "FL8E, FL10E, FL12E")),
    ("OLFL24FK", ("Large Capacity Kilns", "FL24E")),
    ("OLFL27FK", ("Large Capacity Kilns", "FL27E, FL31E")),
    ("OLFL36FK", ("Large Capacity Kilns", "FL36E")),
    ("OLFL42FK", ("Large Capacity Kilns", "FL42E")),
    ("OLFL53FK", ("Large Capacity Kilns", "FL53E")),
    ("OLFL64FK", ("Large Capacity Kilns", "FL64E")),
]:
    m(sku, lambda a=args: F(*a))

m("OL186GFETLCFK", lambda: F("120 Volt Kilns", '18" Square'), EXACT,
  'the 18" Square kit in the 120-volt section; the 18"-wide stackable kit is $225')
m("OLO20FK", lambda: F("Oval Kilns", "209GFE & 2014GFE"), REVIEW,
  'listing just says "Oval 20"; priced as the glass oval kit. If it is for 2018HE/2023HE/2027HE it is $830')
m("OL23RAKUFK", lambda: F("UpDraft Gas Kilns (Raku & Torchbearer)", "23 Raku"), LIKELY,
  'old compare ($756) matches the 23 Torchbearer kit, not the 23 Raku kit — check which one this SKU really is')
m("OLMAS28SFK", lambda: F("Medallion Artist Series", '28H"'), LIKELY, "MAS 28-series kit")
m("OL18HFK", lambda: F('18" Wide Kilns', '18" Wide Stackable'), LIKELY,
  'listing says "Standard 18\\" Electric Kiln"; the 18" square-kiln kit is $225')

for sku, args, conf, note in [
    ("OLECBR20", ('20/20H" Blank Ring',), LIKELY, "3 store SKUs map to this one ring"),
    ("OL20BR", ('20/20H" Blank Ring',), LIKELY, "3 store SKUs map to this one ring"),
    ("OL2018BR", ('20/20H" Blank Ring',), EXACT, '$480 confirmed by Sheffield Pottery (20" oval ring), despite the "1.98 cu ft" in the listing'),
    ("OLECBR25", ('25/25H" Blank Ring',), LIKELY, ""),
    ("OLECBR30", ('30/30H" Blank Ring',), LIKELY, ""),
    ("OL30BR", ('30/30H" Blank Ring',), LIKELY, ""),
    ("OL18BR", ('18" Blank Ring',), EXACT, ""),
    ("OL18BRH", ('18H" Blank Ring',), EXACT, ""),
    ("OL23BR", ('23" Blank Ring',), EXACT, ""),
    ("OL23HBR", ('23H" Blank Ring',), EXACT, ""),
    ("OL28HBR", ('28/28H" Blank Ring',), EXACT, ""),
    ("OLPEEP", ("Observation Plugs",), EXACT, ""),
    ("OLSTYPE", ("Type S Thermocouple", "Studio"), LIKELY, ""),
    ("OLHBP", ("Pyrometer Digital", "Studfio Kilns"), REVIEW, 'listing is "pyrometer for hot box"; priced as the studio digital pyrometer'),
    ("OLDP", ("Pyrometer Digital", "Studfio Kilns"), EXACT, ""),
    ("OLDDDP10", ("Pyrometer Digital", "Large Capacity"), EXACT, ""),
    ("OES", ("Electro Sitter", "KilnStar"), LIKELY, "Genesis 2.0 version is $1,450"),
    ("OLK3K", ("Electro Sitter", "KilnStar"), REVIEW, '"3 Key Base Model" — the 2026 list only has KilnStar ($1,250) and Genesis ($1,450)'),
    ("OLHLC", ("High Limit Controller",), EXACT, "listing text matches the pricelist wording"),
    ("OLHLC120", ("High Limit Controller",), LIKELY, "120V version; the list shows one price"),
    ("OLDDEC", ("High Limit Controller",), REVIEW, "electronic shut-off w/ valve; closest item in the 2026 list"),
    ("OLDDBB", ("Blower Burner 200k (per burner)", "Burner on Kiln"), REVIEW, "stand-alone burner version is $1,700"),
    ("OLDDGH", ("Vent Hood - DownDraft Kilns", "Galvanized"), EXACT, ""),
    ("OLGH", ("Vent Hood - DownDraft Kilns", "Galvanized"), EXACT, ""),
    ("OLDDSH", ("Vent Hood - DownDraft Kilns", "Stainless"), EXACT, ""),
    ("OLHOSS", ("Vent Hood - DownDraft Kilns", "Stainless"), EXACT, ""),
    ("OLHSSUPD", ('Vent Hood for 18" & 23" kilns',), EXACT, ""),
    ("OLSSH4040", ('Vent Hood for 28" kilns',), EXACT, ""),
    ("OLWINDOW24", ("Quartz Glass Viewing Window", "Rectangle"), EXACT, ""),
    ("OLWINDOW2R", ("Quartz Glass Viewing Window", "Round"), EXACT, ""),
    ("OLLPR18", ('Low Pressure Regulator 18"',), EXACT, ""),
    ("OLL23PR", ('Low Pressure Regulator 23" & 28"',), EXACT, ""),
    ("OLEK3Z", ("3 Zone Control",), EXACT, "2-zone control is $150"),
    ("OL3ZONE", ("3 Zone Control",), EXACT, "2-zone control is $150"),
    ("OLCEK3Z", ("3 Zone Control",), LIKELY, 'listing says "zone control" without a count; 2-zone is $150'),
    ("OL480V", ("480 volt",), EXACT, ""),
    ("OLLSS", ("Automatic Lid Shut-off",), EXACT, ""),
    ("OLLSO", ("Automatic Lid Shut-off",), EXACT, ""),
    ("OLDME", ("Dual Media (DM) Lid Element",), LIKELY, ""),
    ("OLLA", ("Lid Assist",), EXACT, "retro-fit version is $750"),
    ("OLCWLS", ("Lid Assist",), REVIEW, '"counter weight lid system" priced as Lid Assist; retro-fit is $750'),
    ("OLVSSEK", ("VentMaster",), EXACT, ""),
    ("OLDVC", ("VentMaster",), EXACT, ""),
    ("OLVMEK", ("VentMaster Expansion Kit",), EXACT, ""),
    ("OLEKC", ("Castors-Studio Kilns",), EXACT, "large-capacity castors are $450"),
]:
    m(sku, lambda a=args: A(*a), conf, note)

m("OLO2023H", lambda: K("2023HE"), EXACT,
  "the 2026 list price is $60 BELOW the old compare-at, unlike every other oval — worth a sanity check")
m("OLHS21", lambda: S('23" Half Shelf'), REVIEW,
  'read as a 21" half shelf; if it is the full 21" round shelf it is $105')
m("OLHB89SHELF", lambda: S("HB84,HB86, HB89 Shelf"), EXACT, "")

m("OLSSR17", lambda: R("76-100 Amps", "1ph", "1 phase"), EXACT,
  "$650 confirmed by Sheffield Pottery — relays are priced by amperage and FL17/FL20/FL24 all draw 70-98A")
m("OLSSR173P", lambda: R("76-100 Amps", "3ph", "3 phase"), LIKELY,
  "same 76-100A band as OLSSR17, which Sheffield confirmed at $650")
m("OLFL24-old", lambda: K("FL24E"), EXACT, "listing is marked ARCHIVE — priced the same as the current FL24 listing")
m("OLDDEC", lambda: A("High Limit Controller"), LIKELY,
  'listing is the 120V/20A electronic high-limit shut-off with valve; the list has one High Limit Controller price')

THREE_PH = "Accessories: 3 Phase Wiring-Studio Line/Large Capacity"
for sku in ("OLDM3P", "OLPHASE3"):
    m(sku, lambda: (110, THREE_PH + " — studio line"), EXACT, 'list cell reads "$110/$450"')
for sku in ("OL3PCK", "OLPHASE3C"):
    m(sku, lambda: (450, THREE_PH + " — large capacity"), EXACT, 'list cell reads "$110/$450"')

m("OLGENESIS", lambda: (150, "Kilns: Genesis upgrade"), REVIEW,
  "Genesis adds $150 on most models, but it varies by model ($120-$160 on studio kilns) — see the Kilns sheet")
m("OESGENESISTSC", lambda: (200, "Accessories: Electro Sitter Genesis $1,450 less KilnStar $1,250"), LIKELY,
  "derived from the two Electro Sitter prices")

NO_MATCH = {
    "OLBFEC": "no matching item in the 2026 pricelist",
    "OLIRTS1823": "ignition ring & thermocouple — not priced in the 2026 list",
    "OLIRTS28": "ignition ring & thermocouple — not priced in the 2026 list",
    "OLTBBR18": "Torchbearer blank ring — the 2026 list only prices electric-kiln blank rings",
    "OLTBBR23": "Torchbearer blank ring — the 2026 list only prices electric-kiln blank rings",
    "OLTBBR28": "Torchbearer blank ring — the 2026 list only prices electric-kiln blank rings",
    "OL2323": "no 2323E in the 2026 list (the 23\" block runs 2318E, 2318HE, 2323HE, 2327E, 2327HE, 2331HE)",
    "OLKSC": "KilnStar is the base controller in the 2026 list, so it carries no separate upgrade price",
    "OLSC12K": "KilnStar is the base controller in the 2026 list, so it carries no separate upgrade price",
    "OES12KC": "Electro Sitter KilnStar is the base version; no separate upgrade price in the list",
    "OLVG3DC": "the 2026 list prices the HB86 Vitrigraph by controller, not as a controller upgrade",
    "SPIFL8": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL12": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL17": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL20": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL24": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL27": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL31": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
    "SPIFL53": "Sheffield kiln package (kiln + vent + shelf kit) — not a single pricelist item",
}

# ---------------- apply ----------------
with open(SRC_CSV, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))
header, body = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
assert "new compare" not in header
i_sku = header.index("SKU")
i_cmp = header.index("Compare-at Price")
i_txt = header.index("Title") if "Title" in header else header.index("Description")

def title(d):
    t = html.unescape(re.sub(r"<[^>]+>", " ", d))
    t = re.sub(r"\s+", " ", t).strip()
    return t.replace("You are browsing ceramic kilns, glass fusing kiln, raku kilns and test Kilns. This is a", "").strip()

out_rows, audit, unmapped = [], [], []
for r in body:
    sku = r[i_sku].replace('="', "").replace('"', "")
    new, basis, conf, note = "", "", "", ""
    if sku in M:
        spec, conf, note = M[sku]
        price, basis = spec()
        new = f"{price:.2f}"
    elif sku in NO_MATCH:
        conf, note, basis = "no match", NO_MATCH[sku], ""
    else:
        unmapped.append(sku)
        conf, note = "no match", "not mapped"
    out_rows.append(r + [new])
    old = r[i_cmp]
    audit.append([sku, title(r[i_txt])[:70], r[header.index("Price")],
                  float(old) if old not in ("", "0.00") else None,
                  float(new) if new else None, basis, conf, note])

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header + ["new compare"])
    w.writerows(out_rows)

# ---------------- audit workbook ----------------
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
awb = openpyxl.Workbook(); sh = awb.active; sh.title = "New Compare Audit"
sh.sheet_view.showGridLines = False
HDRS = ["SKU", "Listing", "Current Price", "Old Compare-at", "new compare",
        "Matched to (2026 pricelist)", "Match", "Note / what to check", "Change"]
W = [16, 52, 13, 14, 13, 46, 9, 66, 11]
for i, (h, w) in enumerate(zip(HDRS, W), 1):
    c = sh.cell(row=1, column=i, value=h)
    c.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="1F3864")
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    sh.column_dimensions[get_column_letter(i)].width = w
sh.row_dimensions[1].height = 28
FLAG = PatternFill("solid", fgColor="FCE4D6")
BORDER = Border(bottom=Side(style="thin", color="BFBFBF"))
for n, a in enumerate(audit, 2):
    sh.cell(row=n, column=9, value=(f"=IF(OR(E{n}=\"\",D{n}=\"\"),\"\",E{n}/D{n}-1)"))
    for i, v in enumerate(a, 1):
        c = sh.cell(row=n, column=i, value=v)
        c.font = Font(name="Arial", size=10)
        c.border = BORDER
        c.alignment = Alignment(vertical="center", wrap_text=(i in (2, 6, 8)))
        if i in (3, 4, 5): c.number_format = '$#,##0.##'
    sh.cell(row=n, column=9).number_format = '0.0%;-0.0%;"—"'
    sh.cell(row=n, column=9).font = Font(name="Arial", size=10)
    sh.cell(row=n, column=9).border = BORDER
    if a[6] in ("review", "no match"):
        for i in range(1, 10): sh.cell(row=n, column=i).fill = FLAG
sh.freeze_panes = "A2"
sh.auto_filter.ref = f"A1:I{len(audit)+1}"
sh.page_setup.orientation = "landscape"
sh.page_setup.fitToWidth, sh.page_setup.fitToHeight = 1, 0
sh.sheet_properties.pageSetUpPr.fitToPage = True
sh.print_title_rows = "1:1"
awb.save(OUT_AUDIT)

print("rows:", len(out_rows), "| priced:", sum(1 for a in audit if a[4] is not None),
      "| no match:", sum(1 for a in audit if a[4] is None), "| unmapped SKUs:", unmapped)
import collections
print(collections.Counter(a[6] for a in audit))

print()
print("=== new compare BELOW the old compare-at, or up more than 22% ===")
for a in audit:
    if a[3] and a[4]:
        ch = a[4] / a[3] - 1
        if ch < 0 or ch > 0.22:
            print(f"  {a[0]:16} {a[1][:40]:42} old {a[3]:>9,.0f} -> new {a[4]:>9,.0f}  {ch:+6.1%}   {a[5][:40]}")
