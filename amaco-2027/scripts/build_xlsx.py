"""Build the AMACO / Brent 2027 review workbook from plan.json.

usage: python3 -I build_xlsx.py <work_dir> <out.xlsx>
"""
import json, os, sys
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

base, out = sys.argv[1], sys.argv[2]
rows = json.load(open(os.path.join(base, 'plan.json')))
d = json.load(open(os.path.join(base, 'matches.json')))
sheet = d['sheet']

ARIAL = 'Arial'
F = Font(name=ARIAL, size=10)
FB = Font(name=ARIAL, size=10, bold=True)
FH = Font(name=ARIAL, size=10, bold=True, color='FFFFFF')
FT = Font(name=ARIAL, size=14, bold=True)
FN = Font(name=ARIAL, size=9, italic=True, color='555555')
HDR = PatternFill('solid', fgColor='1F4E78')
INPUT = PatternFill('solid', fgColor='FFF2CC')   # cells the reviewer may edit
FLAG = PatternFill('solid', fgColor='FCE4D6')
OKF = PatternFill('solid', fgColor='E2EFDA')
WRAP = Alignment(wrap_text=True, vertical='top')
MONEY = '$#,##0.00;($#,##0.00);-'
PCT = '0.0%;-0.0%;-'

live = lambda r: r['status'] in ('ACTIVE', 'UNLISTED')
gid_v = lambda r: f"gid://shopify/ProductVariant/{r['vid']}"

wb = Workbook()


def table_sheet(title, headers, data, widths, money_cols=(), pct_cols=(), text_cols=(), input_cols=(), note=None, tname=None):
    ws = wb.create_sheet(title)
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = FN
        ws.cell(1, 1).alignment = Alignment(wrap_text=True, vertical='top')
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=min(len(headers), 10))
        ws.row_dimensions[1].height = 42
        r0 = 2
    for c, h in enumerate(headers, 1):
        cell = ws.cell(r0, c, h)
        cell.font, cell.fill = FH, HDR
        cell.alignment = Alignment(wrap_text=True, vertical='center')
    ws.row_dimensions[r0].height = 30
    for i, rowvals in enumerate(data, r0 + 1):
        for c, val in enumerate(rowvals, 1):
            cell = ws.cell(i, c, val)
            cell.font = F
            h = headers[c - 1]
            if h in money_cols:
                cell.number_format = MONEY
            elif h in pct_cols:
                cell.number_format = PCT
            elif h in text_cols:
                cell.number_format = '@'
            if h in input_cols:
                cell.fill = INPUT
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 3)
    if data:
        ref = f"A{r0}:{get_column_letter(len(headers))}{r0 + len(data)}"
        t = Table(displayName=tname or title.replace(' ', '_').replace('&', 'and').replace('-', '_'), ref=ref)
        t.tableStyleInfo = TableStyleInfo(name='TableStyleLight1', showRowStripes=True)
        ws.add_table(t)
    return ws, r0


# ---------------------------------------------------------------- Price update (Jan 1)
upd = [r for r in rows if r['item'] and r['status'] != 'ARCHIVED' and (r['price_action'].startswith('UPDATE') or (r['cap_new'] != '' and r['price_action'].startswith('UPDATE')))]
upd.sort(key=lambda r: (r['product'], r['variant']))
H = ['Product', 'Variant', 'Status', 'SKU', 'AMACO Item #', 'AMACO Description', 'Current Price', '2026 List', '2027 List',
     'New Price (Jan 1)', 'Change $', 'Change %', 'Current Compare-at', 'New Compare-at', 'Variant ID']
data = []
for r in upd:
    data.append([r['product'], r['variant'], r['status'], r['sku'], r['item'], r['amaco_desc'], r['price'], r['p26'], r['p27'],
                 r['price_new'], None, None, r['cap'], r['cap_new'] if r['cap_new'] != '' else None, gid_v(r)])
ws, r0 = table_sheet('Jan 1 Price Update', H, data, [44, 30, 10, 14, 11, 34, 11, 10, 10, 12, 10, 9, 11, 11, 40],
                     money_cols={'Current Price', '2026 List', '2027 List', 'New Price (Jan 1)', 'Change $', 'Current Compare-at', 'New Compare-at'},
                     pct_cols={'Change %'}, text_cols={'AMACO Item #', 'SKU'}, input_cols={'New Price (Jan 1)', 'New Compare-at'},
                     note='Variants whose Sheffield price today equals AMACO\'s 2026 retail list. Proposed new price = 2027 retail list. '
                          'Brent wheels excluded (on hold). Yellow cells are editable; Change $ / % are formulas. Apply on Jan 1, 2027.',
                     tname='PriceUpdate')
