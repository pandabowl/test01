"""
Curated SEO + agentic-commerce content for Sheffield Pottery's Cone Art kilns.

Everything in this file is derived from data already published on the store
(the custom.specifications spec table, the product description, the product
title, variant options). Nothing here is a new spec claim. Where the store's
own sources disagree (description vs. spec table), the disputed value is left
out of the new copy and listed in DISPUTED_FACTS so a human can resolve it
against Cone Art's spec sheet. See cone_art/AUDIT.md.

The spec tables were cross-checked with physics (amps = kW / volts) and are
internally consistent for every model except the 4213G (fixed below), so the
spec table is treated as the source of truth for dimensions, capacity and amp
draw. Breaker sizes are only quoted where the description and spec table
agree; otherwise customers are pointed at the Specifications tab and a
licensed electrician.

Consumed by scripts/cone_art_seo.py (`plan` command).
"""
import html

# --------------------------------------------------------------------------
# Shopify standard product taxonomy
# --------------------------------------------------------------------------
CATEGORY_CERAMIC_KILNS = "gid://shopify/TaxonomyCategory/ae-2-1-4-20-1"
CATEGORY_GLASS_KILNS = "gid://shopify/TaxonomyCategory/ae-2-1-4-20-3"
CATEGORY_THERMOCOUPLES = "gid://shopify/TaxonomyCategory/ha-15-36-34-2"

# Category metafield (standard attribute) values, keyed by standard
# metaobject type. taxonomy_value ids come from the Kilns category in
# Shopify's standard product taxonomy.
ATTRIBUTE_VALUES = {
    "shopify--kiln-features": {
        "digital-controller": ("Digital controller", "gid://shopify/TaxonomyValue/28628"),
        "energy-efficient": ("Energy efficient", "gid://shopify/TaxonomyValue/28629"),
        "exhaust-vent-system": ("Exhaust vent system", "gid://shopify/TaxonomyValue/28630"),
        "programmable-firing-cycles": ("Programmable firing cycles", "gid://shopify/TaxonomyValue/28634"),
        "sectional-construction": ("Sectional construction", "gid://shopify/TaxonomyValue/28637"),
        "touchscreen": ("Touchscreen", "gid://shopify/TaxonomyValue/28639"),
    },
    "shopify--kiln-loading-style": {
        "top-loading": ("Top loading", "gid://shopify/TaxonomyValue/28646"),
    },
    "shopify--kiln-firing-atmosphere": {
        "oxidation": ("Oxidation", "gid://shopify/TaxonomyValue/69947"),
    },
    "shopify--kiln-heating-element-type": {
        "kanthal-fecral-wire": ("Kanthal (FeCrAl) wire", "gid://shopify/TaxonomyValue/69951"),
    },
    "shopify--power-source": {
        "ac-powered": ("AC-powered", "gid://shopify/TaxonomyValue/7773"),
    },
    "shopify--shape": {
        "round": ("Round", "gid://shopify/TaxonomyValue/627"),
        "square": ("Square", "gid://shopify/TaxonomyValue/628"),
        "oval": ("Oval", "gid://shopify/TaxonomyValue/7321"),
    },
}

# metaobject type -> product metafield key in the reserved `shopify` namespace
ATTRIBUTE_METAFIELD_KEYS = {
    "shopify--kiln-features": "kiln-features",
    "shopify--kiln-loading-style": "kiln-loading-style",
    "shopify--kiln-firing-atmosphere": "kiln-firing-atmosphere",
    "shopify--kiln-heating-element-type": "kiln-heating-element-type",
    "shopify--power-source": "power-source",
    "shopify--shape": "shape",
}

