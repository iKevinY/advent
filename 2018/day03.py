import fileinput
from collections import Counter, defaultdict

from utils import parse_line

SQUARES = Counter()
CLAIMS = defaultdict(list)

for i, line in enumerate(fileinput.input()):
    _id, x, y, w, h = parse_line(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)

    for i in range(x, x + w):
        for j in range(y, y + h):
            SQUARES[(i, j)] += 1
            CLAIMS[_id].append((i, j))

print "Square inches of fabric within multiple claims:", sum(n > 1 for c, n in SQUARES.items())

for _id in CLAIMS:
    for pos in CLAIMS[_id]:
        if SQUARES[pos] != 1:
            break
    else:
        print "ID of only non-overlapping claim:", _id
