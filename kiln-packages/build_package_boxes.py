#!/usr/bin/env python3
"""
Build the "What's in the package" box for each Sheffield Pottery kiln package
and insert it into the product description.

Reads   kiln-packages/originals/<product id>.html  (descriptions as they were
        before this change, pulled from Shopify on 2026-11-19)
Writes  kiln-packages/updated/<product id>.html    (description with the box)
        kiln-packages/preview.html                 (all boxes on one page)

Running it again is safe: if a description already contains a box
(class="sppk"), the old box is replaced rather than duplicated.

Where the contents come from (in this order of preference):
  1. What the package's own description already says about its kit/vent,
     so the box never contradicts the text under it.
  2. The store's own matching furniture-kit / vent product
     (e.g. "Skutt Furniture Kit For KM818-3 / 822-3 Kiln",
     "Skutt EnviroVent 2: Kiln Vent", "L&L Vent-Sure Kiln Vent System",
     "Orton VentMaster Downdraft Kiln Venting System").
  3. The manufacturer's site (only used for the L&L eQuad-Pro kits,
     from hotkilns.com).
Anything not confirmed by one of those is described generically and listed
in UNCONFIRMED below so a person can fill it in.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- styles ---
# Inline styles only (no <style> block): Shopify's Google Shopping feed strips
# tags from descriptions, and CSS text in a <style> block would leak into it.
NAVY, RED, LINE, MUTED = "#1f2a6b", "#c8452d", "#e4ddd0", "#5b5b5b"
ST = {
    "box": (f"display:flow-root;clear:both;background:#fff;border:2px solid {NAVY};"
            "border-radius:14px;overflow:hidden;margin:0 0 22px;max-width:760px;"
            "color:#222;line-height:1.5;box-sizing:border-box;"),
    "h": (f"margin:0;padding:12px 18px;background:{NAVY};color:#fff;"
          "font-size:18px;line-height:1.3;"),
    "rows": "list-style:none;margin:0;padding:0;",
    "row": f"list-style:none;margin:0;padding:12px 18px;border-top:1px solid {LINE};",
    "row1": "list-style:none;margin:0;padding:12px 18px;",
    "top": ("display:flex;flex-wrap:wrap;justify-content:space-between;"
            "align-items:center;gap:6px 12px;"),
    "name": f"color:{NAVY};font-size:16px;",
    "badge": ("display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;"
              "font-weight:700;letter-spacing:.05em;text-transform:uppercase;"
              f"white-space:nowrap;background:{NAVY};color:#fff;"),
    "badge_opt": ("display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;"
                  "font-weight:700;letter-spacing:.05em;text-transform:uppercase;"
                  f"white-space:nowrap;background:#fff;color:{RED};border:1px solid {RED};"),
    "sub": "margin:6px 0 0 20px;padding:0;font-size:15px;",
    "li": "margin:2px 0;padding:0;",
    "need": f"margin:6px 0 0;font-size:14px;color:{MUTED};",
    "foot": (f"margin:0;padding:10px 18px;background:#f4f1ea;font-size:14px;color:{MUTED};"
             f"border-top:1px solid {LINE};"),
    "a": f"color:{NAVY};font-weight:700;",
}

# -------------------------------------------------------- shared pieces ---
IN = "Included"
OPT = "Optional, not included"

SKUTT_SMALL_POSTS = 'Small post assortment: 3 each of 1", 2", 3", 4", 5" and 6" posts'
SKUTT_LARGE_POSTS = 'Large post assortment: 6 each of 1", 2", 3", 4", 5" and 6" posts'
LL_POSTS = ('Six each of 1/2", 1", 2", 4", 6" and 8" high posts '
            '(1-1/2" square)')
LL_GLOVES = "One pair of heat-resistant gloves"

ENVIROVENT2 = dict(
    name="Skutt EnviroVent 2 downdraft vent",
    badge=IN,
    items=[
        "Wall-mounted 140 CFM fan motor (plugs into a standard 120V outlet)",
        "Spring-loaded plenum cup that seals against the underside of the kiln",
        '8 ft of 3" heavy-duty flexible aluminum duct (cup to fan)',
        '3" exhaust tube on the fan, made to pass through most walls',
        "Floor-mount bracket",
    ],
    need="Pulls fumes out through small holes in the kiln floor and lid and "
         "sends them outdoors, while improving heat uniformity and element life.",
)


def ventmaster(volts=None):
    name = "Orton VentMaster downdraft vent"
    if volts:
        name += f" ({volts})"
    return dict(
        name=name,
        badge=IN,
        items=[
            "Fan (blower) assembly with 6 ft power cord, sits on the floor or mounts on the wall (73 CFM)",
            "Collector cup with adjustable-height foot and high-temperature gasket",
            '4 ft of 2" high-temperature hose and two 2" hose clamps',
            '1/4" drill bit and 3" stud for installation',
            "Orton sample test cones, plus Cones &amp; Firing and Kiln Safety booklets",
        ],
        need='Not included: to send fumes outdoors you will also need a dryer vent kit '
             '(4" aluminum duct and a wall vent) from any hardware store.',
    )


VENTSURE = dict(
    name="L&amp;L Vent-Sure downdraft vent",
    badge=IN,
    items=[
        "Wall-mounted blower on a bracket, with vent pipe to pass through the outside wall and motor inlet duct",
        "8 ft power cord with in-line on/off switch (plugs into a standard 120V outlet)",
        "Bypass Collection Box, with hardware to mount it on the kiln stand",
        "Flexible aluminum duct (expands to 8 ft) and two hose clamps",
        '4" 90&deg; elbow for the outside end of the vent pipe',
    ],
    need="The blower is mounted away from the kiln, so there is no vibration or heat on the motor, "
         "and the duct runs under negative pressure so a leak pulls air in rather than pushing fumes out.",
)

CONEART_VENT = dict(
    name="Orton downdraft vent, factory installed",
    badge=IN,
    items=[
        "Installed on the kiln at the Cone Art factory",
        "Integrated with the Genesis controller, so the vent can switch on and off automatically as part of your firing",
    ],
    need=None,
)

OLYMPIC_FL_VENT = dict(
    name="Orton kiln-mount downdraft vent",
    badge=IN,
    items=["Installed on the kiln at the Olympic factory"],
    need=None,
)

FREEDOM_KIT = dict(
    name="Olympic Freedom Kit (spare-parts kit)",
    badge=IN,
    items=[
        "Wiring schematic for your kiln",
        "Extra thermocouple",
        "2 elements with element pins, high-temperature connectors and installation instructions",
        "Crimping tool for crimping connectors to elements",
        "Pint of mortar",
    ],
    need=None,
)


def kiln(name, items):
    return dict(name=name, badge=IN, items=items, need=None)


def kit(name, items, badge=IN, need=None):
    return dict(name=name, badge=badge, items=items, need=need)


# ------------------------------------------------------- Skutt helpers ---
SK = {
    "818-3": ['2 full shelves, 15" &times; 15" &times; 5/8"', '3 half shelves, 5/8" thick', SKUTT_SMALL_POSTS],
    "818": ['2 full shelves, 15" &times; 16" &times; 5/8"', '3 half shelves, 8" &times; 15" &times; 5/8"', SKUTT_SMALL_POSTS],
    "1018-3": ['6 half shelves, 9-7/8" &times; 20" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1018": ['6 half shelves, 10-5/8" &times; 22" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1027-3": ['8 half shelves, 9-7/8" &times; 20" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1027": ['8 half shelves, 10-5/8" &times; 22" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1222-3": ['6 half shelves, 13" &times; 26" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1227-3 5/8": ['8 half shelves, 13" &times; 26" &times; 5/8"', SKUTT_LARGE_POSTS],
    "1227-3 1": ['8 half shelves, 13" &times; 26" &times; 1"', SKUTT_LARGE_POSTS],
    # Not confirmed in the store or on skutt.com -- see UNCONFIRMED.
    "1231-3PK 1": ['1"-thick half shelves, rated for cone 10', "Post assortment"],
}


def skutt(model, kitkey, touch, sides, kit_label=None):
    ctrl = ("KilnMaster touchscreen controller with Wi-Fi" if touch
            else "KilnMaster controller")
    std = "Stand and peephole plugs" + (", plus Skutt lid lifter" if sides >= 10 else "")
    return [
        kiln(f"Skutt {model} kiln", [ctrl, std]),
        kit(kit_label or f"Skutt furniture kit for the {model}", SK[kitkey]),
        ENVIROVENT2,
    ]


# --------------------------------------------------------- L&L helpers ---
def ll(model, shelves):
    return [
        kiln(f"L&amp;L {model} Easy-Fire kiln",
             ["Genesis touchscreen controller with Wi-Fi (upgrade)", "Stand and peephole plugs"]),
        kit("L&amp;L furniture kit", shelves + [LL_POSTS, LL_GLOVES]),
        VENTSURE,
    ]


def llq(model, shelves):
    return [
        kiln(f"L&amp;L {model} eQuad-Pro kiln",
             ["Genesis touchscreen controller with Wi-Fi", "3-zone control and quad elements",
              "Stand and peephole plugs"]),
        kit("L&amp;L furniture kit", shelves + [LL_POSTS, LL_GLOVES]),
        VENTSURE,
    ]


# ----------------------------------------------------- Olympic helpers ---
def freedom(model, layers):
    return [
        kiln(f"Olympic Freedom {model} kiln",
             ["Bartlett electronic controller", "Stand, peephole plugs and instruction manual"]),
        kit("Freedom furniture kit", layers + ["1 lb bag of kiln wash", "33 assorted stilts for glazing"]),
        ventmaster(),
        FREEDOM_KIT,
    ]


def fl(model, shelves, posts):
    return [
        kiln(f"Olympic {model} front-loading kiln",
             ["Dual-zone electronic controller", "Door and floor elements"]),
        kit("Furniture kit (four layers)", [shelves, posts, "Bag of kiln wash"]),
        OLYMPIC_FL_VENT,
    ]


# ---------------------------------------------------- Cone Art helpers ---
def coneart(model, kit_items):
    return [
        kiln(f"Cone Art {model} kiln", ["Bartlett Genesis touchscreen controller with Wi-Fi"]),
        kit("High-alumina furniture kit (cone 11 rated)", kit_items),
        CONEART_VENT,
    ]


CA_2327 = ['Three 21" diameter full shelves', 'Two 21" diameter half shelves',
           'Three each 1-3/4" square posts in 1", 2", 6" and 8" heights',
           'Six 1-3/4" square &times; 4" posts', "2 kg kiln wash"]
CA_SQ = ['3 square shelves, 21" &times; 21" &times; 3/4"', '2 shelves, 21" &times; 10-1/2" &times; 3/4"',
         'Three each 1", 2", 6" and 8" posts', 'Six 4" posts', "2 kg kiln wash"]

# ----------------------------------------------------- Paragon helpers ---
DRAGON_KIT = ['1 C-30 full shelf, 22" &times; 22" &times; 1"', '4 C-30H half shelves, 22" &times; 11" &times; 1"',
              '1-1/2" wide square posts, 8 each in 4", 6" and 8" lengths', "1 lb bag of kiln wash"]
BULL_ELK_KIT = ['2 C-30 full shelves, 22" &times; 22" &times; 1"', '8 C-30H half shelves, 22" &times; 11" &times; 1"',
                '1-1/2" wide square posts, 16 each in 4", 6" and 8" lengths', "2 lb bag of kiln wash"]


def optional_kit(contents):
    return kit("Furniture kit", contents, badge=OPT,
               need="Not part of this package. Call us to add the matching kit listed above.")


# =================================================== the packages ======
# Keyed by Shopify product id (numeric part).
SPEC = {
    # ---- Skutt (EnviroVent 2) ----
    "8316161327426": skutt("KMT1022-3", "1018-3", True, 10),
    "8316169322818": skutt("KMT1027-3", "1027-3", True, 10),
    "8316170174786": skutt("KMT822-3", "818-3", True, 8),
    "9372720398658": skutt("KM1027", "1027", False, 10),
    "9372747497794": skutt("KM1222-3", "1222-3", False, 12, 'Skutt 5/8" furniture kit for the KM1222-3'),
    "9372750086466": skutt("KM818-3", "818-3", False, 8),
    "9372760637762": skutt("KMT1227-3", "1227-3 5/8", True, 12, 'Skutt 5/8" furniture kit for the KM1227-3'),
    "9372766208322": skutt("KMT1227-3PK", "1227-3 1", True, 12, 'Skutt 1" furniture kit for the KM1227-3'),
    "9372769485122": skutt("KMT1231-3PK", "1231-3PK 1", True, 12, 'Skutt 1" furniture kit for the KM1231-3PK'),
    "9715480625474": skutt("KM818-30A-3", "818-3", False, 8),
    "14795305156979": skutt("KMT818-3", "818-3", True, 8),
    "14795305681267": skutt("KM818", "818", False, 8),
    "14795308204403": skutt("KM822", "818", False, 8),
    "14795313119603": skutt("KMT822", "818", True, 8),
    "14795313414515": skutt("KM822-3", "818-3", False, 8),
    "14795313578355": skutt("KM1027-3", "1027-3", False, 10),
    "14795313709427": skutt("KMT1222-3", "1222-3", True, 12, 'Skutt 5/8" furniture kit for the KM1222-3'),
    "15141954290035": skutt("KMT818", "818", True, 8),
    "8316161065282": skutt("KM1022-3", "1018-3", False, 10),
    "15141949636979": skutt("KMT818-30A-3", "818-3", True, 8),
    "15141956354419": skutt("KM1018", "1018", False, 10),
    "15141956878707": skutt("KM1018-3", "1018-3", False, 10),
    "15141959663987": skutt("KMT1027", "1027", True, 10),
    "15141967823219": skutt("KM1231-3PK", "1231-3PK 1", False, 12, 'Skutt 1" furniture kit for the KM1231-3PK'),
    "15418821083507": skutt("KMT1018-3", "1018-3", True, 10),

    # ---- L&L (Vent-Sure) ----
    "8315913634114": ll("e18M-3", ["1 full shelf and 4 half shelves (cone 11 rated)"]),
    "8315913765186": ll("e18S-3", ['One 15-1/2" full round shelf and four 15-1/2" half round shelves (5/8" thick)']),
    "8315913994562": ll("e18T-3", ['Two 15" full round shelves and four 15" half round shelves (5/8" thick)']),
    "8315914289474": ll("e23M-3", ['Six 20" half round shelves (3/4" thick)']),
    "8315914649922": ll("e23S-3", ['Six 20" half round shelves (3/4" thick)']),
    "8315915108674": ll("e23T-3", ['Eight 20" half round shelves (3/4" thick)']),
    "8315915469122": ll("e28M-3", ['Six 25-1/2" half round shelves (3/4" thick)']),
    "8315915796802": ll("e28S-3", ['Six 25-1/2" half round shelves (3/4" thick)']),
    "8315916157250": ll("e28T-3", ['Eight 25-1/2" half round shelves (3/4" thick)']),
    "8315917041986": llq("eQ2827-3", ['Eight 25-1/2" half round hollow-core shelves (5/8" thick)']),
    "15142970130803": llq("eQ2327-3", ['Eight 20" half round hollow-core shelves (5/8" thick)']),

    # ---- Olympic Freedom (Orton VentMaster + Freedom Kit) ----
    "8316052308290": freedom("1414HE", ["2 layers of shelving: 1 full shelf and 2 half shelves",
                                        '3 each of 1", 2", 3", 4", 5" and 6" posts']),
    "8316052373826": freedom("1823HE", ['3 layers of shelving: 1 full shelf (1/2" thick) and 4 half shelves (1" thick)',
                                        '6 each of 4", 6", 8" and 10" posts']),
    "8316052439362": freedom("2323HE", ['3 layers of shelving: 1 full shelf (1/2" thick) and 4 half shelves (1" thick)',
                                        '6 each of 4", 6", 8" and 10" posts']),
    "8316052537666": freedom("2327HE", ['3 layers of shelving: 1 full shelf (1/2" thick) and 4 half shelves (1" thick)',
                                        '6 each of 4", 6", 8" and 10" posts']),
    "8316052570434": freedom("2527HE", ['3 layers of 1"-thick shelving: 2 half shelves and 1 rectangle shelf per layer',
                                        '10 each of 6", 8" and 10" posts']),
    "8316052701506": freedom("2823HE", ['4 layers of 1"-thick shelving: 8 half shelves',
                                        '6 each of 4", 6", 8" and 10" posts']),
    "8316052734274": freedom("2827HE", ['4 layers of 1"-thick shelving: 8 half shelves',
                                        '6 each of 4", 6", 8" and 10" posts']),

    # ---- Olympic front loaders (factory-mounted Orton vent) ----
    "8316335030594": fl("FL8", '8 shelves, 11" &times; 22" &times; 1"', '8 each of 4", 6", 8" and 10" posts'),
    "8316333556034": fl("FL12", '8 shelves, 11" &times; 22" &times; 1"', '8 each of 4", 6", 8" and 10" posts'),
    "8316333785410": fl("FL17", '8 shelves, 13" &times; 26" &times; 1"', '8 each of 4", 6", 8" and 10" posts'),
    "8316333982018": fl("FL20", '8 rectangle shelves, 13" &times; 26" &times; 1" (2 per layer)',
                        '8 each of 4", 6", 8" and 10" large square posts'),
    "8316334211394": fl("FL24", '16 shelves, 16" &times; 16" &times; 1"', '16 each of 4", 6", 8" and 10" posts'),
    "8316334342466": fl("FL27", '16 shelves, 17" &times; 17" &times; 1"', '16 each of 4", 6", 8" and 10" posts'),
    "8316334571842": fl("FL31", '16 shelves, 17" &times; 17" &times; 1"', '16 each of 4", 6", 8" and 10" posts'),
    "8316334866754": fl("FL53", '32 shelves, 11" &times; 22" &times; 1"', '32 each of 4", 6", 8" and 10" posts'),

    # ---- Cone Art (factory-installed, controller-integrated Orton vent) ----
    "8316361081154": coneart("GX2322D-SQ square", CA_SQ),
    "15380548911475": coneart("GX2327D-SQ square", CA_SQ),
    "8316361441602": coneart("GX2327D round", CA_2327),
    "8316361900354": coneart("GX2827D round", ['Eight 26" diameter half shelves',
                                               'Six each 1-3/4" square posts in 1", 2", 4", 6" and 8" heights',
                                               "2 kg kiln wash"]),
    "8316362096962": coneart("GX4227D oval", ['3 kiln shelves, 26" &times; 13"', '6 half round shelves, 26"',
                                              '9 each of 1", 2", 4", 6" and 8" posts', "2 kg kiln wash"]),

    # ---- Paragon (Orton VentMaster) ----
    "8304899490114": [
        kiln("Paragon TnF-23-3 kiln", ["Touchscreen controller", "Heavy-duty rolling kiln stand"]),
        kit("Paragon furniture kit for the TnF-23-3",
            ['6 C-23H half shelves, 20" round &times; 3/4" thick',
             '1" wide square posts, 8 each in 1", 2", 3", 4", 5" and 6" lengths']),
        ventmaster(),
    ],
    "8304899588418": [
        kiln("Paragon TnF-24-3 kiln", ["Sentinel Touch controller", "Deluxe rolling kiln stand"]),
        kit("Paragon FSA24B3 furniture kit",
            ['8 C-23H half shelves, 20" round &times; 3/4" thick',
             '1" wide square posts, 8 each in 1", 2", 3", 4", 5" and 6" lengths', "1 lb bag of kiln wash"]),
        ventmaster(),
    ],
    "8304899817794": [
        kiln("Paragon TnF-82 kiln", ["Touchscreen controller",
                                     "Deluxe rolling kiln stand with locking casters, vent bracket and greenware drying rack"]),
        kit("Paragon FSA82B furniture kit",
            ['3 C-16 shelves, 15-1/2" octagon &times; 5/8"', '1 C-16H half shelf, 15-1/2" octagon &times; 5/8"',
             '1" wide square posts, 4 each in 1/2", 1", 2", 3", 4", 5" and 6" lengths', "1 lb bag of kiln wash"]),
        ventmaster(),
    ],
    "8304899883330": [
        kiln("Paragon TnF-82-3 kiln", ["Sentinel Touch controller",
                                       "Deluxe rolling kiln stand with locking casters, vent bracket and greenware drying rack"]),
        kit("Paragon FSA82B3 furniture kit",
            ['3 C-18 shelves, 15" round &times; 5/8"', '1 C-18H half shelf, 15" round &times; 5/8"',
             '1" wide square posts, 4 each in 1/2", 1", 2", 3", 4", 5" and 6" lengths', "1 lb bag of kiln wash"]),
        ventmaster(),
    ],
    "8304898015554": [
        kiln("Paragon Super Dragon front-loading kiln", ["Touchscreen controller", "Auxiliary output for the vent"]),
        ventmaster(),
        optional_kit(DRAGON_KIT),
    ],
    "8316066234690": [
        kiln("Paragon Dragon front-loading kiln", ["Digital controller", '24" stand (no casters)',
                                                   "Door switch and auxiliary output plug"]),
        ventmaster("240V"),
        optional_kit(DRAGON_KIT),
    ],
    "8316071543106": [
        kiln("Sheffield Pottery Bull Elk Pro front-loading kiln (by Paragon)",
             ["Touchscreen controller", "3-zone control with S-type thermocouples", "Door elements",
              "Door gasket and door safety shut-off", "AOP outlet for vent integration",
              '19" stand with casters']),
        ventmaster("240V"),
        optional_kit(BULL_ELK_KIT),
    ],
    "8316071674178": [
        kiln("Sheffield Pottery Bull Elk Studio front-loading kiln (by Paragon)",
             ["Touchscreen controller", "3-zone control with type K thermocouples",
              "Door gasket and door safety shut-off", '19" stand with casters']),
        ventmaster("120V"),
        optional_kit(BULL_ELK_KIT),
    ],
}

# Packages whose box has something a person should still confirm.
UNCONFIRMED = {
    "9372769485122": "Exact shelf count/size of the Skutt 1\" kit for the KM1231-3PK (not in the store or on skutt.com).",
    "15141967823219": "Exact shelf count/size of the Skutt 1\" kit for the KM1231-3PK (not in the store or on skutt.com).",
}

# Deliberately left alone, with the reason.
SKIPPED = {
    "8312988041538": "Skutt KMT1231-3PK Kiln with Touchscreen Controller: a bare kiln, not a package (no kit or vent).",
    "8316066431298": "Paragon Iguana package: includes neither a vent nor a furniture kit; its optional kit is already listed.",
    "15663311356275": "Skutt GM814 glass package: already lists its furniture kit contents; glass packages have no vent.",
    "15677737566579": "Skutt GM818 glass package: already lists its furniture kit contents; glass packages have no vent.",
    "15677744054643": "Skutt GM1014 glass package: already lists its furniture kit contents; glass packages have no vent.",
    "15682529493363": "Evenheat RM II 2322 (draft): Evenheat XL1 kit contents not found in the store or on evenheat-kiln.com.",
    "15141964415347": "Skutt KM1227-3 (draft): unclear whether it ships with the 5/8\" or 1\" kit, and text mentions a touchscreen the title doesn't.",
    "8316360917314": "Cone Art GX2322D round: kit contents not found in the store.",
}

FOOT = ('Questions about what\'s in the box? Call our kiln experts at '
        '<a href="tel:+18887742529">(888) 774-2529</a>.')


# ------------------------------------------------------------ rendering ---
def render_row(r, first):
    badge = ST["badge"] if r["badge"] == IN else ST["badge_opt"]
    out = [f'<li style="{ST["row1"] if first else ST["row"]}">'
           f'<div style="{ST["top"]}"><b style="{ST["name"]}">{r["name"]}</b>'
           f'<span style="{badge}">{r["badge"]}</span></div>']
    if r["items"]:
        out.append(f'<ul style="{ST["sub"]}">'
                   + "".join(f'<li style="{ST["li"]}">{i}</li>' for i in r["items"]) + "</ul>")
    if r.get("need"):
        out.append(f'<p style="{ST["need"]}">{r["need"]}</p>')
    out.append("</li>")
    return "".join(out)


def render_box(rows):
    foot = FOOT.replace("<a ", f'<a style="{ST["a"]}" ')
    return (f'<div class="sppk" id="whats-in-the-package" style="{ST["box"]}">'
            f'<h3 style="{ST["h"]}">What\'s in the package</h3>'
            f'<ul style="{ST["rows"]}">'
            + "".join(render_row(r, i == 0) for i, r in enumerate(rows)) + "</ul>"
            f'<p class="sppk-foot" style="{ST["foot"]}">{foot}</p></div>')


EXISTING_BOX = re.compile(r'<div class="sppk".*?<p class="sppk-foot".*?</p></div>', re.S)


def insert_box(desc, box):
    """Put the box after any leading <style> blocks and leading headings;
    otherwise at the very top. Replace an earlier box if there is one."""
    if EXISTING_BOX.search(desc):
        return EXISTING_BOX.sub(lambda _m: box, desc, count=1)
    pos = 0
    lead = re.compile(r"\s*(<style\b.*?</style>)", re.S | re.I)
    while (m := lead.match(desc, pos)):
        pos = m.end()
    head = re.compile(r"\s*<h[1-3]\b[^>]*>.*?</h[1-3]>", re.S | re.I)
    while (m := head.match(desc, pos)):
        pos = m.end()
    return desc[:pos] + box + desc[pos:]


def main():
    idx = {d["id"].split("/")[-1]: d for d in
           json.load(open(os.path.join(HERE, "originals", "index.json")))}
    os.makedirs(os.path.join(HERE, "updated"), exist_ok=True)
    preview = ["<!doctype html><meta charset='utf-8'><title>Kiln package boxes</title>"
               "<body style='font-family:system-ui,sans-serif;max-width:820px;margin:20px auto;padding:0 16px'>"]
    for pid, rows in SPEC.items():
        meta = idx[pid]
        src = open(os.path.join(HERE, "originals", f"{pid}.html")).read()
        box = render_box(rows)
        new = insert_box(src, box)
        assert new.count('class="sppk"') == 1, pid
        open(os.path.join(HERE, "updated", f"{pid}.html"), "w").write(new)
        flag = f" <em style='color:#c8452d'>[confirm: {UNCONFIRMED[pid]}]</em>" if pid in UNCONFIRMED else ""
        preview.append(f"<h2 style='font-size:16px;margin:28px 0 8px'>{html.escape(meta['title'])} "
                       f"<small>({meta['status']})</small>{flag}</h2>{box}")
    missing = set(idx) - set(SPEC) - set(SKIPPED)
    assert not missing, missing
    open(os.path.join(HERE, "preview.html"), "w").write("".join(preview))
    print(f"{len(SPEC)} descriptions written, {len(SKIPPED)} skipped, {len(UNCONFIRMED)} to confirm")


if __name__ == "__main__":
    main()
