#!/usr/bin/env python3
"""
Put the "What's in the package" box back into live descriptions that lost it.

Usage:
    python3 kiln-packages/merge_live.py <saved GraphQL response JSON>

The JSON is the same nodes(ids) response verify_live.py reads. For every
package in SPEC whose live description has no box (or an out-of-date one),
the box is inserted into the LIVE description -- so edits other people or
tools made since our push (e.g. a new banner) are kept -- and the result is
written to updated/<id>.html, ready to push. Products that already match are
left alone. Prints the IDs it rewrote.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_package_boxes import SPEC, insert_box, render_box  # noqa: E402
from verify_live import norm  # noqa: E402


def main():
    nodes = json.load(open(sys.argv[1]))["data"]["nodes"]
    changed = []
    for n in nodes:
        pid = n["id"].split("/")[-1]
        if pid not in SPEC:
            continue
        path = os.path.join(HERE, "updated", f"{pid}.html")
        live = n["descriptionHtml"]
        if norm(live) == norm(open(path).read()):
            continue
        merged = insert_box(live, render_box(SPEC[pid]))
        if norm(merged) == norm(live):
            continue
        open(path, "w").write(merged)
        changed.append(pid)
    print("\n".join(changed) if changed else "nothing to merge")


if __name__ == "__main__":
    main()