for i in range(r0 + 1, r0 + 1 + len(data)):
    ws.cell(i, 11, f'=J{i}-G{i}').number_format = MONEY
    ws.cell(i, 12, f'=IF(G{i}=0,0,J{i}/G{i}-1)').number_format = PCT
    for c in (11, 12):
        ws.cell(i, c).font = F
n_upd = len(data)
end_upd = r0 + n_upd

# ---------------------------------------------------------------- Price review
rev = [r for r in rows if r['item'] and r['status'] != 'ARCHIVED' and (r['price_action'].startswith('REVIEW') or r['price_action'].startswith('NO CHANGE: list unchanged ('))]
rev += [r for r in rows if r['item'] and r['status'] != 'ARCHIVED' and r['cap_new'] != '' and not r['price_action'].startswith('UPDATE') and r not in rev]
NOTES = {
    '25147G': 'AMACO: 25147G = "Kit Ez-Lift 12 Sided" ($795 list). Our $760 matches the 10-sided kit price. Prices or part #s look SWAPPED with the Ex-247/270 kit.',
    '25148L': 'AMACO: 25148L = "Kit Ez-Lift 10 Sided 2 1/2" Brick" ($760 list). Our $795 matches the 12-sided kit price. Prices or part #s look SWAPPED with the Ex-399/1099/1266 kit.',
    '22628J': 'AMACO list for "Die Set Standard" is $89 -> $93. We charge $709. Likely a pricing error, or this listing is a different item.',
    '22785E': 'AMACO is nearly doubling list ($67 -> $125). We are at $87.',
    '22827F': 'AMACO list for the replacement cover is $12 -> $13. We charge $38.',
    '22930B': 'We are above AMACO list ($90 -> $100).',
    '22281F': 'We are above AMACO list ($90 -> $100).',
}
rev.sort(key=lambda r: (0 if r['item'] in NOTES else 1, r['product'], r['variant']))
H = ['Product', 'Variant', 'Status', 'SKU', 'AMACO Item #', 'AMACO Description', 'Current Price', '2026 List', '2027 List',
     'Our price vs 2026 list', 'Same % change would be', 'Current Compare-at', 'Suggested Compare-at', 'Decision: New Price', 'Note', 'Variant ID']
data = []
for r in rev:
    note = NOTES.get(r['item'], '')
    if not note and r['cap'] is not None and r['cap'] == r['p26']:
        note = 'Sale price under compare-at (= 2026 list). Compare-at can move to 2027 list; sale price is your call.'
    elif not note and r['price_action'].startswith('NO CHANGE: list unchanged'):
        note = 'AMACO list unchanged for 2027; our price is below list.'
    elif not note:
        note = 'Our price differs from AMACO 2026 list.'
    data.append([r['product'], r['variant'], r['status'], r['sku'], r['item'], r['amaco_desc'], r['price'], r['p26'], r['p27'],
                 None, None, r['cap'], r['cap_new'] if r['cap_new'] != '' else None, None, note, gid_v(r)])
ws, r0 = table_sheet('Price Review', H, data, [44, 26, 10, 12, 11, 30, 11, 10, 10, 11, 12, 11, 12, 12, 60, 40],
                     money_cols={'Current Price', '2026 List', '2027 List', 'Same % change would be', 'Current Compare-at', 'Suggested Compare-at', 'Decision: New Price'},
                     pct_cols={'Our price vs 2026 list'}, text_cols={'AMACO Item #', 'SKU'}, input_cols={'Decision: New Price', 'Suggested Compare-at'},
                     note='Our current price does NOT equal AMACO\'s 2026 list, so the new price needs a human decision. '
                          'Fill in "Decision: New Price" (yellow). Highlighted rows look like data errors worth fixing regardless of Jan 1.',
                     tname='PriceReview')
for i in range(r0 + 1, r0 + 1 + len(data)):
    ws.cell(i, 10, f'=IF(H{i}=0,0,G{i}/H{i}-1)').number_format = PCT
    ws.cell(i, 11, f'=IF(H{i}=0,G{i},ROUND(G{i}*I{i}/H{i},2))').number_format = MONEY
    for c in (10, 11):
        ws.cell(i, c).font = F
    if ws.cell(i, 5).value in NOTES:
        for c in range(1, 17):
            if ws.cell(i, c).fill != INPUT:
                ws.cell(i, c).fill = FLAG
    ws.cell(i, 15).alignment = WRAP
