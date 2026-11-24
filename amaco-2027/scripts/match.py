"""Match Sheffield Shopify AMACO/Brent variants to the AMACO 2027 price list.

usage: python3 -I match.py <amaco_price_list.xlsx> <shopify_variants.json> <work_dir>
writes <work_dir>/matches.json
"""
import json, re, sys, os
from collections import defaultdict
import pandas as pd

sheet_path, shop_path, base = sys.argv[1:4]
os.makedirs(base, exist_ok=True)
xl = pd.read_excel(sheet_path, sheet_name=None, dtype=str)
sheet = []
for tab, df in xl.items():
    df = df.fillna('')
    for _, r in df.iterrows():
        sheet.append(dict(
            tab=tab, item=r['Item #'].strip().upper(), upc=r['UPC'].strip(), status=r['Status'].strip(),
            desc=r['DESCRIPTION'].strip(), cat=r['Item Category'].strip(), catdesc=r['Item Category Description'].strip(),
            search=r['Search Description'].strip(), series=r['SERIES'].strip(), group=r['Prod Group Description'].strip(),
            ssu=r['SSU\nQty'].strip(), case=r['Case\nQty'].strip(),
            p26=float(r['2026 Retail Price']) if r['2026 Retail Price'] else None,
            p27=float(r['2027 Retail Price']) if r['2027 Retail Price'] else None))

CODE_RE = re.compile(r'\b([A-Za-z]{1,4})- ?(\d+)\b')


def norm_code(prefix, num):
    return f'{prefix.upper()}-{int(num)}'


def sheet_code(s):
    d = s['desc']
    m = re.match(r'UG Liq #(\d+)', d)
    if m:
        return norm_code('LUG', m.group(1))
    m = re.match(r'UG Set #(\d+)', d)
    if m:
        return norm_code('SET', m.group(1))
    if s['cat'] in ('05', '06', '18'):
        m = CODE_RE.search(d)
        if m:
            return norm_code(*m.groups())
    return None


def sheet_size(s):
    d = s['desc']
    if re.search(r'\b2 Oz\b', d, re.I):
        return '2OZ'
    if re.search(r'\b8 Oz', d, re.I):
        return '8OZ'
    if re.search(r'\bPt\b', d):
        return 'PINT'
    if re.search(r'\bGal\b', d):
        return 'GALLON'
    if '25#' in d:
        return '25LB'
    if '10#' in d or s['search'] == 'GZ DRY DL':
        return '10LB'
    if re.search(r'(?<!\d)1#', d):
        return '1LB'
    return {'PINTS': 'PINT', 'GALLON': 'GALLON', '2 OZ': '2OZ', '8 OZ': '8OZ', '10# DRY': '10LB', '25# DRY': '25LB'}.get(s['search'])


by_upc = defaultdict(list)
by_item = {}
by_code = defaultdict(list)
for s in sheet:
    s['code'] = sheet_code(s)
    s['size'] = sheet_size(s)
    by_upc[s['upc']].append(s)
    by_item[s['item']] = s
    if s['code']:
        by_code[(s['code'], s['size'])].append(s)

SIZE_MAP = {'PINT': 'PINT', '2 OZ': '2OZ', 'GALLON': 'GALLON', '10 LB PAIL': '10LB', '25 LB PAIL': '25LB',
            '8 OZ': '8OZ', '1 LB DRY': '1LB', '18 POUNDS DRY': '18LB', '5 GALLON PAIL': '5GAL'}


def shop_code_size(v):
    vt, pt = v['vtitle'], v['ptitle']
    code = size = None
    if vt != 'Default Title':
        m = re.match(r'Set (\d+)$', vt.strip())
        if m:
            return norm_code('SET', m.group(1)), None
        m = CODE_RE.search(vt)
        if m:
            code = norm_code(*m.groups())
        if '/' in vt:
            size = SIZE_MAP.get(vt.split('/')[-1].strip().upper())
        elif re.search(r'8\s?oz', vt, re.I):
            size = '8OZ'
    else:
        m = CODE_RE.search(pt)
        if m and (v['vendor'] == 'Amaco') and not re.search(r'kiln|excel', pt, re.I):
            code = norm_code(*m.groups())
    if code and not size:
        if re.search(r'gallon', pt, re.I):
            size = 'GALLON'
        elif re.search(r'10 Pound Dry', pt, re.I):
            size = '10LB'
        elif code.startswith('INK-'):
            size = '8OZ'
        elif re.search(r'\bdry\b', pt, re.I):
            size = 'DRY'   # dry product with no stated weight: don't guess
        else:
            size = 'PINT'
    return code, size


def bc12(b):
    b = re.sub(r'\D', '', b or '')
    if len(b) == 11:
        return '0' + b
    return b


def pick(cands):
    """Prefer active-tab rows when a key hits several sheet rows."""
    act = [c for c in cands if c['status'] == 'A']
    return (act or cands)


# Hand-checked matches the parser can't infer (Shopify SKU -> AMACO item #)
MANUAL = {
    'BBAB': '22119C',      # Brent BatBrace add-on  -> "Bat Brace For Batmobile"
    'AUGPBLA': '11420F',   # Underglaze Pencil Black -> "UG Pencil #1 Black"
}

shop = json.load(open(shop_path))
out = []
for v in shop:
    nvar = sum(1 for x in shop if x['pid'] == v['pid'])
    code, size = shop_code_size(v)
    hits = {}
    b = bc12(v['barcode'])
    if b and b in by_upc:
        hits['barcode'] = pick(by_upc[b])
    for fld in ('mpn_custom',):
        val = v[fld].strip().upper()
        if val in by_item:
            hits[fld] = [by_item[val]]
    if nvar == 1:
        vp = v['vp'].strip().upper()
        vp2 = vp[1:] if re.fullmatch(r'A\d{5}[A-Z]', vp) else vp
        if vp2 in by_item:
            hits['vp'] = [by_item[vp2]]
        sku = v['sku'].strip().upper()
        sku2 = sku[1:] if re.fullmatch(r'A\d{5}[A-Z]', sku) else sku
        if sku2 in by_item:
            hits['sku'] = [by_item[sku2]]
    if code and (code, size) in by_code:
        hits['code'] = pick(by_code[(code, size)])
    if v['sku'] in MANUAL:
        hits['manual'] = [by_item[MANUAL[v['sku']]]]
    bad_barcode = None
    if set(hits) == {'barcode'} and re.search(r'class pack|bundle', v['ptitle'], re.I):
        bad_barcode = hits.pop('barcode')[0]['item']
    items = {}
    for k, lst in hits.items():
        for s in lst:
            items.setdefault(s['item'], []).append(k)
    out.append(dict(v=v, code=code, size=size, nvar=nvar, bad_barcode=bad_barcode, hits={k: [s['item'] for s in lst] for k, lst in hits.items()}, items=items))

json.dump(dict(matches=out, sheet=sheet), open(os.path.join(base, 'matches.json'), 'w'))
from collections import Counter
print('variants', len(out))
print('matched (any)', sum(1 for o in out if o['items']))
print('single candidate', sum(1 for o in out if len(o['items']) == 1))
print('conflicting candidates', sum(1 for o in out if len(o['items']) > 1))
print('method counts', Counter(tuple(sorted(o['hits'])) for o in out))
