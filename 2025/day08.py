import fileinput
from collections import Counter

from utils import UnionFind


# Read problem input.
BOXES = []
for line in fileinput.input():
    a, b, c = [int(x) for x in line.split(',')]
    BOXES.append((a, b, c))


# Precompute pairwise distances and sort ascending.
DISTS = []
for y, (a1, b1, c1) in enumerate(BOXES):
    for x, (a2, b2, c2) in enumerate(BOXES):
        if x >= y:
            continue
        dist = (abs(a2 - a1) ** 2) + (abs(b2 - b1) ** 2) + (abs(c2 - c1) ** 2)
        DISTS.append((dist, x, y))
DISTS.sort()

# Solve problem.
TARGET_MERGES = 1000
uf = UnionFind(len(BOXES))
last_merge = None
for it, (dist, x, y) in enumerate(DISTS):
    if not uf.in_same_set(x, y):
        uf.merge(x, y)
        last_merge = (BOXES[x], BOXES[y])

    if it == TARGET_MERGES - 1:
        circuits = [uf.find(i) for i in range(len(BOXES))]
        sizes = [size for circuit, size in Counter(circuits).most_common()]
        print("Part 1:", sizes[0] * sizes[1] * sizes[2])

print("Part 2:", last_merge[0][0] * last_merge[1][0])