n_rev = len(data)

# ---------------------------------------------------------------- GTIN & MPN
gm = [r for r in rows if r['item'] or r['gtin_action']]
order = {'ADD': 0, 'FIX: restore leading zero': 1, 'FIX: replace test value': 1, 'REVIEW: barcode belongs to another AMACO item': 2,
         'REVIEW: barcode differs from AMACO': 2, 'HOLD: same item as an active listing': 3, 'OK': 4, '': 5}
gm.sort(key=lambda r: (0 if r['status'] == 'ACTIVE' else 1 if r['status'] == 'UNLISTED' else 2, r['product'], r['variant']))
H = ['Product', 'Variant', 'Status', 'SKU', 'Current Barcode', 'GTIN Action', 'New Barcode (UPC-A)', 'Current MPN (variant)',
     'MPN Action', 'New MPN (AMACO Item #)', 'Product-level part # (pdp_vendor_part_no)', 'AMACO Description', 'AMACO Status', 'Matched by', 'Variant ID']
data = []
for r in gm:
    cur_mpn = ' / '.join(x for x in (r['mpn_custom'], r['mpn_google']) if x)
    data.append([r['product'], r['variant'], r['status'], r['sku'], r['barcode'] or None, r['gtin_action'], r['gtin_new'] or None,
                 cur_mpn or None, r['mpn_action'], r['mpn_new'] or None, r['vp'] or None, r['amaco_desc'],
                 {'A': 'Active', 'D': 'Discontinued', 'F': 'FD (Discontinued & FD tab)'}.get(r['amaco_status'], ''), r['match_how'], gid_v(r)])
ws, r0 = table_sheet('GTIN & MPN', H, data, [44, 30, 10, 14, 15, 26, 16, 16, 22, 14, 16, 34, 14, 18, 40],
                     text_cols={'SKU', 'Current Barcode', 'New Barcode (UPC-A)', 'Current MPN (variant)', 'New MPN (AMACO Item #)', 'Product-level part # (pdp_vendor_part_no)'},
                     note='Every Shopify AMACO/Brent variant we could tie to an AMACO item. Barcode = AMACO UPC (12 digits, keep leading 0) -> Google GTIN. '
                          'MPN = AMACO Item # at VARIANT level (today only the product has one part #, so every colour/size shares it). Sorted Active first.',
                     tname='GtinMpn')
for i in range(r0 + 1, r0 + 1 + len(data)):
    a = ws.cell(i, 6).value or ''
    if a.startswith('ADD') or a.startswith('FIX'):
        ws.cell(i, 6).fill = OKF
    elif a.startswith('REVIEW') or a.startswith('HOLD'):
        ws.cell(i, 6).fill = FLAG
    m = ws.cell(i, 9).value or ''
    if m.startswith('ADD') or m.startswith('FIX'):
        ws.cell(i, 9).fill = OKF
n_gm = len(data)

# ---------------------------------------------------------------- Discontinued by AMACO
dis = [r for r in rows if r['item'] and r['amaco_status'] in ('D', 'F') and live(r)]
dis.sort(key=lambda r: (r['product'], r['variant']))
H = ['Product', 'Variant', 'Status', 'SKU', 'AMACO Item #', 'AMACO Description', 'AMACO Status', 'Current Price', '2027 List', 'Variant ID']
data = [[r['product'], r['variant'], r['status'], r['sku'], r['item'], r['amaco_desc'],
         'D' if r['amaco_status'] == 'D' else 'F', r['price'], r['p27'], gid_v(r)] for r in dis]
table_sheet('AMACO Discontinued', H, data, [44, 30, 10, 14, 11, 36, 10, 11, 10, 40],
            money_cols={'Current Price', '2027 List'}, text_cols={'AMACO Item #', 'SKU'},
            note='Live on our site, but AMACO lists them on its "Discontinued & FD" tab (status D or F). '
                 'Worth checking stock and deciding whether to mark "while supplies last" or retire.', tname='Discontinued')
n_dis = len(data)

