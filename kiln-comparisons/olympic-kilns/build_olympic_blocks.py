"""Build the Olympic family comparison blocks (shared-block format) from Olympic's
2026 price list numbers. Writes one file per block into the given folder.

    python3 build_olympic_blocks.py <out-dir>
"""
import os
import sys

out = sys.argv[1]
P = '/products/'
C = '/collections/'


def a(href, text):
    return f'<a href="{href}">{text}</a>'


def table(cols, rows):
    """cols: list of (header, data-label, nowrap). rows: list of (model_html, [cells])."""
    h = ['<div class="spc-table-wrap">', '<table>', '<thead>', '<tr>',
         '<th scope="col">Model</th>']
    h += [f'<th scope="col">{c[0]}</th>' for c in cols]
    h += ['</tr>', '</thead>', '<tbody>']
    for model, cells in rows:
        assert len(cells) == len(cols), (model, cells)
        h.append('<tr>')
        h.append(f'<td class="spc-model">{model}</td>')
        for (head, label, nowrap), v in zip(cols, cells):
            cls = ' class="spc-num"' if nowrap else ''
            h.append(f'<td data-label="{label}"{cls}>{v}</td>')
        h.append('</tr>')
    h += ['</tbody>', '</table>', '</div>']
    return '\n'.join(h)


def picks(title, items):
    h = [f'<h3>{title}</h3>', '<ul class="spc-picks">']
    h += [f'<li><strong>{t}</strong>{body}</li>' for t, body in items]
    h.append('</ul>')
    return '\n'.join(h)


def block(handle, h2id, h2, intro, parts):
    body = [f'<div class="spc-block" id="{handle}">', f'<h2 id="{h2id}">{h2}</h2>', f'<p>{intro}</p>', '']
    for p in parts:
        body += [p, '']
    body[-1] = '</div>'
    return '\n'.join(body) + '\n'


blocks = {}
PL = "Specs come from Olympic's current price list"
AMPS = ('Amps (240V / 208V)', 'Amps', True)
INSIDE_WD = ('Inside (width × depth)', 'Inside', True)
CAP = ('Capacity', 'Capacity', True)
HOOK = ('Hookup', 'Hookup', True)
BEST = ('Best for', 'Best for', False)
NEMA650 = 'NEMA 6-50 plug'
EITHER = 'NEMA 6-50 plug or direct wire'
DW = 'Direct wire'

