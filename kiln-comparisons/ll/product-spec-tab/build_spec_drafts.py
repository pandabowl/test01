"""Build proposed description + custom.specifications values for the L&L spec-tab move.
Reads before/<handle>.description.html, before/<handle>.specifications.html and
kiln_only_specs.json; writes drafts/<handle>.description.html and drafts/<handle>.specifications.html.
Nothing is sent to Shopify."""
import json, os, re, sys
D = sys.argv[1]
os.makedirs(f'{D}/drafts', exist_ok=True)
rd = lambda p: open(p, encoding='utf-8').read()
ko = {p['handle']: (p['specs'] or {}).get('value') or '' for p in json.load(open(f'{D}/kiln_only_specs.json'))['data']['products']['nodes']}
META = '<p><meta charset="UTF-8"> <meta content="width=device-width, initial-scale=1.0" name="viewport"></p>\n'

def cut_container_section(desc):
    """Remove META + unscoped <style> + <div class="container">...</table>\n</div>\n</div>. Returns (new_desc, removed, table_html)."""
    ms = list(re.finditer(r'<p><meta charset="UTF-8">\s*<meta [^>]*name="viewport"[^>]*></p>\n', desc))
    assert len(ms) == 1, len(ms)
    a, st = ms[0].start(), ms[0].end()
    assert desc.startswith('<style>', st)
    c = desc.index('<div class="container">', st)
    assert desc.count('<div class="container">') == 1
    t0 = desc.index('<table', c); t1 = desc.index('</table>', t0) + len('</table>')
    end_marker = '</table>\n</div>\n</div>'
    assert desc[t1 - len('</table>'):].startswith(end_marker)
    b = t1 - len('</table>') + len(end_marker)
    return desc[:a] + desc[b:], desc[a:b], desc[t0:t1]

def wrap_like_existing(template_spec, table_html):
    """Put table_html into the standard L&L spec-tab wrapper (CSS + container) taken from an existing spec field."""
    i = template_spec.index('<table'); j = template_spec.rindex('</table>') + len('</table>')
    return template_spec[:i] + table_html + template_spec[j:]

pairs = {
 'l-l-e18m-3-easy-fire-kiln-package-lke18m3-cm':'l-l-e18m-3-easy-fire-kiln-e18m3',
 'l-l-e18s-3-easy-fire-kiln-special-package-lke18s3-cm':None,
 'l-l-e18t3-easy-fire-kiln-special-package-lke18t3-cm':'l-l-e18t3-easy-fire-kiln-special-package-lke18t3',
 'l-l-e23m-3-easy-fire-kiln-package-lke23m3-cm':'l-l-e23m-3-easy-fire-kiln-lke23m3',
 'l-l-e23s-3-easy-fire-kiln-package-lke23s3-cm':'l-l-e23s-3-3-brick-easy-fire-kiln-lke23s3',
 'l-l-e23t-3-easy-fire-kiln-special-package-lke23t3-cm':'l-l-e23t-3-3-brick-easy-fire-kiln-lke23t3',
 'l-l-e28m-easy-fire-kiln-package-lke28m-cm':'l-l-e28m-easy-fire-kiln-lke28m',
 'l-l-e28s-easy-fire-kiln-package-lke28s-cm':'l-l-e28s-easy-fire-kiln-lke28s',
 'l-l-e28t-easy-fire-kiln-package-lke28t-cm':'l-l-e28t-easy-fire-kiln-lke28t',
 'l-l-eq2827-3-equad-pro-commercial-kiln-package-lkeq282732083p':'l-l-eq2827-3-equad-pro-commercial-kiln-package',
}
e23t_spec = rd(f'{D}/before/l-l-e23t-3-3-brick-easy-fire-kiln-lke23t3.specifications.html')
ko['l-l-e23t-3-3-brick-easy-fire-kiln-lke23t3'] = e23t_spec
report = []
for pkg, kiln in pairs.items():
    desc = rd(f'{D}/before/{pkg}.description.html')
    new_desc, removed, table = cut_container_section(desc)
    table = table.replace('<thead>\n<tr></tr>\n</thead>\n', '')   # drop the empty header row group
    if kiln:   # same rows as the kiln-only product: reuse its spec tab exactly
        spec = ko[kiln]
    else:      # e18S-3: package table is the more complete one; move it as-is into the standard wrapper
        spec = wrap_like_existing(e23t_spec, table.replace(' border="1"', '').replace(' summary=""', ''))
    open(f'{D}/drafts/{pkg}.description.html', 'w', encoding='utf-8').write(new_desc)
    open(f'{D}/drafts/{pkg}.specifications.html', 'w', encoding='utf-8').write(spec)
    report.append((pkg, len(desc), len(new_desc), len(removed), 'copy of ' + kiln if kiln else 'own table, standard wrapper'))

# A1: e23S-JH -- electrical table in the description == spec field: remove it from the description, spec field unchanged.
h = 'l-l-cone-12-kiln-e23s-jh-for-crystalline-glaze-lke23sjh'
desc = rd(f'{D}/before/{h}.description.html')
new_desc, removed, _ = cut_container_section(desc)
open(f'{D}/drafts/{h}.description.html', 'w', encoding='utf-8').write(new_desc)
open(f'{D}/drafts/{h}.specifications.html', 'w', encoding='utf-8').write(rd(f'{D}/before/{h}.specifications.html'))
report.append((h, len(desc), len(new_desc), len(removed), 'spec field unchanged; JH series table left in description pending owner'))

# A2: e23T-3 kiln -- move the "Specifications" key/value table into the spec field, above the electrical table.
h = 'l-l-e23t-3-3-brick-easy-fire-kiln-lke23t3'
desc = rd(f'{D}/before/{h}.description.html')
m = re.search(r'<h2 class="abz-seo-product">Specifications</h2>\n<div class="responsive-table">\n(<table>.*?</table>)\n</div>\n', desc, re.S)
assert m and desc.count('<h2 class="abz-seo-product">Specifications</h2>') == 1
kv = m.group(1).replace('<table>', '<table class="sp-kv-specs">', 1)
new_desc = desc[:m.start()] + desc[m.end():]
spec = e23t_spec
css = ('\n        #custom-specifications-section table.sp-kv-specs { min-width: 0; }\n'
       '        #custom-specifications-section table.sp-kv-specs td { white-space: normal; }\n'
       '        #custom-specifications-section table.sp-kv-specs td:first-child { width: 34%; }\n    ')
k = spec.index('</style>'); spec = spec[:k].rstrip(' ') + css + spec[k:]
first_title = '<div class="section-title">Specifications</div>'
assert spec.count(first_title) == 1
spec = spec.replace(first_title,
    first_title + '\n        <div class="table-wrapper">\n' + kv + '\n        </div>\n'
    '        <div class="section-title">Electrical specifications</div>', 1)
open(f'{D}/drafts/{h}.description.html', 'w', encoding='utf-8').write(new_desc)
open(f'{D}/drafts/{h}.specifications.html', 'w', encoding='utf-8').write(spec)
report.append((h, len(desc), len(new_desc), len(desc) - len(new_desc), 'spec field: + kiln specs table above electrical'))
for r in report: print(f'{r[0][:58]:58} desc {r[1]:6} -> {r[2]:6} (removed {r[3]:5}) | {r[4]}')