# --------------------------------------------------------------------------
# Per-product facts and copy (40 storefront-visible Cone Art products)
#
# family:  glass | pottery | package | part
# ctrl:    bartlett3 (glass base) | bartlett12 | genesis
# interior: text exactly as it should read in an answer
# cuft:    None when the store's sources disagree (see DISPUTED_FACTS)
# amps:    single-phase (240 V, 208 V) or 120 V draw from the spec table
# amps3:   three-phase (240 V, 208 V) when the spec table lists it
# breaker: only when description and spec table agree
# zones:   only when the product's own description states it
# --------------------------------------------------------------------------
PRODUCTS = {
    # ---------------------------------------------------------------- glass
    "8316355019074": dict(
        model="115G-SQ", family="glass", shape="square", ctrl="bartlett3",
        interior='15.5" x 15.5" x 6.5" deep', cuft="0.9", sections=1,
        volts="120", amps="18", breaker="20 A", elements="an element in the lid",
        seo_title='Cone Art 115G-SQ Square Glass Kiln | 15.5" x 15.5", 120V',
        seo_desc='Cone Art 115G-SQ square glass fusing kiln: 15.5" x 15.5" x 6.5" interior, '
                 'lid element, 120 V. A starter kiln for fusing, slumping and annealing.',
    ),
    "8316355215682": dict(
        model="117G", family="glass", shape="round", ctrl="bartlett3",
        interior='14.5" across x 6" deep', cuft="1", sections=1,
        volts="120", amps="14.5", breaker="15 A",
        plug_note="It can be plugged into a normal wall outlet.",
        elements="Kanthal A-1 elements in the lid",
        seo_title='Cone Art 117G Glass Fusing Kiln | 120V, 14.5" x 6" Deep',
        seo_desc='Cone Art 117G glass fusing kiln: 14.5" x 6" interior with Kanthal A-1 lid '
                 'elements. Plugs into a normal 120 V wall outlet. A home-studio fusing kiln.',
    ),
    "8316355379522": dict(
        model="1809G", family="glass", shape="round", ctrl="bartlett3",
        interior='17.5" across x 9" deep', cuft="1.3", sections=1,
        volts="208/240", amps=("28", "32"), breaker="40 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 1809G Glass Fusing Kiln | 17.5" x 9" Deep',
        seo_desc='Cone Art 1809G glass fusing kiln: 17.5" x 9" interior (1.3 cu ft), elements '
                 'in lid and walls, 208/240 V. Bartlett 3-key control, 12-key upgrade available.',
    ),
    "8316355445058": dict(
        model="1813G", family="glass", shape="round", ctrl="bartlett3",
        interior='17.5" across x 13.5" deep', cuft="2", sections=2,
        volts="208/240", amps=("28", "32"), breaker="40 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 1813G Glass Fusing Kiln | 17.5" x 13.5" Deep',
        seo_desc='Cone Art 1813G glass fusing kiln: 17.5" x 13.5" deep (2 cu ft) for projects '
                 'that need extra depth. Lid and wall elements, 208/240 V, CSA approved.',
    ),
    "8316355608898": dict(
        model="2309G", family="glass", shape="round", ctrl="bartlett3", large_glass=True,
        interior='23.5" across x 9" deep', cuft="2.3", sections=1,
        volts="208/240", amps=("30", "35"), breaker="40 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 2309G Glass Fusing Kiln | 23.5" x 9" Deep',
        seo_desc='Cone Art 2309G glass fusing kiln: 23.5" x 9" interior (2.3 cu ft), elements '
                 'in lid and walls, 208/240 V. A size many glass artists choose for platters.',
    ),
    "8316355707202": dict(
        model="2309G-SQ", family="glass", shape="square", ctrl="bartlett3",
        interior='23" x 23" x 9" deep', cuft="2.8", sections=1,
        volts="208/240", amps=("30", "35"), breaker="40 A",
        elements="elements in the lid and the walls", max_temp="1700°F",
        seo_title='Cone Art 2309G-SQ Square Glass Kiln | 23" x 23" x 9"',
        seo_desc='Cone Art 2309G-SQ square glass kiln: 23" x 23" x 9" interior (2.8 cu ft), lid '
                 'and wall elements, fires to 1700°F, 208/240 V. Fits large platters.',
    ),
    "8316355903810": dict(
        model="2313G", family="glass", shape="round", ctrl="bartlett3", large_glass=True,
        interior='23.5" across x 13.5" deep', cuft=None, sections=1,
        volts="208/240", amps=("30", "35"), breaker="40 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 2313G Glass Fusing Kiln | 23.5" x 13.5" Deep',
        seo_desc='Cone Art 2313G glass fusing kiln: 23.5" across x 13.5" deep, elements in lid '
                 'and walls, 208/240 V on a 40 A breaker. Room for large and deeper pieces.',
    ),
    "8316356034882": dict(
        model="2313G-SQ", family="glass", shape="square", ctrl="bartlett3",
        interior='23" x 23" x 13.5" deep', cuft="4.2", sections=2,
        volts="208/240", amps=("30", "35"), breaker="40 A", max_temp="1700°F",
        seo_title='Cone Art 2313G-SQ Square Glass Kiln | 23" x 23" x 13.5"',
        seo_desc='Cone Art 2313G-SQ square glass fusing kiln: 23" x 23" x 13.5" interior '
                 '(4.2 cu ft), fires to 1700°F, 208/240 V on a 40 A breaker. CSA approved.',
    ),
    "8316356460866": dict(
        model="2809G", family="glass", shape="round", ctrl="bartlett3", large_glass=True,
        interior='28" across x 9" deep', cuft="3.3", sections=1,
        volts="208/240", amps=("42", "48"), breaker="60 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 2809G Glass Fusing Kiln | 28" x 9" Deep',
        seo_desc='Cone Art 2809G glass fusing kiln: a full 28" across x 9" deep (3.3 cu ft), '
                 'elements in lid and walls, 208/240 V. Built for large fused and slumped pieces.',
    ),
    "8316356657474": dict(
        model="2813G", family="glass", shape="round", ctrl="bartlett3", large_glass=True,
        interior='28" across x 13.5" deep', cuft="5", sections=2,
        volts="208/240", amps=("42", "48"), breaker="60 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 2813G Glass Fusing Kiln | 28" x 13.5" Deep',
        seo_desc='Cone Art 2813G glass fusing kiln: 28" x 13.5" deep (5 cu ft), 3" brick walls '
                 'and lid, elements in lid and walls, 208/240 V. For large-volume fusing.',
    ),
    "8316356854082": dict(
        model="4209G", family="glass", shape="oval", ctrl="bartlett3", large_glass=True,
        interior='41" x 31" x 9" deep', cuft="5.5", sections=1,
        volts="208/240", amps=("48", "55"), breaker="60 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 4209G Oval Glass Fusing Kiln | 41" x 31" x 9"',
        seo_desc='Cone Art 4209G oval glass fusing kiln: 41" x 31" x 9" interior (5.5 cu ft), '
                 '3" lid and walls, elements in lid and walls, 208/240 V. For big glass work.',
    ),
    "8316357050690": dict(
        model="4213G", family="glass", shape="oval", ctrl="bartlett3", large_glass=True,
        interior='41" x 31" x 13.5" deep', cuft="8.25", sections=2,
        volts="208/240", amps=("48", "55"), breaker="60 A",
        elements="Kanthal A-1 elements in the lid and walls",
        seo_title='Cone Art 4213G Oval Glass Fusing Kiln | 41" x 31" x 13.5"',
        seo_desc='Cone Art 4213G oval glass kiln: 41" x 31" x 13.5" deep (8.25 cu ft), the '
                 'largest Cone Art glass kiln. Lid and wall elements, 3" walls, 208/240 V.',
        product_type="Glass Kilns", item_class="Glass Kilns", category=CATEGORY_GLASS_KILNS,
    ),
    # ---------------------------------------------------------- BX pottery
    "8316357574978": dict(
        model="BX119D", family="pottery", shape="round", ctrl="bartlett12", test_kiln=True,
        interior='11" across x 9" deep', cuft="0.57", sections=1,
        volts="120", amps="18", breaker="20 A",
        plug_note="It comes with a cord set and a 20 A NEMA 5-20 plug, which is not a standard household outlet.",
        floor_element=False,
        seo_title="Cone Art BX119D 120V Cone 10 Test Kiln | 0.57 cu ft",
        seo_desc='Cone Art BX119D test kiln fires to cone 10 on 120 V (18 A, 20 A circuit, '
                 'NEMA 5-20 plug). Double-wall, 11" x 9" interior, Bartlett 12-key controller.',
        kiln_type="Test Kiln", voltage="120 Volt",
    ),
    "8316357673282": dict(
        model="BX1813D", family="pottery", shape="round", ctrl="bartlett12",
        interior='17.5" across x 13.5" deep', cuft=None, sections=1,
        volts="208/240", amps=("19", "21"), breaker="30 A", floor_element=False,
        seo_title='Cone Art BX1813D Pottery Kiln | 17.5" x 13.5", Cone 10',
        seo_desc='Cone Art BX1813D double-wall pottery kiln: 17.5" x 13.5" interior, true cone '
                 '10, 208/240 V on a 30 A breaker, Bartlett 12-key controller. Classroom size.',
    ),
    "15060527087987": dict(
        model="BX1818D", family="pottery", shape="round", ctrl="bartlett12",
        interior='17.5" across x 18" deep', cuft="2.64", sections=1,
        volts="208/240", amps=("24", "28"), zones=2, floor_element=True,
        seo_title="Cone Art BX1818D Pottery Kiln | 2.64 cu ft, Cone 10",
        seo_desc='Cone Art BX1818D double-wall pottery kiln: 17.5" x 18" interior (2.64 cu ft), '
                 'cone 10, floor element and 2-zone Bartlett 12-key control, 208/240 V.',
        short_desc="Cone Art BX1818D double-wall round ceramics kiln with Bartlett 12-key controller",
    ),
    "8316357837122": dict(
        model="BX1822D", family="pottery", shape="round", ctrl="bartlett12",
        interior='17.5" across x 22.5" deep', cuft="3.3", sections=1,
        volts="208/240", amps=("28", "32"), breaker="40 A", zones=2, floor_element=True,
        seo_title="Cone Art BX1822D Pottery Kiln | 3.3 cu ft, Cone 10",
        seo_desc='Cone Art BX1822D double-wall pottery kiln: 17.5" x 22.5" interior (3.3 cu ft), '
                 'cone 10, floor element, 2-zone Bartlett 12-key control, 208/240 V.',
    ),
    "8316358132034": dict(
        model="BX2318D", family="pottery", shape="round", ctrl="bartlett12",
        interior='23.5" across x 18" deep', cuft="4.7", sections=2,
        volts="208/240", amps=("35", "40"), breaker="50 A", zones=2,
        seo_title="Cone Art BX2318D Pottery Kiln | 4.7 cu ft, Cone 10",
        seo_desc='Cone Art BX2318D double-wall pottery kiln: 23.5" x 18" interior (4.7 cu ft) '
                 'for easy loading, cone 10, 2-zone Bartlett 12-key control, 208/240 V.',
    ),
    "8316358295874": dict(
        model="BX2318D-SQ", family="pottery", shape="square", ctrl="bartlett12",
        interior='23" x 23" x 18" deep', cuft="5.6", sections=2,
        volts="208/240", amps=("40", "46"), zones=2, floor_element=True,
        seo_title="Cone Art BX2318D-SQ Square Pottery Kiln | 5.6 cu ft, Cone 10",
        seo_desc='Cone Art BX2318D-SQ square pottery kiln: 23" x 23" x 18" interior (5.6 cu ft), '
                 'cone 10, double wall, floor element, 2-zone Bartlett 12-key control.',
        short_desc="Cone Art BX2318D-SQ square ceramics kiln, 5.6 cubic feet, cone 10",
    ),
    "8316358492482": dict(
        model="BX2322D", family="pottery", shape="round", ctrl="bartlett12",
        interior='23.5" across x 22.5" deep', cuft="5.83", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"), zones=3, floor_element=True,
        seo_title="Cone Art BX2322D Pottery Kiln | 5.83 cu ft, Cone 10",
        seo_desc='Cone Art BX2322D double-wall pottery kiln: 23.5" x 22.5" interior (5.83 cu ft) '
                 'for easy loading, cone 10, 3-zone control, floor element, 208/240 V.',
    ),
    "8316358656322": dict(
        model="BX2322D-SQ", family="pottery", shape="square", ctrl="bartlett12",
        interior='23" x 23" x 22.5" deep', cuft="7", sections=3,
        volts="208/240", amps=("55", "63"), amps3=("31.9", "36.3"), zones=3, floor_element=True,
        phase_variants=True,
        seo_title="Cone Art BX2322D-SQ Square Pottery Kiln | 7 cu ft, Cone 10",
        seo_desc='Cone Art BX2322D-SQ square pottery kiln: 23" x 23" x 22.5" interior (7 cu ft), '
                 'cone 10, 3 zones plus floor element. 240 V or 208 V, single or 3 phase.',
    ),
    "8316358918466": dict(
        model="BX2327D", family="pottery", shape="round", ctrl="bartlett12",
        interior='23.4" across x 27" deep', cuft="7", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"), zones=3, floor_element=True,
        plug_note="It ships without a plug on its cord and is hard-wired.",
        seo_title="Cone Art BX2327D Double-Wall Pottery Kiln | 7 cu ft, Cone 10",
        seo_desc='Cone Art BX2327D, Cone Art\'s most popular kiln: 7 cu ft, 23.4" x 27" interior, '
                 'cone 10, 3-zone Bartlett 12-key control, floor element, 208/240 V.',
    ),
    "8316357378370": dict(
        model="BX2327D-SQ", family="pottery", shape="square", ctrl="bartlett12",
        interior='23" x 23" x 27" deep', cuft="8.4", sections=3,
        volts="208/240", amps=("55", "63"), amps3=("31.9", "36.3"), zones=3, floor_element=True,
        seo_title="Cone Art BX2327D-SQ Square Pottery Kiln | 8.4 cu ft, Cone 10",
        seo_desc='Cone Art BX2327D-SQ square pottery kiln: 23" x 23" x 27" interior (8.4 cu ft) '
                 'on 21" x 21" shelves, cone 10, 3-zone control, floor element, 208/240 V.',
    ),
    "8316359115074": dict(
        model="BX2336D", family="pottery", shape="oval", ctrl="bartlett12",
        interior='36" x 26" x 27" deep', cuft="12", sections=3,
        volts="208/240", amps=("69", "79.9"), amps3=("39.7", "45.8"), zones=3, floor_element=True,
        seo_title="Cone Art BX2336D Oval Pottery Kiln | 12 cu ft, Cone 10",
        seo_desc='Cone Art BX2336D oval pottery kiln: 36" x 26" x 27" interior (12 cu ft) for '
                 'wide sculpture and production loads. Cone 10, double wall, 3-zone control.',
    ),
    "8316359344450": dict(
        model="BX2818D", family="pottery", shape="round", ctrl="bartlett12",
        interior='28" across x 18" deep', cuft=None, sections=2,
        volts="208/240", amps=("47.1", "54.3"), zones=2, floor_element=True,
        seo_title='Cone Art BX2818D Pottery Kiln | 28" x 18" Deep, Cone 10',
        seo_desc='Cone Art BX2818D double-wall pottery kiln: 28" across x 18" deep for wide '
                 'platters and easy loading. Cone 10, floor element, 2-zone control, 208/240 V.',
    ),
    "8316359606594": dict(
        model="BX2822D", family="pottery", shape="round", ctrl="bartlett12",
        interior='28" across x 22.5" deep', cuft="8.33", sections=3,
        volts="208/240", amps=("63", "72.5"), amps3=("36.6", "41.9"), zones=3, floor_element=True,
        seo_title="Cone Art BX2822D Pottery Kiln | 8.33 cu ft, Cone 10",
        seo_desc='Cone Art BX2822D double-wall pottery kiln: 28" x 22.5" interior (8.33 cu ft) '
                 'for 26" shelves, cone 10, 3-zone control, floor element, 208/240 V.',
    ),
    "8316359901506": dict(
        model="BX2827D", family="pottery", shape="round", ctrl="bartlett12",
        interior='28" across x 27" deep', cuft="10", sections=3,
        volts="208/240", amps=("63", "72.5"), amps3=("36.3", "41.9"), zones=3, floor_element=True,
        seo_title="Cone Art BX2827D Pottery Kiln | 10 cu ft, Cone 10",
        seo_desc='Cone Art BX2827D production pottery kiln: 28" x 27" interior (10 cu ft), fires '
                 'to cone 10 even with heavy loads. 3-zone Bartlett 12-key control, 208/240 V.',
    ),
    "8316360065346": dict(
        model="BX4222D", family="pottery", shape="oval", ctrl="bartlett12",
        interior='an oval roughly 42" x 31" and 22.5" deep', cuft="13.7", sections=3,
        volts="208/240", amps=("75", "79.9"), amps3=("43.3", "46.1"), zones=3, floor_element=True,
        seo_title="Cone Art BX4222D Oval Pottery Kiln | 13.7 cu ft, Cone 10",
        seo_desc='Cone Art BX4222D oval pottery kiln: 13.7 cu ft with a 22.5" loading depth for '
                 'production and sculpture studios. Cone 10, double wall, 3-zone control.',
    ),
    "8316360294722": dict(
        model="BX4227D", family="pottery", shape="oval", ctrl="bartlett12",
        interior='41" x 31" x 27" deep', cuft="16.5", sections=3,
        volts="208/240", amps=("75", "79.9"), amps3=("43.3", "46.1"), zones=3, floor_element=True,
        seo_title="Cone Art BX4227D Oval Pottery Kiln | 16.5 cu ft, Cone 10",
        seo_desc='Cone Art BX4227D oval pottery kiln: 16.5 cu ft, 41" x 31" x 27" interior for '
                 'busy production and sculpture studios. Cone 10, double wall, 3-zone control.',
    ),
    # ---------------------------------------------------------- GX pottery
    "8316360425794": dict(
        model="GX119D", family="pottery", shape="round", ctrl="genesis", test_kiln=True,
        interior='11" across x 9" deep', cuft="0.57", sections=1,
        volts="120", amps="18", breaker="20 A",
        plug_note="It comes with a cord set and a 20 A NEMA 5-20 plug, which is not a standard household outlet.",
        floor_element=False,
        seo_title="Cone Art GX119D 120V Test Kiln | Genesis Touchscreen",
        seo_desc='Cone Art GX119D cone 10 test kiln on 120 V (18 A, NEMA 5-20 plug) with the '
                 'Bartlett Genesis touchscreen controller. Double-wall, 11" x 9" interior.',
        kiln_type="Test Kiln", voltage="120 Volt", kiln_style="Top Loading", gas_or_electric="Electric",
    ),
    "8316360589634": dict(
        model="GX1813D", family="pottery", shape="round", ctrl="genesis",
        interior='17.5" across x 13.5" deep', cuft=None, sections=1,
        volts="208/240", amps=("19", "21"), breaker="30 A", floor_element=False,
        seo_title="Cone Art GX1813D Genesis Touchscreen Kiln | Cone 10",
        seo_desc='Cone Art GX1813D double-wall pottery kiln with Wi-Fi Bartlett Genesis '
                 'touchscreen: 17.5" x 13.5" interior, true cone 10, 208/240 V, 30 A breaker.',
        short_desc="Cone Art GX1813D double-wall ceramics kiln with Wi-Fi Genesis touchscreen controller",
    ),
    "8316360720706": dict(
        model="GX2322D", family="pottery", shape="round", ctrl="genesis",
        interior='23.5" across x 22.5" deep', cuft="5.83", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"), zones=3, floor_element=True,
        seo_title="Cone Art GX2322D Genesis Touchscreen Kiln | 5.83 cu ft",
        seo_desc='Cone Art GX2322D pottery kiln with Bartlett Genesis touchscreen: 23.5" x 22.5" '
                 'interior (5.83 cu ft), cone 10, double wall, 3-zone control, 208/240 V.',
    ),
    "8316361212226": dict(
        model="GX2327D", family="pottery", shape="round", ctrl="genesis",
        interior='23.4" across x 27" deep', cuft="7", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"), zones=3, floor_element=True,
        phase_variants=True,
        plug_note="It ships without a plug on its cord and is hard-wired.",
        seo_title="Cone Art GX2327D Genesis Touchscreen Kiln | 7 cu ft, Cone 10",
        seo_desc='Cone Art GX2327D pottery kiln with Wi-Fi Bartlett Genesis touchscreen: 7 cu ft, '
                 '23.4" x 27" interior, cone 10, 3-zone control. 240/1, 208/1 or 208/3.',
    ),
    "8316361670978": dict(
        model="GX2827D", family="pottery", shape="round", ctrl="genesis",
        interior='28" across x 27" deep', cuft="10", sections=3,
        volts="208/240", amps=("63", "72.5"), amps3=("36.3", "41.9"), zones=3, floor_element=True,
        phase_variants=True,
        seo_title="Cone Art GX2827D Genesis Touchscreen Kiln | 10 cu ft",
        seo_desc='Cone Art GX2827D production kiln with Bartlett Genesis touchscreen: 28" x 27" '
                 'interior (10 cu ft), cone 10 with heavy loads, 3-zone control, 208/240 V.',
    ),
    # ------------------------------------------------------------ packages
    "8316360917314": dict(
        model="GX2322D", family="package", shape="round", ctrl="genesis",
        interior='23.5" across x 22.5" deep', cuft="5.83", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"),
        vent="a factory-installed, automated Orton kiln vent",
        seo_title="Cone Art GX2322D Kiln Package | Vent, Furniture, Genesis",
        seo_desc='Cone Art GX2322D kiln package: 5.83 cu ft cone 10 kiln with Bartlett Genesis '
                 'touchscreen, factory-installed Orton vent and furniture kit.',
        category=CATEGORY_CERAMIC_KILNS,
    ),
    "8316361081154": dict(
        model="GX2322D-SQ", family="package", shape="square", ctrl="genesis",
        interior='23" x 23" x 22.5" deep', cuft="7", sections=3,
        volts="208/240", amps=("55", "63"), amps3=("31.9", "36.3"), phase_variants=True,
        vent="a factory-installed Orton kiln vent",
        seo_title="Cone Art GX2322D-SQ Square Kiln Package | Vent & Furniture",
        seo_desc='Cone Art GX2322D-SQ square kiln package: 7 cu ft cone 10 kiln, Genesis '
                 'touchscreen, factory-installed Orton vent and cone 11 high-alumina furniture.',
        category=CATEGORY_CERAMIC_KILNS,
    ),
    "8316361441602": dict(
        model="GX2327D", family="package", shape="round", ctrl="genesis",
        interior='23.4" across x 27" deep', cuft="7", sections=3,
        volts="208/240", amps=("48", "55.4"), amps3=("27.6", "31.9"), phase_variants=True,
        vent="a factory-installed, automated Orton kiln vent",
        seo_title="Cone Art GX2327D Kiln Package | Vent, Furniture, Genesis",
        seo_desc='Cone Art GX2327D turnkey kiln package: 7 cu ft cone 10 kiln, Genesis '
                 'touchscreen, factory-installed Orton vent, furniture kit. 240/1, 208/1, 208/3.',
        category=CATEGORY_CERAMIC_KILNS,
    ),
    "15380548911475": dict(
        model="GX2327D-SQ", family="package", shape="square", ctrl="genesis",
        interior='23" x 23" x 27" deep', cuft="8.4", sections=3,
        volts="208/240", amps=("55", "63"), amps3=("31.9", "36.3"), phase_variants=True,
        vent="a factory-installed Orton kiln vent",
        seo_title="Cone Art GX2327D-SQ Square Kiln Package | Vent & Furniture",
        seo_desc='Cone Art GX2327D-SQ square kiln package: 8.4 cu ft cone 10 kiln, Genesis '
                 'touchscreen, factory-installed Orton vent and square-shelf furniture kit.',
        product_type="Kiln Packages", item_class="Kiln Packages",
        short_desc="Cone Art GX2327D-SQ square kiln package: Genesis touchscreen, factory-installed Orton vent and furniture kit",
        add_tags=["Cone Art Kilns Energy Efficient Kiln Packages"],
    ),
    "8316361900354": dict(
        model="GX2827D", family="package", shape="round", ctrl="genesis",
        interior='28" across x 27" deep', cuft="10", sections=3,
        volts="208/240", amps=("63", "72.5"), amps3=("36.3", "41.9"), phase_variants=True,
        vent="a factory-installed, automated Orton kiln vent",
        seo_title="Cone Art GX2827D Kiln Package | Vent, Furniture, Genesis",
        seo_desc='Cone Art GX2827D kiln package: 10 cu ft cone 10 production kiln, Wi-Fi '
                 'Genesis touchscreen, factory-installed Orton vent and cone 11 furniture kit.',
        category=CATEGORY_CERAMIC_KILNS,
    ),
    "8316362096962": dict(
        model="GX4227D", family="package", shape="oval", ctrl="genesis",
        interior='41" x 31" x 27" deep', cuft="16.5", sections=3,
        volts="208/240", amps=("75", "79.9"), amps3=("43.3", "46.1"),
        vent="a factory-installed Orton kiln vent with controller integration",
        seo_title="Cone Art GX4227D Oval Kiln Package | Vent & Furniture",
        seo_desc='Cone Art GX4227D oval kiln package: 16.5 cu ft cone 10 kiln, factory-installed '
                 'Orton vent with controller integration, furniture kit and Genesis.',
        category=CATEGORY_CERAMIC_KILNS, item_class="Kiln Packages",
        add_tags=["Cone Art Kilns Energy Efficient Kiln Packages"],
    ),
    # ---------------------------------------------------------------- part
    "8316362228034": dict(
        model="Thermocouple", family="part",
        seo_title='Cone Art 8" Type K Replacement Kiln Thermocouple',
        seo_desc='Replacement 8" type K thermocouple for double-wall Cone Art (Tucker), Shimpo '
                 'and Bailey top-loading kilns. Ceramic connection block not included.',
        category=CATEGORY_THERMOCOUPLES,
        faqs=[
            ("Which kilns does this Cone Art thermocouple fit?",
             'It is an 8" type K replacement thermocouple for double-wall Cone Art (Tucker), '
             "Shimpo and Bailey top-loading kilns."),
            ("Does the thermocouple include the ceramic connection block?",
             "No. The ceramic connection block rarely needs replacing. Call us at "
             "1-888-774-2529 if you need the version with the block."),
        ],
    ),
}

