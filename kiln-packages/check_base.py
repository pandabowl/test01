#!/usr/bin/env python3
"""
Content guard, run just before pushing one product.

Usage:
    python3 kiln-packages/check_base.py <saved nodes response JSON> <product id>

The JSON is a saved `nodes(ids:)` response with `{ ... on Product { id
descriptionHtml } }` that includes the product (repeating the id is fine; it
only makes the response big enough to be saved to a file). Prints one word:

  PUSH     the live description, with the box and text fixes applied, is
           exactly updated/<id>.html: nobody has changed the description
           text since the file was prepared, so pushing it is safe.
  DONE     the live description already matches updated/<id>.html.
  CHANGED  someone else changed the description; do not push (exit 1).

Unlike comparing updatedAt, this ignores edits to other fields (inventory,
tags, metafields, ...), which a scheduled job makes several times a day.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_package_boxes import SPEC, insert_box, render_box  # noqa: E402
from merge_live import apply_fixes  # noqa: E402
from verify_live import norm  # noqa: E402


def main():
    path, pid = sys.argv[1], sys.argv[2]
    nodes = [n for n in json.load(open(path))["data"]["nodes"]
             if n and n["id"].split("/")[-1] == pid]
    if not nodes or pid not in SPEC:
        print("CHANGED (product not found in the response)")
        sys.exit(1)
    live = nodes[0]["descriptionHtml"]
    want = norm(open(os.path.join(HERE, "updated", f"{pid}.html")).read())
    if norm(live) == want:
        print("DONE")
    elif norm(apply_fixes(pid, insert_box(live, render_box(SPEC[pid])))) == want:
        print("PUSH")
    else:
        print("CHANGED")
        sys.exit(1)


if __name__ == "__main__":
    main()
