"""Summarize kiln specs from a saved Shopify GraphQL result.

Run the collection query in PLAYBOOK.md (step 2). Its output is usually too big
to show inline, so the tool saves it to a file; pass that file here:

    python3 parse_specs.py <saved-graphql-result.json> [--all]

Prints one block per ACTIVE product: title, handle, price, finder.* facts,
custom.kiln_* fields, and the rows of the custom.specifications spec table and
capacity table. Packages and touchscreen (KMT-style) duplicates are hidden
unless --all is given. Treat these numbers as leads only: the store's spec
tables have known copy/paste errors. Fact-check every number against the
manufacturer before it goes on the site.
"""
import html
import json
import re
import sys


def cells(fragment):
    return [html.unescape(re.sub(r'<[^>]+>', '', c)).strip()
            for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', fragment, re.S)]


def tables(spec_html):
    out = {}
    for cls in ('ceramic-specs', 'capacity'):
        m = re.search(r'<table class="%s">(.*?)</table>' % cls, spec_html, re.S)
        if m:
            out[cls] = [cells(tr) for tr in re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S)]
    # Some brands may use other table classes; fall back to every table.
    if not out:
        for i, t in enumerate(re.findall(r'<table[^>]*>(.*?)</table>', spec_html, re.S)):
            out[f'table{i}'] = [cells(tr) for tr in re.findall(r'<tr>(.*?)</tr>', t, re.S)]
    return out


def main():
    path = sys.argv[1]
    show_all = '--all' in sys.argv
    data = json.load(open(path))
    node = data['data']
    # Accept either {collection:{products:{nodes}}} or {products:{nodes}}.
    products = (node.get('collection') or node)['products']['nodes']
    for p in products:
        if p.get('status') != 'ACTIVE':
            continue
        t = p['title']
        if not show_all and ('Package' in t or re.search(r'\bKMT', t)):
            continue
        g = lambda k: (p.get(k) or {}).get('value')
        price = p.get('priceRangeV2', {}).get('minVariantPrice', {}).get('amount')
        print('##', t, '|', p['handle'], '| $' + str(price), '' if p.get('onlineStoreUrl') else '| NOT ON ONLINE STORE')
        print('   finder:', g('eyebrow'), '/', g('facts'), '/', g('note'))
        print('   kiln_*: cone', g('cone'), '| power', g('power'), '| size', g('size'), '| box', g('box'))
        for name, rows in tables(g('specs') or '').items():
            for r in rows:
                print(f'   {name}:', r)


if __name__ == '__main__':
    main()