# Short, unambiguous text fixes inside existing product descriptions.
# (old, new[, expected_count]) - `old` must occur exactly expected_count times
# (default 1) or the plan aborts.
DESCRIPTION_FIXES = {
    # 117G page headline named a different kiln (BX1809).
    "8316355215682": [
        ("Tucker's CONE ART BX1809 GLASS FUSING KILN With Bartlett Control",
         "Tucker's Cone Art 117G Glass Fusing Kiln With Bartlett Control"),
    ],
    # 2809G overview was copied from the 2309G. Corrected to the 2809G's own
    # spec table (3.3 cu ft, 60 A breaker), which matches its sibling 2813G.
    "8316356460866": [
        ("<li>G 2309 - 2.3 Cubic ft</li>", "<li>G 2809 - 3.3 Cubic ft</li>"),
        ("<li>40 Amp breaker required</li>", "<li>60 Amp breaker required</li>"),
        ("The Tucker’s Cone Art Kiln model G2309 is the perfect size",
         "The Tucker’s Cone Art Kiln model G2809 is the perfect size"),
    ],
    "15060527087987": [("<li>208 or 204 Volts</li>", "<li>208 or 240 Volts</li>")],
    "8316358656322": [("The standard model is the BX12322D SQ.", "The standard model is the BX2322D SQ.")],
    "8316357378370": [
        ("yielding more stacking space than it’s cousin the 2327D SQ.",
         "yielding more stacking space than its cousin the 2327D."),
    ],
    # BX2318D-SQ breaker line was copied from the 2322/2327 square kilns; its
    # own spec table (40 A / 46 A draw) lists 50 A / 60 A.
    "8316358295874": [("<li>70 or 80 Amp breaker required</li>", "<li>50 or 60 Amp breaker required</li>")],
    "8316362096962": [
        ("The BX4227D double wall ceramic kiln is designed", "The GX4227D double wall ceramic kiln is designed"),
        ("wifi enabled Bartlet Genesis controller", "wifi enabled Bartlett Genesis controller"),
        ("Inside Dimenssions", "Inside Dimensions"),
    ],
    # Packages include the furniture kit (it is in the product title).
    "15380548911475": [
        ('<h2 class="abz-seo-product">Optional Furniture Kit</h2>',
         '<h2 class="abz-seo-product">Included Furniture Kit</h2>'),
    ],
    "8316361441602": [
        ("Optional Extra Furniture Kit Includes", "Included Furniture Kit"),
        ("Inside Dimenssions", "Inside Dimensions"),
    ],
    "8316361081154": [("Inside Dimenssions", "Inside Dimensions")],
}