# ---------------------------------------------------------------- Not on AMACO list
nol = [r for r in rows if not r['item'] and live(r)]
nol.sort(key=lambda r: (r['product'], r['variant']))
H = ['Product', 'Variant', 'Status', 'Vendor', 'SKU', 'Current Price', 'Current Barcode', 'Product-level part #', 'Variant ID']
data = [[r['product'], r['variant'], r['status'], r['vendor'], r['sku'], r['price'], r['barcode'] or None, r['vp'] or None, gid_v(r)] for r in nol]
table_sheet('Not on AMACO 2027 List', H, data, [46, 34, 10, 10, 14, 11, 15, 14, 40],
            money_cols={'Current Price'}, text_cols={'SKU', 'Current Barcode', 'Product-level part #'},
            note='Live AMACO/Brent variants that do not appear anywhere in the 2027 list (neither active nor discontinued tab). '
                 'No 2027 price to apply. Many are likely dropped by AMACO (e.g. LUG-52, V-316, TC gallons, TP 8 oz, 16/18/20" Plasti-Bats).',
            tname='NotOnList')
n_nol = len(data)

# ---------------------------------------------------------------- Data issues
issues = []
for r in rows:
    if r['gtin_action'].startswith('REVIEW: barcode belongs'):
        issues.append(['Wrong barcode', r['product'], r['variant'], r['status'], r['barcode'],
                       f"Barcode is AMACO's UPC for {r['bad_barcode']} ({next(s['desc'] for s in sheet if s['item']==r['bad_barcode'])}), not this class pack. Clear it."])
    if r['mpn_action'].startswith('FIX'):
        issues.append(['Test value in MPN field', r['product'], r['variant'], r['status'], r['mpn_custom'],
                       f"custom.pdp_mpn_number holds \"{r['mpn_custom']}\". Should be {r['item']}."])
for r in rows:
    if r['vendor'] == 'Roselli' and r['barcode'].startswith('039672'):
        issues.append(['AMACO-prefix barcode on non-AMACO product', r['product'], r['variant'], r['status'], r['barcode'],
                       "039672 is AMACO's UPC company prefix, but this UPC isn't on AMACO's 2027 list. Verify it's the real Roselli UPC."])
st = [r for r in rows if r['sku'] in ('AST55', 'AST56')]
if len(st) == 2:
    issues.append(['Duplicate barcode', 'ST-55 Lavender / ST-56 Violet (Stone Texture)', '', ' / '.join(r['status'] for r in st), st[0]['barcode'],
                   'Both listings share one barcode (ST-56\'s). ST-55 is archived; neither is on the 2027 list.'])
issues.append(['Duplicate UPC in AMACO\'s own sheet', '28647S Element Coil AH25 SF 208V 3Ph / 28885M Wire 14 Ga Black Insulation 1 Ft', '', '', '039672286474',
               "AMACO's price list gives both items the same UPC. AMACO UPCs embed the item number (039672 + 5 digits + check digit; true for 1,566 of 1,574 rows), so this one belongs to 28647S. 28885M's would be 039672288850. Confirm with AMACO before using it."])
multi = {}
for r in rows:
    if r['status'] == 'ACTIVE':
        multi.setdefault(r['pid'], []).append(r)
for pid, vs in multi.items():
    if len(vs) > 5 and vs[0]['vp']:
        issues.append(['One part # for many variants', vs[0]['product'], f'{len(vs)} variants', 'ACTIVE', vs[0]['vp'],
                       f"Product-level pdp_vendor_part_no = {vs[0]['vp']} applies to all {len(vs)} colours/sizes. If the Google feed reads MPN from here, every variant is sent with the same MPN. Variant-level MPNs (GTIN & MPN tab) fix this."])
issues.append(['Brent wheels: compare-at below price', '"Ship Direct" wheel listings', '', 'UNLISTED / ARCHIVED', '',
               'Ship-direct wheel listings have compare-at prices LOWER than the selling price (e.g. Model C $2,800 vs compare-at $2,700). Out of scope for now (wheels on hold).'])
H = ['Issue', 'Product', 'Variant', 'Status', 'Value', 'Detail / Suggested fix']
ws, r0 = table_sheet('Data Issues', H, issues, [30, 50, 22, 16, 18, 90], text_cols={'Value'}, tname='Issues')
for i in range(r0 + 1, r0 + 1 + len(issues)):
    ws.cell(i, 6).alignment = WRAP
    ws.cell(i, 2).alignment = WRAP

# ---------------------------------------------------------------- Summary (first tab)
ws = wb['Sheet']
ws.title = 'Summary'
wb.move_sheet('Summary', offset=-(len(wb.sheetnames) - 1))
ws.column_dimensions['A'].width = 58
ws.column_dimensions['B'].width = 14
ws.column_dimensions['C'].width = 70
ws['A1'] = 'AMACO / Brent 2027 Price List: Shopify Review'
ws['A1'].font = FT
ws['A2'] = ('Source: AMACO-brent 2027 Retail Price List (effective Jan 1, 2027): 1,339 active + 235 discontinued/FD items, every one with a 12-digit UPC. '
            'Compared against a live Shopify pull (Nov 24, 2026) of every product with vendor Amaco or Brent, or an AMACO-prefix barcode: '
            f'{len({r["pid"] for r in rows})} products / {len(rows)} variants.')
