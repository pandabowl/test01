"""Print a value as a JSON string ready to paste into a GraphQL `variables` object.

Shopify values often contain invisible characters (no-break spaces U+00A0,
variation selectors U+FE0E/U+FE0F after ☎ or ⚠, zero-width spaces). Typed by
hand they silently turn into ordinary characters and the live page no longer
matches byte for byte. This prints the JSON string with every such character
written as an explicit \\uXXXX escape and lists which ones it found.

    python3 tools/escape_value.py new_value.html > new_value.esc.txt
"""
import json
import sys
import unicodedata

INVISIBLE = ('Cf', 'Mn', 'Me', 'Zs', 'Zl', 'Zp', 'Cc', 'Co', 'Cn')


def escape(value):
    out = []
    for ch in json.dumps(value, ensure_ascii=False):
        if ord(ch) > 127 and unicodedata.category(ch) in INVISIBLE:
            out.append('\\u%04x' % ord(ch))
        else:
            out.append(ch)
    s = ''.join(out)
    assert json.loads(s) == value
    return s


if __name__ == '__main__':
    v = open(sys.argv[1], encoding='utf-8', newline='').read()
    found = sorted({'U+%04X' % ord(c) for c in v if ord(c) > 127 and unicodedata.category(c) in INVISIBLE})
    print(escape(v))
    print('invisible characters escaped:', ', '.join(found) or 'none', file=sys.stderr)
