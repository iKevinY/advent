import fileinput
from collections import Counter

from utils import Point, DIRS_4, parse_nums


COORDS = []

for line in fileinput.input():
    x, y = parse_nums(line)
    COORDS.append((x, y))

X, Y = zip(*COORDS)

ASSIGNS = {}
REGIONS = Counter()
SAFETY = Counter()

for y in range(min(Y), max(Y)):
    for x in range(min(X), max(X)):
        p = Point(x, y)
        total_distance = 0
        to_point = {}

        for (xx, yy) in COORDS:
            q = Point(xx, yy)
            dist = p.to_manhattan(q)
            to_point[q] = dist
            total_distance += dist

        SAFETY[p] = total_distance

        dists = list(sorted(to_point.items(), key=lambda x: x[1]))
        if dists[0][1] < dists[1][1]:
            REGIONS[dists[0][0]] += 1
            ASSIGNS[p] = dists[0][0]
        else:
            ASSIGNS[p] = Point(-1, -1)

for p, n in REGIONS.most_common():
    for d in DIRS_4:
        q = p + d
        while q in ASSIGNS:
            if ASSIGNS[q] != p:
                # Not infinite
                break

            q += d
        else:
            # Confirmed infinite
            break

    else:
        # This is the largest non-infinite region
        print "Size of Part 1 region:", n
        break


print "Size of Part 2 region:", sum(n < 10000 for n in SAFETY.values())