ws['A2'].font = F
ws['A2'].alignment = WRAP
ws.merge_cells('A2:C2')
ws.row_dimensions[2].height = 44

live_rows = [r for r in rows if live(r)]
gtin_c = Counter(r['gtin_action'] for r in live_rows)
mpn_c = Counter(r['mpn_action'] for r in live_rows if r['item'])
lines = [
    ('MATCHING', None, None),
    ('Variants matched to an AMACO item', sum(1 for r in rows if r['item']), 'By barcode, part #, or glaze code + size (e.g. "V-301 / PINT" -> 37501K). Every glaze-code match also agrees on the colour name.'),
    ('  of which live (Active/Unlisted)', sum(1 for r in live_rows if r['item']), None),
    ('Live variants not on the 2027 list', n_nol, "See 'Not on AMACO 2027 List'"),
    ('GTINs (barcodes), live variants', None, None),
    ('Already correct', gtin_c['OK'], None),
    ('Can ADD, currently blank', gtin_c['ADD'], 'The big win: today only ~1 in 9 AMACO/Brent variants has a barcode.'),
    ('Fix: leading zero was stripped (11 digits)', gtin_c['FIX: restore leading zero'], 'Excel-style damage; Google rejects 11-digit UPCs.'),
    ('Hold: duplicate listing of an active item', gtin_c['HOLD: same item as an active listing'], 'Kiln vent / ship-direct wheel twins. GTIN goes on the active listing only.'),
    ('MPNs (AMACO Item #), live variants', None, None),
    ('Can ADD at variant level', mpn_c['ADD'], 'Today only 5 variants have one (3 are test values).'),
    ('Fix test values (Test1 / Test2 / 123456)', mpn_c['FIX: replace test value'], None),
    ('JAN 1 PRICES (Brent wheels excluded)', None, None),
    ('Straight update: our price = 2026 list -> 2027 list', n_upd, "'Jan 1 Price Update' tab. Ready to apply."),
    ('Needs a decision (our price differs from list)', n_rev, "'Price Review' tab. Includes 3 likely data errors (Easy-Lift kits swapped, $709 die set)."),
    ('Already at 2027 list / no change', sum(1 for r in rows if r['item'] and r['status'] != 'ARCHIVED' and r['price_action'].startswith('NO CHANGE: already')), None),
    ('Brent wheels skipped', sum(1 for r in rows if r['is_wheel'] and r['status'] != 'ARCHIVED'), 'On hold per request.'),
    ('OTHER', None, None),
    ('Live items AMACO now lists as Discontinued / FD', n_dis, "'AMACO Discontinued' tab: all LUG 2 oz, Shino line, many Celadon 10 lb pails."),
    ('Data issues found', len(issues), "'Data Issues' tab"),
]
r = 4
for label, val, note in lines:
    if val is None and note is None:
        ws.cell(r, 1, label).font = FB
        r += 1
        continue
    ws.cell(r, 1, label).font = F
    c = ws.cell(r, 2, val)
    c.font = F
    c.number_format = '#,##0'
    if note:
        ws.cell(r, 3, note).font = F
        ws.cell(r, 3).alignment = WRAP
    r += 1
r += 1
ws.cell(r, 1, 'How to read').font = FB
r += 1
for t in ['Yellow cells are editable decisions. Change $ / % columns are live formulas.',
          'Variant ID is the Shopify GID used when writing changes back.',
          'AMACO status: A = active; D / F = on AMACO\'s "Discontinued & FD" tab.',
          'GTIN = Shopify variant Barcode (feeds Google GTIN). MPN target field to be confirmed: '
          'Google & YouTube "Google: MPN" (mm-google-shopping.mpn) and/or theme spec field custom.pdp_mpn_number.',
          'Nothing has been written to Shopify yet.']:
    ws.cell(r, 1, '• ' + t).font = F
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    ws.cell(r, 1).alignment = WRAP
    ws.row_dimensions[r].height = 28
    r += 1

wb.save(out)
print('wrote', out, '| upd', n_upd, 'rev', n_rev, 'gtin/mpn', n_gm, 'disc', n_dis, 'notonlist', n_nol, 'issues', len(issues))
