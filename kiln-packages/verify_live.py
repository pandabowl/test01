#!/usr/bin/env python3
"""
Check live Shopify descriptions against kiln-packages/updated/<id>.html.

Usage:
    python3 kiln-packages/verify_live.py <saved GraphQL response JSON>

The JSON is the result of
    query($ids: [ID!]!) { nodes(ids: $ids) { ... on Product { id descriptionHtml } } }

Shopify reformats descriptions when it saves them (adds line breaks between
block tags, turns named entities like &times; into the character), so both
sides are normalized before comparing: entities decoded, whitespace between
tags dropped, other runs of whitespace collapsed.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(h):
    h = html.unescape(h)
    h = re.sub(r">\s+", ">", h)
    h = re.sub(r"\s+<", "<", h)
    return re.sub(r"\s+", " ", h).strip()


def main():
    nodes = json.load(open(sys.argv[1]))["data"]["nodes"]
    bad = 0
    for n in nodes:
        pid = n["id"].split("/")[-1]
        want = norm(open(os.path.join(HERE, "updated", f"{pid}.html")).read())
        got = norm(n["descriptionHtml"])
        boxes = n["descriptionHtml"].count('class="sppk"')
        if want == got and boxes == 1:
            print(f"{pid} OK")
            continue
        bad += 1
        i = next((k for k, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
        print(f"{pid} MISMATCH boxes={boxes} len want={len(want)} got={len(got)} at {i}")
        print("   want:", want[max(0, i - 80):i + 80])
        print("   got: ", got[max(0, i - 80):i + 80])
    print(f"{len(nodes) - bad}/{len(nodes)} match")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