# Fixes inside the custom.specifications spec-table metafield.
SPEC_FIXES = {
    # 11.5 kW at 208 V is 55 A (same as the 4209G); "45" was a typo.
    "8316357050690": [("<td>48 | 45</td>", "<td>48 | 55</td>")],
    "8316360425794": [("<td>20</td>", "<td>20A</td>")],
    "8316358492482": [("Inside Dimenssions", "Inside Dimensions")],
    "8316358918466": [("Inside Dimenssions", "Inside Dimensions")],
    "8316360294722": [("Inside Dimenssions", "Inside Dimensions")],
    "8316361212226": [("Inside Dimenssions", "Inside Dimensions")],
    "8316361670978": [("Inside Dimenssions", "Inside Dimensions")],
}

# The "Cone Art Glass Fusing Kilns" tag drives the Cone Art Glass Kilns
# collection; it is removed from every product that is not a glass kiln.
GLASS_COLLECTION_TAG = "Cone Art Glass Fusing Kilns"

# Values the store's own sources disagree on. Left out of all new copy.
DISPUTED_FACTS = [
    ("BX1813D / GX1813D", "capacity", "description says 1.7 cu ft, spec table says 1.98 cu ft"),
    ("BX2818D", "capacity", "description says 6.5 cu ft, spec table says 6.66 cu ft"),
    ("2313G", "capacity", "description says 3.5 cu ft, spec table says 3.4 cu ft"),
    ("BX2822D", "breaker", 'description lists "63 or 72.5 amp breaker" (those are the amp draws); spec table says 80 A / 90 A single phase, 50 A three phase'),
    ("BX2827D / GX2827D package", "breaker", "description says 70 or 80 A; spec table says 80 A / 90 A single phase, 50 A three phase"),
    ("BX4222D / BX4227D / GX4227D package", "breaker", "description says 80 or 90 A; spec table says 90 A single phase, 60 A three phase"),
    ("BX4222D", "interior", 'spec table says 41" x 32" x 22.5", description says 42" x 31" x 22.5"'),
    ("2809G", "wall thickness", 'description says 2.5" firebrick walls; the 2813G page says the 2809G and 2813G both have 3" brick walls and lid'),
]

