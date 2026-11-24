"""Turn matches.json into per-variant action rows (GTIN, MPN, price).

usage: python3 -I plan.py <work_dir>   -> writes <dir>/plan.json
"""
import json, os, re, sys
from collections import Counter, defaultdict

base = sys.argv[1]
d = json.load(open(os.path.join(base, 'matches.json')))
S = {s['item']: s for s in d['sheet']}
JUNK_MPN = {'TEST1', 'TEST2', '123456'}


def bc12(b):
    b = re.sub(r'\D', '', b or '')
    return '0' + b if len(b) == 11 else b


def money(x):
    return round(float(x), 2) if x not in (None, '') else None


rows = []
item_users = defaultdict(list)
for o in d['matches']:
    v = o['v']
    item = list(o['items'])[0] if o['items'] else None
    s = S.get(item)
    if item:
        item_users[item].append(v)
    r = dict(
        pid=v['pid'], vid=v['vid'], product=v['ptitle'], variant=v['vtitle'], status=v['status'], vendor=v['vendor'],
        sku=v['sku'], price=money(v['price']), cap=money(v['cap']), barcode=v['barcode'],
        mpn_custom=v['mpn_custom'], mpn_google=v['mpn_google'], vp=v['vp'],
        match_how=', '.join(sorted(o['hits'])) if o['hits'] else '', bad_barcode=o['bad_barcode'],
        item=item, upc=s['upc'] if s else None, amaco_status=s['status'] if s else None,
        amaco_desc=s['desc'] if s else None, amaco_group=s['group'] if s else None, amaco_cat=s['catdesc'] if s else None,
        p26=s['p26'] if s else None, p27=s['p27'] if s else None, ssu=s['ssu'] if s else None)
    # ---- GTIN
    cur = re.sub(r'\D', '', v['barcode'] or '')
    if not s:
        r['gtin_action'] = 'REVIEW: barcode belongs to another AMACO item' if o['bad_barcode'] else ''
        r['gtin_new'] = ''
    elif not cur:
        r['gtin_action'], r['gtin_new'] = 'ADD', s['upc']
    elif cur == s['upc']:
        r['gtin_action'], r['gtin_new'] = 'OK', ''
    elif bc12(cur) == s['upc']:
        r['gtin_action'], r['gtin_new'] = 'FIX: restore leading zero', s['upc']
    else:
        r['gtin_action'], r['gtin_new'] = 'REVIEW: barcode differs from AMACO', s['upc']
    # ---- MPN (variant level)
    if not s:
        r['mpn_action'], r['mpn_new'] = '', ''
    else:
        have = {x.strip().upper() for x in (v['mpn_custom'], v['mpn_google']) if x.strip()}
        if have == {item}:
            r['mpn_action'], r['mpn_new'] = 'OK', ''
        elif have & JUNK_MPN:
            r['mpn_action'], r['mpn_new'] = 'FIX: replace test value', item
        elif have and item not in have:
            r['mpn_action'], r['mpn_new'] = 'REVIEW: different MPN on file', item
        else:
            r['mpn_action'], r['mpn_new'] = 'ADD', item
    # ---- price
    wheel = bool(s and s['group'] == 'Wheels') or bool(re.search(r'pottery wheel|wheel adaptive|model (b|c|cxc|16)\b', v['ptitle'], re.I) and v['vendor'] == 'Brent')
    r['is_wheel'] = wheel
    r['price_action'] = r['price_new'] = r['cap_new'] = r['price_note'] = ''
    if s and s['p27'] is not None:
        p, c, p26, p27 = r['price'], r['cap'], s['p26'], s['p27']
        if wheel:
            r['price_action'] = 'SKIP: Brent wheel (on hold)'
        elif p == p27 and (c is None or c in (p27,) or c != p26):
            r['price_action'] = 'NO CHANGE: already at 2027 list'
        elif p == p26 and p27 != p26:
            r['price_action'], r['price_new'] = 'UPDATE: 2026 list -> 2027 list', p27
        elif p == p26 and p27 == p26:
            r['price_action'] = 'NO CHANGE: list price unchanged'
        else:
            if p27 == p26:
                r['price_action'] = 'NO CHANGE: list unchanged (our price differs from list)'
            else:
                r['price_action'] = 'REVIEW: our price differs from 2026 list'
                r['price_note'] = f'same % change -> {round(p * p27 / p26, 2):.2f}' if p26 else ''
        if c is not None and c == p26 and p27 != p26 and not wheel:
            r['cap_new'] = p27
            if not r['price_action'].startswith('UPDATE'):
                r['price_note'] = (r['price_note'] + '; ' if r['price_note'] else '') + 'compare-at = 2026 list -> raise to 2027 list'
    rows.append(r)

# flag variants that share an AMACO item
for r in rows:
    users = item_users.get(r['item'], [])
    others = [u for u in users if u['vid'] != r['vid']]
    r['shared_with'] = '; '.join(f"{u['ptitle'][:40]} / {u['vtitle'][:25]} ({u['status']})" for u in others)

    # one AMACO item listed twice: put the GTIN on the ACTIVE listing only
    if r['status'] != 'ACTIVE' and any(u['status'] == 'ACTIVE' for u in others) and r['gtin_action'] in ('ADD', 'FIX: restore leading zero'):
        r['gtin_action'] = 'HOLD: same item as an active listing'
        r['gtin_new'] = ''

json.dump(rows, open(os.path.join(base, 'plan.json'), 'w'), indent=0)

live = lambda r: r['status'] in ('ACTIVE', 'UNLISTED')
print('variants', len(rows), 'matched', sum(1 for r in rows if r['item']))
print('GTIN', Counter(r['gtin_action'] for r in rows if r['item'] or r['gtin_action']))
print('GTIN live', Counter(r['gtin_action'] for r in rows if live(r) and (r['item'] or r['gtin_action'])))
print('MPN', Counter(r['mpn_action'] for r in rows if r['item']))
print('MPN live', Counter(r['mpn_action'] for r in rows if r['item'] and live(r)))
print('PRICE live+draft', Counter(r['price_action'] for r in rows if r['item'] and r['status'] != 'ARCHIVED'))
print('cap updates', sum(1 for r in rows if r['cap_new'] != ''))
print('amaco status of live matched', Counter(r['amaco_status'] for r in rows if r['item'] and live(r)))
print('live unmatched', sum(1 for r in rows if not r['item'] and live(r)))