# ---------------------------------------------------------------- Medallion
mas = lambda h, t: a(P + h, t)
blocks['olympic-medallion'] = block(
    'olympic-medallion', 'olympic-medallion-comparison', 'Olympic Medallion Artist Series Comparison',
    "Medallion Artist Series (MAS) kilns are Olympic's lower-cost cone 10 stackables. They have the same "
    "chamber sizes as Olympic's HE models, with 3\" brick and a green electrical box, and every model fires to "
    f"cone 10 (2350°F). {PL} and are for 240- or 208-volt, single-phase power.",
    [picks('Which Medallion kiln should I buy?', [
        ('Home studio', f"The {mas('olympic-medallion-artist-series-mas1818he-olmas1818he', 'MAS1818HE')} draws 21 amps at 240V and plugs into a NEMA 6-30 outlet. The {mas('olympic-medallion-artist-series-mas1823he-olmas1823he', 'MAS1823HE')} adds 4.5\" of height on a NEMA 6-50 plug."),
        ('Schools and community studios', f"The {mas('olympic-medallion-artist-series-mas2323he-olmas2323he', 'MAS2323HE')} or {mas('olympic-medallion-artist-series-mas2327he-olmas2327he', 'MAS2327HE')}: 5.83 and 7 cu ft, both on a NEMA 6-50 plug."),
        ('Big loads', f"The {mas('olympic-medallion-artist-series-mas2823he-8-34-olmas2823he', 'MAS2823HE')} or {mas('olympic-medallion-artist-series-mas28237he-olmas2827he', 'MAS2827HE')}: 28 1/4\" wide, 8.34 and 10 cu ft. The MAS2827HE is direct-wired."),
     ]),
     table([INSIDE_WD, CAP, AMPS, HOOK, BEST], [
        (mas('olympic-medallion-artist-series-mas1818he-olmas1818he', 'MAS1818HE'), ['17.5" × 18"', '2.63 cu ft', '21 / 24', 'NEMA 6-30 plug', 'A first cone 10 kiln on a 30-amp circuit']),
        (mas('olympic-medallion-artist-series-mas1823he-olmas1823he', 'MAS1823HE'), ['17.5" × 22.5"', '3.29 cu ft', '26.5 / 30', NEMA650, 'Home studios that need room for taller pieces']),
        (mas('olympic-medallion-artist-series-mas2323he-olmas2323he', 'MAS2323HE'), ['23 3/8" × 22.5"', '5.83 cu ft', '44 / 46', NEMA650, 'Classrooms and active home studios']),
        (mas('olympic-medallion-artist-series-mas2327he-olmas2327he', 'MAS2327HE'), ['23 3/8" × 27"', '7 cu ft', '47 / 48', NEMA650, 'Schools and busy studios']),
        (mas('olympic-medallion-artist-series-mas2823he-8-34-olmas2823he', 'MAS2823HE'), ['28 1/4" × 22.5"', '8.34 cu ft', '48 / 55', EITHER, 'Wide platters and big classroom loads']),
        (mas('olympic-medallion-artist-series-mas28237he-olmas2827he', 'MAS2827HE'), ['28 1/4" × 27"', '10 cu ft', '56 / 64', DW, 'The largest Medallion, for production work']),
     ]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V. Three-phase wiring is available on every model except the MAS1818HE and MAS1823HE. Have an electrician check your circuit before the kiln arrives.</p>'])

# ---------------------------------------------------------------- Freedom
fr = lambda h, t: a(P + h, t)
blocks['olympic-freedom'] = block(
    'olympic-freedom', 'olympic-freedom-comparison', 'Olympic Freedom Series Comparison',
    "Each Freedom package is a cone 10 Olympic kiln with a furniture kit, a kiln vent and a Freedom Kit of spare "
    "parts: two elements, a thermocouple, a pint of mortar, a crimping tool and a wiring schematic. Every model has "
    f"3\" brick and fires to cone 10 (2350°F). {PL} and are for 240- or 208-volt, single-phase power.",
    [picks('Which Freedom package should I buy?', [
        ('Tests and small work', f"The {fr('olympic-freedom-1414-he-kiln-olf1414he', 'Freedom 1414HE')}: 1.4 cu ft on a NEMA 6-30 plug."),
        ('Home studio', f"The {fr('olympic-freedom-1823-he-kiln-olf1823he', 'Freedom 1823HE')}: 3.29 cu ft on a NEMA 6-50 plug."),
        ('Schools and community studios', f"The {fr('olympic-freedom-2323-he-kiln-olf2323he', 'Freedom 2323HE')} or {fr('olympic-freedom-2327-he-kiln-olf2327he', 'Freedom 2327HE')}: 5.83 and 7 cu ft, both on a NEMA 6-50 plug."),
        ('Production potters', f"The {fr('olympic-freedom-2827-he-kiln-olf2827he', 'Freedom 2827HE')} (10 cu ft) or the oval {fr('olympic-freedom-2527-he-kiln-olf2527he', 'Freedom 2527HE')} (12.8 cu ft), both direct-wired."),
     ]),
     table([INSIDE_WD, CAP, AMPS, HOOK, BEST], [
        (fr('olympic-freedom-1414-he-kiln-olf1414he', 'Freedom 1414HE'), ['14.5" × 13.5"', '1.4 cu ft', '15 / 17', 'NEMA 6-30 plug', 'Glaze tests and small pieces']),
        (fr('olympic-freedom-1823-he-kiln-olf1823he', 'Freedom 1823HE'), ['17.5" × 22.5"', '3.29 cu ft', '26.5 / 30', NEMA650, 'Home studios']),
        (fr('olympic-freedom-2323-he-kiln-olf2323he', 'Freedom 2323HE'), ['23 3/8" × 22.5"', '5.83 cu ft', '44 / 46', NEMA650, 'Classrooms and active home studios']),
        (fr('olympic-freedom-2327-he-kiln-olf2327he', 'Freedom 2327HE'), ['23 3/8" × 27"', '7 cu ft', '47 / 48', NEMA650, 'Schools and busy studios']),
        (fr('olympic-freedom-2823-he-kiln-olf2823he', 'Freedom 2823HE'), ['28 1/4" × 22.5"', '8.34 cu ft', '48 / 55', EITHER, 'Wide platters and big loads']),
        (fr('olympic-freedom-2827-he-kiln-olf2827he', 'Freedom 2827HE'), ['28 1/4" × 27"', '10 cu ft', '56 / 64', DW, 'Production potters']),
        (fr('olympic-freedom-2527-he-kiln-olf2527he', 'Freedom 2527HE'), ['37" × 25" oval, 29" deep', '12.8 cu ft', '56 / 64', DW, 'The largest Freedom: an oval for long pieces']),
     ]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V. Three-phase wiring is available on every Freedom model except the 1414HE.</p>'])

# ---------------------------------------------------------------- Ovals
ov = lambda code: a(P + f'olympic-kilns-oval-electric-kiln-{code.lower()}-with-v6-cf-olo{code.lower()}', code + 'E')
blocks['olympic-oval'] = block(
    'olympic-oval', 'olympic-oval-kiln-comparison', 'Olympic Oval Kiln Comparison',
    "Olympic's oval kilns give you a long chamber for platters, long sculpture and big loads. They're 30\", 37\" or "
    "42\" wide and 20\" to 33.5\" deep, with 3\" brick and a lid-lift assist. Every model here fires to cone 10 "
    f"(2350°F). {PL} and are for 240- or 208-volt, single-phase power.",
    [picks('Which Olympic oval should I buy?', [
        ('Long pieces in a smaller space', f"The {ov('2018H')} or {ov('2023H')}: 30\" long, 5.85 and 7.2 cu ft, both on a NEMA 6-50 plug."),
        ('Studio production', f"The {ov('2523H')} or {ov('2527H')}: 37\" long, 10 and 12.8 cu ft."),
        ('The biggest loads', f"The {ov('3027H')} or {ov('3031H')}: 42\" long, 17.7 and 20.5 cu ft, direct-wired."),
     ]),
     table([('Inside', 'Inside', False), CAP, AMPS, HOOK, BEST], [
        (ov('2018H'), ['30" × 20", 20" deep', '5.85 cu ft', '41 / 47', NEMA650, 'Platters and long pieces in a smaller studio']),
        (ov('2023H'), ['30" × 20", 24.5" deep', '7.2 cu ft', '48 / 55', NEMA650, 'Long pieces with more height']),
        (ov('2027H'), ['30" × 20", 29" deep', '8.5 cu ft', '56 / 64', EITHER, 'Tall work in a 30" oval']),
        (ov('2518H'), ['37" × 25", 20" deep', '8.8 cu ft', '42 / 48', NEMA650, 'Wide platters, with an easy reach to the floor']),
        (ov('2523H'), ['37" × 25", 24.5" deep', '10 cu ft', '48 / 55', EITHER, 'Studio production']),
        (ov('2527H'), ['37" × 25", 29" deep', '12.8 cu ft', '56 / 64', DW, 'Big studio and classroom loads']),
        (ov('2531H'), ['37" × 25", 33.5" deep', '14.8 cu ft', '65 / 75', DW, 'Tall work in a 37" oval']),
        (ov('3018H'), ['42" × 30", 20" deep', '12.2 cu ft', '55 / 63', DW, 'The largest platters and tiles']),
        (ov('3023H'), ['42" × 30", 24.5" deep', '14.9 cu ft', '70 / 80', DW, 'Production potters']),
        (ov('3027H'), ['42" × 30", 29" deep', '17.7 cu ft', '80 / 92', DW, 'High-volume production']),
        (ov('3031H'), ['42" × 30", 33.5" deep', '20.5 cu ft', '85 / 98', DW, "Olympic's largest oval"]),
     ]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V; every oval here can also be wired three-phase. Olympic also builds ovals with lower amperage or a lower top temperature. Where Olympic lists "NEMA 6-50 plug or direct wire," tell us your voltage and we\'ll confirm the hookup.</p>'])

# ---------------------------------------------------------------- 120 volt
v = lambda h, t: a(P + h, t)
blocks['olympic-120v'] = block(
    'olympic-120v', 'olympic-120-volt-kiln-comparison', 'Olympic 120-Volt Kiln Comparison',
    "These Olympic kilns run on household 120-volt power. The HotBox models and the Doll/Test kiln fire to cone 10 "
    "(2350°F). A kiln with a NEMA 5-15 plug fits a standard household outlet; a NEMA 5-20 plug needs a 20-amp outlet. "
    f"{PL}.",
    [picks('Which 120-volt Olympic should I buy?', [
        ('Cone 10 glaze tests', f"The {v('olympic-hotbox-cone-10-top-loading-120-volt-electric-kiln-w-3-key', 'HotBox E')} or {v('olympic-hb86-top-loading-120-volt-electric-kiln-olhb86', 'HB86E')}. Both plug into a standard outlet."),
        ('Taller small pieces', f"The {v('olympic-hb89-top-loading-120-volt-electric-kiln-olhb89', 'HB89E')} (9\" deep) or the {v('olympic-doll-test-mini-oval-120-volt-kiln-olodt', 'Doll/Test')} kiln. Both have a hinged lid and fire to cone 10."),
        ('More room on 120 volts', f"The {v('olympic-1214-120-cone-4-top-loading-120-kiln-ol1214120', '1214-120E')} (0.86 cu ft, cone 4) or the {v('olympic-129-120-volt-kiln-cone-6-electric-kiln-ol129', '129E')} (0.58 cu ft, cone 6)."),
        ('Glass and ceramics on the road', f"The {v('olympic-traveler-kiln-glass-and-ceramic-combo-oltrav', 'Traveler')} has a lid element for glass, a folding lid and wheels. It fires to 2000°F."),
     ]),
     table([('Inside', 'Inside', False), CAP, ('Max temp', 'Max temp', True), ('Plug', 'Plug', True), BEST], [
        (v('olympic-hb64-top-loading-120-volt-electric-kiln-olhb64', 'HB64E'), ['6.5" × 6.5" × 4.5"', '0.11 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Test tiles and small jewelry']),
        (v('olympic-hotbox-cone-10-top-loading-120-volt-electric-kiln-w-3-key', 'HotBox E'), ['6.5" × 6.5" × 6.5"', '0.16 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Glaze tests']),
        (v('olympic-hb84-top-loading-120-volt-electric-kiln-olhb84', 'HB84E'), ['8" × 8" × 4.5"', '0.17 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Tiles and flat pieces']),
        (v('olympic-hb86-top-loading-120-volt-electric-kiln-olhb86', 'HB86E'), ['8" × 8" × 6.5"', '0.24 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Glaze tests and small pots']),
        (v('olympic-hb89-top-loading-120-volt-electric-kiln-olhb89', 'HB89E'), ['8" × 8" × 9"', '0.33 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Taller small pieces, with a hinged lid']),
        (v('olympic-doll-test-mini-oval-120-volt-kiln-olodt', 'Doll/Test'), ['11.25" × 7" × 9"', '0.3 cu ft', 'Cone 10 (2350°F)', 'NEMA 5-15', 'Dolls, figurines and tests, with a hinged lid']),
        (v('olympic-129-120-volt-kiln-cone-6-electric-kiln-ol129', '129E'), ['11.25" × 9"', '0.58 cu ft', 'Cone 6 (2250°F)', 'NEMA 5-20', 'Mid-fire pieces on household power']),
        (v('olympic-1214-120-cone-4-top-loading-120-kiln-ol1214120', '1214-120E'), ['11.25" × 13.5"', '0.86 cu ft', 'Cone 4 (2100°F)', 'NEMA 5-20', 'The most room on 120V, for low-fire work']),
        (v('olympic-traveler-kiln-glass-and-ceramic-combo-oltrav', 'Traveler'), ['11.5" × 11.5"', '0.84 cu ft', '2000°F', 'NEMA 5-20', 'Glass and low-fire ceramics; folds and rolls']),
     ]),
     '<p class="spc-note">All of these need a 20-amp breaker. A blank or bead collar adds 4.5" of depth to a HotBox (not the HB89E), but lowers its top temperature to 2000°F. Need cone 10 with more room? The ' + a(P + 'olympic-1414he-kiln-ol1414he', '1414HE') + ' test kiln (1.4 cu ft) runs on 240 volts.</p>'])

# ---------------------------------------------------------------- FL front loading
fl = [
    ('olympic-fl-4-5-front-loading-electric-kiln', 'FL4.5E', '18" × 18" × 24"', '4.5 cu ft', '36 / 40', NEMA650, 'A front loader for a smaller studio'),
    ('olympic-fl-5-5-front-loading-kiln-olfl55', 'FL5.5E', '20" × 20" × 24"', '5.5 cu ft', '36 / 40', NEMA650, 'Studio work without a direct-wire hookup'),
    ('olympic-fl-8-front-loading-kiln-olfl8', 'FL8E', '24" × 24" × 24"', '8 cu ft', '48 / 55.5', EITHER, 'Studio production'),
    ('olympic-kilns-fl-4-5-front-loading-electric-kiln', 'FL10E', '24" × 24" × 30"', '10 cu ft', '56 / 65', DW, 'Studios and schools'),
    ('fl-12-front-loading-olympic-kiln-olfl12', 'FL12E', '24" × 24" × 36"', '12 cu ft', '56 / 65', DW, 'Tall work and school loads'),
    ('fl-17-front-loading-olympic-kiln-olfl17', 'FL17E', '28" × 28" × 38"', '17 cu ft', '70 / 81', DW, 'Busy schools and production studios'),
    ('fl-20-front-loading-olympic-kiln-olfl20', 'FL20E', '28" × 28" × 45"', '20 cu ft', '80 / 93', DW, 'Production studios'),
    ('olympic-fl-24-front-loading-kiln-olfl24', 'FL24E', '34" × 34" × 36"', '24 cu ft', '85 / 98', DW, 'Wide production loads'),
    ('olympic-fl-27-front-loading-kiln-olfl27', 'FL27E', '36" × 36" × 36"', '27 cu ft', '90 / 104', DW, 'Universities and large production'),
    ('olympic-fl-31-front-loading-kiln-olfl31', 'FL31E', '36" × 36" × 41.5"', '31 cu ft', '100 / 115', DW, 'Large production and tall work'),
    ('olympic-fl-36-front-loading-electric-kiln', 'FL36E', '38" × 38" × 45"', '36 cu ft', '150 / 173', DW, 'High-volume production and industry'),
    ('olympic-fl-42-front-loading-kiln', 'FL42E', '35" × 46" × 45"', '42 cu ft', '160 / 184', DW, 'High-volume production and industry'),
    ('olympic-fl-53-front-loading-kiln-olfl53', 'FL53E', '46" × 46" × 45"', '53 cu ft', '175 / 202', DW, 'The largest FL we carry'),
]
F = {code: a(P + h, code) for h, code, *_ in fl}
blocks['olympic-fl'] = block(
    'olympic-fl', 'olympic-front-loading-kiln-comparison', 'Olympic FL Front-Loading Kiln Comparison',
    "Olympic's FL kilns are large-capacity electric kilns with a front door, so you load shelves standing up instead "
    "of reaching down. The number in the model name is the cubic feet (FL20E = 20 cu ft). Walls are 4.5\" insulating "
    "brick with 1\" ceramic fiberboard and a 1\" air space, inside a heavy angle-iron frame. Every FL model fires to "
    f"cone 10 (2350°F). {PL} and are for 240- or 208-volt, single-phase power.",
    [picks('Which FL kiln should I buy?', [
        ('Studio production', f"The {F['FL8E']}, a 24\" cube that Olympic lists for a NEMA 6-50 plug or direct wire, or the {F['FL12E']} for 12\" more height."),
        ('Schools and busy studios', f"The {F['FL17E']} or {F['FL20E']}: 17 and 20 cu ft, direct-wired."),
        ('Large production and industry', f"The {F['FL27E']} through {F['FL53E']}: 27 to 53 cu ft."),
        ('Ready-to-fire packages', 'Several FL sizes come as ' + a(C + 'olympic-kilns-front-loader-packages', 'complete FL packages') + '.'),
     ]),
     table([('Inside (W × D × H)', 'Inside', False), CAP, AMPS, HOOK, BEST],
           [(F[code], [ins, cap, amps, hook, best]) for h, code, ins, cap, amps, hook, best in fl]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V. Large-capacity Olympic kilns can also be wired for three-phase or 480 volts. Car versions of the FL10E and larger roll the door and floor out on 6-foot tracks. Olympic requires solid-state relays on kilns shipped to CA, CT, IL, MA, ME, MN, NH, NY, RI and VT. Olympic also quotes custom electric and gas kilns for heat treating, DPF filter cleaning and other industrial work.</p>'])

# ---------------------------------------------------------------- TL top loading commercial
tl = lambda h, t: a(P + h, t)
blocks['olympic-tl'] = block(
    'olympic-tl', 'olympic-top-loading-commercial-kilns', 'Olympic TL Top-Loading Commercial Kilns',
    "Olympic's TL kilns are large-capacity top loaders, built like the FL front loaders: 4.5\" insulating brick with "
    "1\" ceramic fiberboard and a 1\" air space, inside a heavy angle-iron frame. They fire to cone 10 (2350°F) and are "
    f"direct-wired. {PL} and are for 240- or 208-volt, single-phase power.",
    [table([('Inside (W × D × H)', 'Inside', False), CAP, AMPS, HOOK, BEST], [
        (tl('olympic-top-loading-commercial-electric-kiln-tl20-oltl20e', 'TL20E'), ['42" × 28" × 30"', '20 cu ft', '80 / 93', DW, 'Large loads you set from above']),
        (tl('olympic-top-loading-commercial-electric-kiln-tl543-oltl5432e', 'TL5432E'), ['54" × 36" × 32"', '36 cu ft', '150 / 173', DW, 'Big production loads and long work']),
     ]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V; both can also be wired three-phase. Olympic also lists the TL24E, TL4828E, TL4832E and TL5428E; call us if you need one of those sizes.</p>'])

# ---------------------------------------------------------------- Dual Media
dm = [
    ('olympic-dual-media-kiln-1818he-2-63-cu-ft-oldm1818he', 'DM1818HE', '17.5" × 18"', '2.63 cu ft', '29 / 32', NEMA650, 'Glass and pottery in a home studio'),
    ('olympic-dual-media-kiln-1823he-3-29-cu-ft-oldm1823he', 'DM1823HE', '17.5" × 22.5"', '3.29 cu ft', '34 / 38', NEMA650, 'Taller pottery, plus glass'),
    ('olympic-dual-media-kiln-2318he-4-7-cu-ft-oldm2318he', 'DM2318HE', '23 3/8" × 18"', '4.7 cu ft', '42 / 48', NEMA650, 'Wide glass pieces and classroom pottery'),
    ('olympic-dual-media-kiln-2323he-5-83-cu-ft-oldm2323he', 'DM2323HE', '23 3/8" × 22.5"', '5.83 cu ft', '52 / 54', DW, 'Schools that fire glass and clay'),
    ('olympic-dual-media-kiln-2327he-7-cu-ft-oldm2327he', 'DM2327HE', '23 3/8" × 27"', '7 cu ft', '56 / 63', DW, 'Busy studios'),
    ('olympic-dual-media-kiln-2818he-6-67-cu-ft-oldm2818he', 'DM2818HE', '28 1/4" × 18"', '6.67 cu ft', '48 / 54', EITHER, 'Large glass panels'),
    ('olympic-dual-media-kiln-2823he-8-34-cu-ft-oldm2823he', 'DM2823HE', '28 1/4" × 22.5"', '8.34 cu ft', '56 / 63', DW, 'Big glass and pottery loads'),
    ('olympic-dual-media-kiln-2827he-10-cu-ft-oldm2827he', 'DM2827HE', '28 1/4" × 27"', '10 cu ft', '64 / 72', DW, 'Production pottery, plus glass'),
    ('olympic-dual-media-kiln-2523he-oval-10-cu-ft-oldm2523he', 'DM2523HE', '37" × 25" oval, 24.5" deep', '10 cu ft', '56 / 63', DW, 'Long glass pieces and platters'),
    ('olympic-dual-media-kiln-3018he-oval-12-2-cu-ft-oldm3018he', 'DM3018HE', '42" × 30" oval, 20" deep', '12.2 cu ft', '67 / 71', DW, 'The largest glass panels'),
    ('olympic-dual-media-kiln-3023he-oval-14-9-cu-ft-oldm3023he', 'DM3023HE', '42" × 30" oval, 24.5" deep', '14.9 cu ft', '78 / 88', DW, 'The largest Dual Media we carry'),
]
D = {code: a(P + h, code) for h, code, *_ in dm}
blocks['olympic-dual-media'] = block(
    'olympic-dual-media', 'olympic-dual-media-kiln-comparison', 'Olympic Dual Media Kiln Comparison',
    "Olympic's Dual Media (DM) kilns fire both ceramics and glass. They're built with 3\" brick and fire to cone 10 "
    "(2350°F) for pottery, and a lid element for glass fusing is turned on with its own infinite switch. Olympic builds "
    f"the 23\"-wide and larger models with a lid-lift assist. {PL} and are for 240- or 208-volt, single-phase power.",
    [picks('Which Dual Media kiln should I buy?', [
        ('Home studio', f"The {D['DM1818HE']} or {D['DM1823HE']}: 2.63 and 3.29 cu ft, both on a NEMA 6-50 plug."),
        ('Schools', f"The {D['DM2318HE']} (NEMA 6-50 plug) or the direct-wired {D['DM2323HE']}."),
        ('Large glass pieces', f"The ovals: {D['DM2523HE']}, {D['DM3018HE']} and {D['DM3023HE']}, up to 42\" long."),
     ]),
     table([('Inside', 'Inside', False), CAP, AMPS, HOOK, BEST],
           [(D[code], [ins, cap, amps, hook, best]) for h, code, ins, cap, amps, hook, best in dm]),
     '<p class="spc-note">Amps are for single-phase power at 240V / 208V. Three-phase wiring is available on every model except the DM1818HE. For glass and ceramics on 120 volts, see the ' + a(P + 'olympic-traveler-kiln-glass-and-ceramic-combo-oltrav', 'Traveler') + '.</p>'])

# ---------------------------------------------------------------- Glass
g = lambda h, t: a(P + h, t)
blocks['olympic-glass'] = block(
    'olympic-glass', 'olympic-glass-kiln-comparison', 'Olympic Glass Kiln Comparison',
    "Olympic's glass kilns are made for fusing and slumping. In model names, GF means glass fusing and TLC means the "
    "kiln loads two ways: lift the top off, or open it like a clamshell. "
    f"{PL}.",
    [picks('Which Olympic glass kiln should I buy?', [
        ('First glass kiln', f"The {g('olympic-champ-glass-kiln-olchamp', 'Champ')} or {g('olympic-champ-xl-glass-kiln-olchampxl', 'Champ XL')}. Both plug into a standard household outlet."),
        ('More room on 120 volts', f"The {g('olympic-kilns-186gfetlc-furniture-ol186gfetlc', '186GFETLC')}: an 18\" square chamber on a NEMA 5-20 plug."),
        ('Larger panels', f"The {g('olympic-gf2etlc-glass-fusing-kiln-olgf2etlc', 'GF2ETLC')} (20\" square) or {g('olympic-gf3etlc-glass-fusing-kiln-olgf3etlc', 'GF3ETLC')} (25\" square), on 240 volts."),
        ('Glass and pottery', 'The ' + a(C + 'olympic-dual-media-kilns-kilns-for-ceramics-and-glass', 'Dual Media kilns') + ' fire glass with a lid element and pottery to cone 10.'),
     ]),
     table([('Inside', 'Inside', False), CAP, ('Max temp', 'Max temp', True), ('Power', 'Power', False), BEST], [
        (g('olympic-champ-glass-kiln-olchamp', 'Champ'), ['14.5" × 6"', '0.62 cu ft', '1700°F', '120V, NEMA 5-15 plug', 'A first glass kiln']),
        (g('olympic-champ-xl-glass-kiln-olchampxl', 'Champ XL'), ['14.5" × 14.5" × 6"', '0.73 cu ft', '1700°F', '120V, NEMA 5-15 plug', 'Square pieces on household power']),
        (g('olympic-glass-fusing-kiln-ol146gfetlc', '146GFETLC'), ['14.5" × 14.5" × 6"', '0.73 cu ft', '1700°F', '120V, NEMA 5-20 plug', 'Top or clamshell loading on 120V']),
        (g('olympic-kilns-186gfetlc-furniture-ol186gfetlc', '186GFETLC'), ['18" × 18" × 6"', '1.1 cu ft', '1550°F', '120V, NEMA 5-20 plug', 'The most room on 120V']),
        (g('olympic-gf2etlc-glass-fusing-kiln-olgf2etlc', 'GF2ETLC'), ['20" × 20" × 9"', '2.08 cu ft', '1700°F', '240V, 24 A, NEMA 6-50 plug', 'Larger panels and platters']),
        (g('olympic-gf3etlc-glass-fusing-kiln-olgf3etlc', 'GF3ETLC'), ['25" × 25" × 9"', '3.33 cu ft', '1700°F', '240V, 39 A, NEMA 6-50 plug', 'The largest panels we carry']),
        (g('olympic-hb86p-vitrigraph-kiln-olhb86v', 'HB86P Vitrigraph'), ['8" × 8" × 6.5"', '0.24 cu ft', 'Cone 10 (2350°F)', '120V, NEMA 5-15 plug', 'Pulling glass stringers and cane']),
        (g('olympic-traveler-kiln-glass-and-ceramic-combo-oltrav', 'Traveler'), ['11.5" × 11.5"', '0.84 cu ft', '2000°F', '120V, NEMA 5-20 plug', 'Glass and low-fire ceramics; folds and rolls']),
     ]),
     '<p class="spc-note">The GF2ETLC and GF3ETLC draw 28 and 40 amps at 208V. The HB86P Vitrigraph has an adjustable stand (23" to 33" high) and is controlled with an infinite switch.</p>'])

# ---------------------------------------------------------------- Electric raku
er = lambda h, t: a(P + h, t)
blocks['olympic-electric-raku'] = block(
    'olympic-electric-raku', 'olympic-electric-raku-kilns', 'Olympic Electric Raku Kilns',
    "Olympic's electric raku kilns lift the firing chamber with a hand crank. The heat stays in the chamber, and you can "
    f"reach your work from every side. You can bisque and glaze fire in them too. {PL}.",
    [table([INSIDE_WD, CAP, ('Max temp', 'Max temp', True), ('Power', 'Power', False), BEST], [
        (er('olympic-1214-electric-raku-kiln-ol1214eraku', '1214 Raku E'), ['11.25" × 13.5"', '0.86 cu ft', 'Cone 4 (2100°F)', '120V, 16 A, NEMA 5-20 plug', 'Raku on household power']),
        (er('olympic-1823-electric-raku-kiln-ol1823eraku', '1823 Raku E'), ['17.5" × 22.5"', '3.29 cu ft', 'Cone 8 (2300°F)', '240V / 208V, 26.25 / 30 A, NEMA 6-50 plug', 'Bigger raku loads']),
     ]),
     '<p class="spc-note">Olympic also makes TopHat electric kilns, which add a lid element for glass and fire to cone 10; call us about those. For gas raku, see the ' + a(C + 'olympic-gas-raku-and-torchbearer-kilns', 'Olympic gas raku kilns') + '.</p>'])

# ---------------------------------------------------------------- Gas raku and Torchbearer
gr = [
    ('olympic-raku-kiln-ol18raku', '18 Raku', '17.5" × 22.5"', '3.29 cu ft', '2', '120,000', 'Raku in a home studio or class'),
    ('olympic-23-raku-kiln-ol23raku', '23 Raku', '23 3/8" × 27"', '7 cu ft', '3', '240,000', 'Bigger raku pieces'),
    ('olympic-28-raku-kiln-propane-ol28raku', '28 Raku', '28.25" × 27"', '10 cu ft', '4', '280,000', 'The largest raku pieces (3" brick)'),
    ('olympic-1827-torch-bearer-kiln-ol1827g', '1827G Torchbearer', '17.5" × 27"', '3.95 cu ft', '2', '120,000', 'A first gas kiln for reduction firing'),
    ('2327-olympic-torch-bearer-kiln-ol2327g', '2327G Torchbearer', '23 3/8" × 27"', '7 cu ft', '3', '240,000', 'Studio reduction firing'),
    ('2331-olympic-torch-bearer-kiln-ol2331g', '2331G Torchbearer', '23 3/8" × 31.5"', '8.15 cu ft', '3', '240,000', 'Taller work'),
    ('2827-olympic-torch-bearer-kiln-ol2827g', '2827G Torchbearer', '28.25" × 27"', '10 cu ft', '4', '280,000', 'Wide loads (3" brick)'),
    ('2831-olympic-torch-bearer-kiln-ol2831g', '2831G Torchbearer', '28.25" × 31.5"', '11.67 cu ft', '4', '280,000', 'The largest Torchbearer (3" brick)'),
]
G = {code: a(P + h, code) for h, code, *_ in gr}
blocks['olympic-gas-raku'] = block(
    'olympic-gas-raku', 'olympic-gas-raku-torchbearer-comparison', 'Olympic Gas Raku and Torchbearer Kiln Comparison',
    "Olympic's updraft gas kilns run on propane or natural gas, use venturi burners and fire to cone 10 (2350°F). "
    "The Raku models lift the firing chamber with a hand crank for fast turn-around. The Torchbearer is a top-loading, "
    f"stackable gas kiln: add rings for more depth. {PL}.",
    [picks('Which Olympic gas kiln should I buy?', [
        ('Raku', f"The {G['18 Raku']} for most studios, or the {G['23 Raku']} and {G['28 Raku']} for bigger pieces."),
        ('Reduction firing', f"The {G['1827G Torchbearer']} to start, or the {G['2327G Torchbearer']} for 7 cu ft."),
        ('Large loads', f"The {G['2827G Torchbearer']} or {G['2831G Torchbearer']}: 10 and 11.67 cu ft, with 3\" brick."),
     ]),
     table([INSIDE_WD, CAP, ('Burners', 'Burners', True), ('BTU per hour', 'BTU/hr', True), BEST],
           [(G[code], [ins, cap, n, btu, best]) for h, code, ins, cap, n, btu, best in gr]),
     '<p class="spc-note">All of these need a 3/4" gas line. On propane, Olympic says the tank should be at least 5 gallons for the 1827G and 18 Raku, and 15 gallons for the 2327G, 23 Raku, 2827G and 28 Raku. In an enclosed space, Olympic says a gas kiln needs an exhaust hood vented to the outside.</p>'])

# ---------------------------------------------------------------- DownDraft gas
dd = [
    ('olympic-kilns-dd9-downdraft-kiln-oldd9', 'DD9', '23" × 23" × 30"', '9.2 cu ft', '3 / 180,000', '10 gal', 'A first large gas kiln'),
    ('dd12-olympic-downdraft-kiln-oldd12', 'DD12', '27" × 28" × 31"', '13.5 cu ft', '6 / 300,000', '15 gal', 'Studio reduction firing'),
    ('olympic-dd14-downdraft-gas-kiln-oldd14', 'DD14', '29" × 28" × 31"', '14.5 cu ft', '6 / 300,000', '18 gal', 'Studios and schools'),
    ('olympic-kilns-dd17-downdraft-gas-kiln-oldd17', 'DD17', '29" × 28" × 37"', '17.3 cu ft', '6 / 350,000', '21 gal', 'Taller work'),
    ('olympic-kilns-dd20-downdraft-gas-kiln-oldd20', 'DD20', '31" × 31" × 37"', '20.5 cu ft', '6 / 350,000', '24 gal', 'Production studios'),
    ('olympic-kilns-dd24-downdraft-gas-kiln-oldd24', 'DD24', '32" × 35" × 38"', '24.6 cu ft', '6 / 350,000', '29 gal', 'Universities and production'),
    ('olympic-kilns-dd30-downdraft-gas-kiln-oldd30', 'DD30', '36" × 36" × 40"', '30 cu ft', '8 / 375,000', '40 gal', 'High-volume production'),
    ('olympic-kilns-dd40-downdraft-gas-kiln-oldd40', 'DD40', '41" × 41" × 41"', '40 cu ft', '8 / 390,000', '48 gal', 'The largest DownDraft'),
]
DDL = {code: a(P + h, code) for h, code, *_ in dd}
blocks['olympic-downdraft'] = block(
    'olympic-downdraft', 'olympic-downdraft-gas-kiln-comparison', 'Olympic DownDraft Gas Kiln Comparison',
    "Olympic's DownDraft kilns are large-capacity gas kilns for propane or natural gas, rated to cone 10 (2350°F). "
    "The exhaust and intake are at the bottom, so they need a chimney or stack. Walls are 4.5\" insulating brick with "
    "1\" ceramic fiberboard (fiber walls are an option), inside an angle-iron frame with a stainless steel exterior. "
    f"{PL}.",
    [picks('Which DownDraft should I buy?', [
        ('First large gas kiln', f"The {DDL['DD9']} (9.2 cu ft) or {DDL['DD12']} (13.5 cu ft)."),
        ('Schools and production studios', f"The {DDL['DD17']} or {DDL['DD20']}: 17.3 and 20.5 cu ft of setting space."),
        ('High volume', f"The {DDL['DD24']}, {DDL['DD30']} or {DDL['DD40']}: up to 40 cu ft."),
     ]),
     table([('Setting space (W × D × H)', 'Inside', False), ('Usable capacity', 'Capacity', True), ('Burners / BTU per hour', 'Burners / BTU', True), ('Propane per cone 10 firing', 'Propane', True), BEST],
           [(DDL[code], [ins, cap, burn, lp, best]) for h, code, ins, cap, burn, lp, best in dd]),
     '<p class="spc-note">Setting space is the usable area inside the kiln. Every model also comes as a car kiln, and a vent hood adds 24" to the outside depth and height. Most DownDrafts need a 1" gas line; ask us about the DD9. Propane figures are gallons per cone 10 firing; Olympic says to buy a larger tank than that.</p>'])

# ---------------------------------------------------------------- jump list (main page only)
jump = [('olympic-stackable', 'Stackable (18", 23", 28")'), ('olympic-medallion', 'Medallion'), ('olympic-freedom', 'Freedom packages'),
        ('olympic-oval', 'Ovals'), ('olympic-120v', '120-volt'), ('olympic-fl', 'FL front-loading'), ('olympic-tl', 'TL top-loading'),
        ('olympic-dual-media', 'Dual Media'), ('olympic-glass', 'Glass'), ('olympic-electric-raku', 'Electric raku'),
        ('olympic-gas-raku', 'Gas raku & Torchbearer'), ('olympic-downdraft', 'DownDraft gas')]
blocks['olympic-jump'] = ('<div class="spc-block" id="olympic-jump">\n<p><strong>Compare Olympic kilns by type:</strong></p>\n<ul class="spc-jump">\n'
                          + '\n'.join(f'<li><a href="#{h}">{t}</a></li>' for h, t in jump) + '\n</ul>\n</div>\n')

os.makedirs(out, exist_ok=True)
for h, html in blocks.items():
    assert '<style' not in html and '1946' not in html and '$' not in html, h
    open(os.path.join(out, h + '.html'), 'w', encoding='utf-8').write(html)
    print(f'{h}: {len(html)} chars')