# --------------------------------------------------------------------------
# Collections
# --------------------------------------------------------------------------
HUB_FAQS = [
    ("Do Cone Art pottery kilns really fire to cone 10?",
     "Yes. Every Cone Art pottery kiln we sell is rated to cone 10. Double-wall construction "
     "(2½\" of firebrick plus 1\" of block insulation) is what lets them reach cone 10 routinely "
     "while still being a good choice for cone 5–6 firing."),
    ("Which Cone Art kilns run on 120 volts?",
     "The BX119D and GX119D test kilns (18 A on a 20 A circuit, with a NEMA 5-20 plug), the 117G "
     "glass kiln, which plugs into a normal wall outlet, and the 115G-SQ glass kiln (18 A). Every "
     "other Cone Art model needs 208 V or 240 V service."),
    ("What is the difference between Cone Art BX and GX kilns?",
     "The controller. BX models use the Bartlett 12-key digital controller; GX models use the "
     "Bartlett Genesis touchscreen, which adds Wi-Fi remote monitoring. The kiln bodies are the same."),
    ("Are Cone Art kilns energy efficient?",
     "Cone Art's double-wall pottery kilns pair 2½\" of premium firebrick with 1\" of block "
     "insulation. Cone Art rates that at roughly 30% lower electricity use than a conventional "
     "2½\" brick kiln, with a cooler jacket and longer element life."),
    ("What comes in a Cone Art kiln package?",
     "A GX kiln with the Bartlett Genesis touchscreen controller, a factory-installed Orton "
     "kiln vent and a furniture kit with shelves, posts and kiln wash."),
    ("Who makes Cone Art kilns?",
     "Tucker's Cone Art Kilns. Frank Tucker of Tucker's Pottery Supplies started Cone Art in "
     "1982; it was sold to Shimpo America in 1998, and Frank Tucker re-acquired it in June 2006."),
]


