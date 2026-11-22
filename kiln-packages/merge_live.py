#!/usr/bin/env python3
"""
Bring live descriptions up to date without losing other people's edits.

Usage:
    python3 kiln-packages/merge_live.py <saved GraphQL response JSON>

The JSON is the same nodes(ids) response verify_live.py reads. For every
package in SPEC, starting from the LIVE description (so edits made by other
people or tools, e.g. a new banner, are kept):
  - the "What's in the package" box is put back if it is missing, or replaced
    if it is out of date with SPEC;
  - the stale-note fixes in text_fixes.py are applied.
The result is written to updated/<id>.html, ready to push, and the IDs that
changed are printed. Products that are already up to date are left alone.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_package_boxes import SPEC, insert_box, render_box  # noqa: E402
from text_fixes import TEXT_FIXES  # noqa: E402
from verify_live import norm  # noqa: E402


def apply_fixes(pid, desc):
    for old, new in TEXT_FIXES.get(pid, []):
        count = desc.count(old)
        if count > 1:
            sys.exit(f"{pid}: stale note found {count} times, expected once: {old[:60]!r}")
        desc = desc.replace(old, new)
    return desc


def main():
    nodes = json.load(open(sys.argv[1]))["data"]["nodes"]
    changed = []
    for n in nodes:
        pid = n["id"].split("/")[-1]
        if pid not in SPEC:
            continue
        live = n["descriptionHtml"]
        merged = apply_fixes(pid, insert_box(live, render_box(SPEC[pid])))
        if merged.count('class="sppk"') != 1:
            sys.exit(f"{pid}: expected exactly one box after merging")
        if norm(merged) == norm(live):
            continue
        open(os.path.join(HERE, "updated", f"{pid}.html"), "w").write(merged)
        changed.append(pid)
    print("\n".join(changed) if changed else "nothing to merge")


if __name__ == "__main__":
    main()
