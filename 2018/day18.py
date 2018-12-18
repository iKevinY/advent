import fileinput
from collections import defaultdict
from itertools import count

from utils import Point


GRID = {}

for y, line in enumerate(fileinput.input()):
    for x, t in enumerate(line.strip()):
        GRID[Point(x, y)] = t

    DIM = y + 1


seen = defaultdict(list)
resources = {}
period = None
last_period = None

for minute in count():
    tiles = GRID.values()
    trees = tiles.count('|')
    yards = tiles.count('#')

    seen[trees, yards].append(minute)
    resources[minute] = trees, yards

    if minute == 10:
        print "Resource value after 10 minutes:", trees * yards

    # Wait until we see periodic behaviour in the resource values observed
    if len(seen[trees, yards]) > 3:
        poss_period = minute - seen[trees, yards][-2]
        if poss_period == last_period:
            period = poss_period
        last_period = poss_period
    else:
        last_period = None

    if period is not None:
        if (1000000000 - minute) % period == 0:
            print "Resoruce value after 1000000000 minutes:", trees * yards
            break

    next_grid = {}

    for y in range(DIM):
        for x in range(DIM):
            p = Point(x, y)
            neighs = [GRID.get(q) for q in Point(x, y).neighbours_8()]

            if GRID.get(p) == '.':
                next_grid[p] = '|' if neighs.count('|') >= 3 else '.'
            elif GRID.get(p) == '|':
                next_grid[p] = '#' if neighs.count('#') >= 3 else '|'
            else:
                next_grid[p] = '#' if neighs.count('#') >= 1 and neighs.count('|') >= 1 else '.'

    GRID = next_grid