def hub_description_html():
    """Evergreen, factual body for the Tucker's Cone Art Kilns hub collection."""
    faq_html = "".join(
        f"<h3>{html.escape(q, quote=False)}</h3>\n<p>{html.escape(a, quote=False)}</p>\n"
        for q, a in HUB_FAQS
    )
    return (
        "<h2>Cone Art Kilns: Cone 10 Pottery &amp; Glass Fusing Kilns</h2>\n"
        "<p>Sheffield Pottery carries Tucker's Cone Art electric kilns: double-wall pottery "
        "kilns rated to cone 10 in round, square and oval shapes, plus glass fusing kilns from "
        "the 120 V 117G to the 41\" x 31\" 4213G oval. Every kiln is top-loading with "
        "Kanthal A-1 elements and a stainless steel jacket.</p>\n"
        "<ul>\n"
        "<li><strong>BX pottery kilns:</strong> Bartlett 12-key digital controller, double-wall "
        "insulation and multi-zone control, with a floor element on most models. From the 120 V "
        "BX119D test kiln (0.57 cu ft) to the 16.5 cu ft BX4227D oval.</li>\n"
        "<li><strong>GX pottery kilns:</strong> the same kilns with the Wi-Fi enabled Bartlett "
        "Genesis touchscreen controller.</li>\n"
        "<li><strong>Kiln packages:</strong> GX kilns bundled with a factory-installed Orton vent "
        "and a furniture kit.</li>\n"
        "<li><strong>Glass fusing kilns (G series):</strong> elements in the lid for fusing, "
        "slumping and annealing; round, square and oval, 6\" to 13.5\" deep.</li>\n"
        "</ul>\n"
        "<p>Not sure which size or voltage fits your studio? Call our kiln experts at "
        "1-888-774-2529.</p>\n"
        + faq_html
        + '<p><a href="#abz_below_richtxt_id" role="button">Learn more about Cone Art '
        "double-wall construction</a></p>"
    )


