"""Check that the live page renders a metafield value exactly as intended.

The collection template prints custom.abz_collection_below_descrption raw (no
filters), so after publishing, the live HTML must contain the intended value
byte for byte. Also used before publishing, to prove a backup is exact.

    curl -sS -A "Mozilla/5.0" -o live.html "https://www.sheffield-pottery.com/collections/<handle>?v=$RANDOM"
    python3 verify_live.py live.html intended_value.html

Exit code 0 = exact match. Otherwise prints the first difference.
"""
import sys

live = open(sys.argv[1], encoding='utf-8').read()
want = open(sys.argv[2], encoding='utf-8').read()
start = want[:80]
i = live.find(start)
if i < 0:
    print('start of intended value not found on the page (cached page? wrong collection?)')
    sys.exit(1)
seg = live[i:i + len(want)]
if seg == want:
    print('EXACT MATCH: live page renders the intended value')
    sys.exit(0)
for k, (x, y) in enumerate(zip(seg, want)):
    if x != y:
        print('first difference at char', k)
        print(' live:    ', repr(seg[max(0, k - 80):k + 80]))
        print(' intended:', repr(want[max(0, k - 80):k + 80]))
        break
else:
    print('live segment is shorter than intended value')
sys.exit(1)
