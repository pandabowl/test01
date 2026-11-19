"""Replace the old Skutt lift-gate JPG in product descriptions with the HTML offer box.

Usage: python3 -I scripts/replace_liftgate_graphic.py targets.json out_dir

targets.json is a list of {"id", "handle", "title", "body_html"} (e.g. from the
storefront /products/<handle>.json). Originals of the updated products are kept
in backups/ so the change can be reverted.

Writes out_dir/new/<id>.html, out_dir/report.json, and out_dir/bulk.jsonl
(one {"input": {"id", "descriptionHtml"}} line per product for a bulk productUpdate).
"""
import json
import os
import re
import sys

BOX_INNER = (
    '<span style="display:block;box-sizing:border-box;background:#ffffff;border:1px solid #e6ddd6;'
    'border-top:6px solid #d93b22;border-radius:12px;padding:20px 16px;'
    'padding:clamp(14px,4.5cqi,30px) clamp(12px,4.5cqi,30px);text-align:center;line-height:1.15;'
    'font-family:Arial,Helvetica,sans-serif;font-weight:400;font-style:normal;letter-spacing:normal;'
    'text-transform:none;text-decoration:none;color:#2b2b2b;">'
    '<img src="https://cdn.shopify.com/s/files/1/0677/5508/2050/files/logo.png?v=1679391841" '
    'alt="Sheffield Pottery" width="384" height="67" '
    'style="display:block;width:68%;max-width:384px;height:auto;margin:0 auto;border:0;"> '
    '<span style="display:block;margin:0.55em 0 0.2em;padding:0;'
    "font-family:'Trebuchet MS','Segoe UI',system-ui,-apple-system,Roboto,Arial,sans-serif;"
    'font-weight:400;font-style:normal;font-size:20px;font-size:clamp(15px,5.2cqi,33px);line-height:1.15;'
    'letter-spacing:0.01em;text-transform:none;color:#c23a2b;">Special Offer!</span> '
    '<span style="display:block;margin:0;padding:0;'
    "font-family:'Arial Black',Gadget,system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;"
    'font-weight:900;font-style:normal;font-size:22px;font-size:clamp(15px,6cqi,39px);line-height:1.12;'
    'letter-spacing:0;text-transform:uppercase;color:#d93b22;-webkit-text-stroke:0.045em #4a1e16;'
    'paint-order:stroke fill;text-shadow:0.04em 0.05em 0 rgba(0,0,0,0.22);">'
    'Free <span style="white-space:nowrap;">Lift-Gate</span> Service<br> on All Skutt Kilns!</span> '
    '<img src="https://cdn.shopify.com/s/files/1/0677/5508/2050/files/skutt-kilns-web-logo.jpg?v=1680243671" '
    'alt="Skutt Kilns" width="207" height="273" '
    'style="display:block;width:18%;min-width:66px;max-width:108px;height:auto;margin:0.9em auto 0;'
    'border:0;mix-blend-mode:multiply;">'
    '</span>'
)

OUTER_STYLE = (
    'display:block;container-type:inline-size;width:100%;max-width:560px;margin:12px auto 20px;'
    'padding:0;box-sizing:border-box;border:0;background:none;text-decoration:none;color:#2b2b2b;'
)


def box(href=None):
    if href:
        return f'<a href="{href}" style="{OUTER_STYLE}">{BOX_INNER}</a>'
    return f'<span style="{OUTER_STYLE}">{BOX_INNER}</span>'


IMG = r'<img\b[^>]*skutt-kilns-sale-free-lift-gate[^>]*>'
LINKED = re.compile(r'<a\s+href="([^"]*)"\s*>\s*(' + IMG + r')\s*</a>', re.I)
BARE = re.compile(IMG, re.I)
TOKEN = '\x00BOX\x00'


def transform(html):
    """Return (new_html, case) or raise if the graphic isn't found exactly once."""
    if len(BARE.findall(html)) != 1:
        raise ValueError('expected exactly one graphic')
    m = LINKED.search(html)
    if m:
        href = m.group(1)
        if href.endswith('/Skutt-Kilns-s/861.htm'):  # old-site URL; 301s to the collection
            href = '/collections/skutt-kilns'
        html = html[:m.start()] + TOKEN + html[m.end():]
        case = 'linked'
    else:
        href = None
        html = BARE.sub(TOKEN, html, count=1)
        case = 'unlinked'

    # Never leave the box inside a heading: drop a heading that held only the graphic,
    # otherwise move the box to just before the heading.
    h_empty = re.compile(r'<(h[1-6])\b[^>]*>\s*' + re.escape(TOKEN) + r'(?:\s*<br\s*/?>)*\s*</\1>', re.I)
    h_lead = re.compile(r'(<(h[1-6])\b[^>]*>)\s*' + re.escape(TOKEN) + r'(?:\s*<br\s*/?>)?', re.I)
    if h_empty.search(html):
        html = h_empty.sub(TOKEN, html, count=1)
        case += '+heading-removed'
    elif h_lead.search(html):
        html = h_lead.sub(lambda mm: TOKEN + mm.group(1), html, count=1)
        case += '+moved-before-heading'

    assert html.count(TOKEN) == 1
    return html.replace(TOKEN, box(href)), case


def main():
    targets = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(os.path.join(out, 'new'), exist_ok=True)
    report = []
    with open(os.path.join(out, 'bulk.jsonl'), 'w') as bulk:
        for p in targets:
            new, case = transform(p['body_html'])
            assert not BARE.search(new)
            with open(os.path.join(out, 'new', f"{p['id']}.html"), 'w') as f:
                f.write(new)
            bulk.write(json.dumps({'product': {'id': f"gid://shopify/Product/{p['id']}",
                                             'descriptionHtml': new}}, ensure_ascii=False) + '\n')
            report.append({'id': p['id'], 'handle': p['handle'], 'title': p['title'], 'case': case,
                           'old_len': len(p['body_html']), 'new_len': len(new)})
    json.dump(report, open(os.path.join(out, 'report.json'), 'w'), indent=1)
    from collections import Counter
    print(Counter(r['case'] for r in report))


if __name__ == '__main__':
    main()