COLLECTIONS = {
    # Brand hub (curated, tag-based, 39 kilns)
    "gid://shopify/Collection/441037128002": dict(
        handle="tucker-s-cone-art-kilns",
        seo_title="Cone Art Kilns: Cone 10 Pottery & Glass Fusing Kilns",
        seo_desc="Shop Cone Art electric kilns: double-wall cone 10 pottery kilns (BX keypad or "
                 "GX Genesis touchscreen), kiln packages and glass fusing kilns. Expert advice.",
        description_html=hub_description_html(),
        faqs=HUB_FAQS,
    ),
    # Vendor-rule collection that also listed 59 hidden option products.
    "gid://shopify/Collection/467367788866": dict(
        handle="cone-art-kilns",
        seo_title="Cone Art Kilns, Packages & Parts | Sheffield Pottery",
        seo_desc="All Cone Art products at Sheffield Pottery: cone 10 pottery kilns, glass fusing "
                 "kilns, turnkey kiln packages and replacement parts like thermocouples.",
        description_html=(
            "<p>Every Cone Art product we sell in one place: double-wall cone 10 pottery kilns, "
            "glass fusing kilns, turnkey kiln packages and replacement parts. For a guided "
            "overview of the lineup, see <a href=\"/collections/tucker-s-cone-art-kilns\">Cone "
            "Art Kilns: Cone 10 Pottery &amp; Glass Fusing Kilns</a>.</p>"
        ),
        add_rule=dict(column="TAG", relation="NOT_EQUALS", condition="HideOnStorefront"),
    ),
    "gid://shopify/Collection/443939520834": dict(
        handle="cone-art-cone-10-double-wall-automatic-electric-kilns",
        seo_title="Cone Art Cone 10 Pottery Kilns | Double-Wall Electric",
        seo_desc="Cone Art double-wall electric pottery kilns rated to cone 10: round, square and "
                 "oval, 0.57 to 16.5 cu ft, Bartlett keypad or Genesis touchscreen control.",
    ),
    "gid://shopify/Collection/443938341186": dict(
        handle="cone-art-glass-fusing-kilns",
        seo_title="Cone Art Glass Fusing Kilns | Round, Square & Oval",
        seo_desc="Cone Art glass kilns for fusing, slumping and annealing: 0.9 to 8.25 cu ft, "
                 "round, square and oval, 120 V and 208/240 V models with Bartlett control.",
        # strip CSS classes pasted in from a chat UI; content unchanged
        description_replace=[
            (' class="font-claude-response-body whitespace-normal break-words"', "", 2),
        ],
    ),
    "gid://shopify/Collection/441110430018": dict(
        handle="cone-art-kilns-energy-efficient-kiln-packages",
        seo_title="Cone Art Kiln Packages | Kiln, Vent, Furniture & Genesis",
        seo_desc="Turnkey Cone Art kiln packages: a double-wall cone 10 kiln with the Bartlett "
                 "Genesis touchscreen, a factory-installed Orton vent and a furniture kit.",
    ),
    # Empty (0-product) collections: keep out of search results and sitemap.
    "gid://shopify/Collection/446730830146": dict(
        handle="cone-art-kilns-upgrade-to-the-genesis-touch-screen-controller", seo_hidden=True,
    ),
    "gid://shopify/Collection/446730961218": dict(
        handle="cone-art-upgrade-to-touch-screen", seo_hidden=True,
    ),
}


# --------------------------------------------------------------------------
# Product FAQ copy
#
# Rendered visibly by the theme's "ABZ Faq" section (custom.product_faqs) and
# emitted as FAQPage JSON-LD by Booster SEO (custom.faqs), so the structured
# data always matches what shoppers see on the page.
# --------------------------------------------------------------------------
ELECTRICIAN = ("Have a licensed electrician confirm breaker and wire sizes for your "
               "installation; the manufacturer's figures are in the Specifications tab.")


def _size_answer(f):
    ans = f"The interior is {f['interior']}"
    if f.get("cuft"):
        unit = "cubic foot" if f["cuft"] == "1" else "cubic feet"
        ans += f", with {f['cuft']} {unit} of firing space"
    ans += "."
    if f.get("sections", 1) > 1:
        ans += f" The kiln body is built in {f['sections']} sections, which makes delivery and maintenance easier."
    return ans


def _electric_answer(f):
    if f["volts"] == "120":
        ans = f"It runs on 120 V and draws {f['amps']} A"
        if f.get("breaker"):
            ans += f" on a {f['breaker']} circuit"
        ans += "."
        if f.get("plug_note"):
            ans += " " + f["plug_note"]
        return ans
    a240, a208 = f["amps"]
    ans = (f"It runs on 240 V or 208 V. Single-phase current draw is {a240} A at 240 V "
           f"and {a208} A at 208 V")
    if f.get("amps3"):
        b240, b208 = f["amps3"]
        ans += f"; three-phase draw is {b240} A at 240 V and {b208} A at 208 V"
    ans += "."
    if f.get("phase_variants"):
        ans += " Choose 240 V single-phase, 208 V single-phase or 208 V three-phase when you order."
    if f.get("breaker"):
        ans += f" The spec calls for a {f['breaker']} breaker."
    if f.get("plug_note"):
        ans += " " + f["plug_note"]
    return ans + " " + ELECTRICIAN


def _controller_answer(f):
    zones = f", set up for {f['zones']}-zone control" if f.get("zones") else ""
    if f["ctrl"] == "genesis":
        return (f"The Bartlett Genesis touchscreen controller{zones}. It is Wi-Fi enabled for "
                "remote monitoring, but Wi-Fi isn't required to use its firing programs.")
    return ("A Bartlett 12-key digital controller, mounted in Cone Art's angled, easy-view "
            f"control panel{zones}.")


def _efficiency_answer(f):
    ans = ("Cone Art's double-wall construction pairs 2½\" of premium firebrick with 1\" of "
           "block insulation, which Cone Art rates at about 30% lower electricity use than a "
           "conventional 2½\" brick kiln, with a cooler jacket and longer element life.")
    if f.get("floor_element") is True and f.get("zones"):
        ans += " A floor element plus multi-zone control keeps temperatures even from top to bottom."
    elif f.get("floor_element") is False:
        ans += f" At this size the {f['model']} doesn't need a floor element."
    return ans


def product_faqs(f):
    """Return [(question, answer), ...] for one product's facts dict."""
    if "faqs" in f:
        return list(f["faqs"])
    m = f["model"]
    fam = f["family"]
    if fam == "glass":
        use = "Glass fusing, slumping and annealing."
        if f.get("elements"):
            use += f" It has {f['elements']} for even heat across the glass."
        if f.get("max_temp"):
            use += f" It fires to {f['max_temp']}."
        ctrl = ("The base price includes the Bartlett 3-key quick-set controller. The "
                "full-featured 12-key Bartlett V6 controller shown in the photos is available "
                "as an upgrade")
        ctrl += " and recommended for a kiln this size." if f.get("large_glass") else "."
        return [
            (f"What is the Cone Art {m} used for?", use),
            (f"What are the interior dimensions of the Cone Art {m}?", _size_answer(f)),
            (f"What electrical service does the Cone Art {m} need?", _electric_answer(f)),
            (f"Which controller comes with the Cone Art {m}?", ctrl),
            (f"Is kiln furniture included with the Cone Art {m}?",
             "No. An optional furniture kit with shelves, posts and kiln wash is available."),
        ]
    if fam == "package":
        return [
            (f"What's included in the Cone Art {m} kiln package?",
             f"The {m} cone 10 kiln with the Bartlett Genesis touchscreen controller, "
             f"{f['vent']} and a furniture kit with shelves, posts and kiln wash."),
            (f"What are the interior dimensions of the Cone Art {m}?", _size_answer(f)),
            (f"What electrical service does the Cone Art {m} need?", _electric_answer(f)),
            (f"What temperature is the Cone Art {m} rated for?",
             "Cone 10. " + _efficiency_answer(f)),
        ]
    # pottery kiln
    if f.get("test_kiln"):
        use_q = f"What is the Cone Art {m} used for?"
        use = (f"The {m} is a compact cone 10 test kiln that runs on 120 V. Use it for glaze "
               "tests and small pieces, or to mimic the firing curves of a larger kiln.")
    else:
        use_q = f"What can I fire in the Cone Art {m}?"
        use = (f"The {m} is a top-loading electric kiln rated to cone 10, so it handles "
               "high-fire stoneware and porcelain as well as cone 5–6 glazes, bisque and "
               "low-fire work.")
    return [
        (use_q, use),
        (f"What are the interior dimensions of the Cone Art {m}?", _size_answer(f)),
        (f"What electrical service does the Cone Art {m} need?", _electric_answer(f)),
        (f"Which controller comes with the Cone Art {m}?", _controller_answer(f)),
        (f"Is kiln furniture included with the Cone Art {m}?",
         "No. A matching furniture kit with shelves, posts and kiln wash is available as an option."),
        (f"Is the Cone Art {m} energy efficient?", _efficiency_answer(f)),
    ]


def product_attributes(f):
    """Standard category metafield values (metaobject handles) for one product."""
    if f["family"] == "part":
        return {}
    features = ["digital-controller", "programmable-firing-cycles"]
    if f["family"] in ("pottery", "package"):
        features.append("energy-efficient")
    if f.get("sections", 1) > 1:
        features.append("sectional-construction")
    if f["ctrl"] == "genesis":
        features.append("touchscreen")
    if f["family"] == "package":
        features.append("exhaust-vent-system")
    return {
        "shopify--kiln-features": features,
        "shopify--kiln-loading-style": ["top-loading"],
        "shopify--kiln-firing-atmosphere": ["oxidation"],
        "shopify--kiln-heating-element-type": ["kanthal-fecral-wire"],
        "shopify--power-source": ["ac-powered"],
        "shopify--shape": [f["shape"]],
    }


def faq_handle(f):
    slug = f["model"].lower().replace(" ", "-")
    if f["family"] == "package":
        slug += "-package"
    return f"cone-art-{slug}-faq"
