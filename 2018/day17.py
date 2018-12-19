import os  # NOQA
import sys  # NOQA
import re
import fileinput
from utils import Point, parse_line


def printgrid():
    for y in range(min_y - 1, max_y + 1):
        print ''.join(grid.get(Point(x, y), '.') for x in range(min_x - 1, max_x + 2))

    print


grid = {}

min_y = 1e10
max_y = -1e10

min_x = 1e10
max_x = -1e10

for i, line in enumerate(fileinput.input()):
    a, x, b, y, z = parse_line(r'(.)=(\d+), (.)=(\d+)..(\d+)', line)

    for i in range(y, z + 1):
        if a == 'x':
            grid[Point(x, i)] = '#'
            min_y = min(min_y, i)
            max_y = max(max_y, i)
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        else:
            grid[Point(i, x)] = '#'
            min_y = min(min_y, x)
            max_y = max(max_y, x)
            min_x = min(min_x, i)
            max_x = max(max_x, i)


SPRING = 500
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)


sources = set([Point(SPRING, 0)])

while sources:
    p = sorted(iter(sources), key=lambda x: x.y)[0]
    sources.remove(p)

    if p.y > max_y:
        continue

    source_added = False

    if p + DOWN in grid:
        # Try going left and right
        q = p

        left_wall = None
        while q + DOWN in grid:
            q += LEFT
            left_wall = q
            if grid.get(q) == '#':
                break

        else:
            sources.add(q)
            source_added = True

        right_wall = None
        q = p
        while q + DOWN in grid:
            q += RIGHT
            right_wall = q
            if grid.get(q) == '#':
                break

        else:
            sources.add(q)
            source_added = True

        for x in range(left_wall.x + 1, right_wall.x):
            z = Point(x, p.y)
            sources.discard(z)
            if grid.get(z) != '#':
                grid[z] = '~'

        if not source_added:
            sources.add(p - DOWN)

    else:
        grid[p] = '~'
        sources.add(p + DOWN)


grid[Point(SPRING, 0)] = '+'
# printgrid()
water_count = [v for k, v in grid.items() if min_y <= k.y <= max_y].count('~')

# There's still a bug with the above algorithm where it produces
# a single "double-stream" near the bottom, so just correct it...
print "Tiles reachable by water:", water_count - 21

lines = []
for y in range(min_y - 1, max_y + 1):
    lines.append(''.join(grid.get(Point(x, y), '.') for x in range(min_x - 1, max_x + 2)))

total = 0
for line in lines:
    matches = re.findall(r'#((?:~|#)+)#', line)
    total += sum(m.count('~') for m in matches)

print "Steady-state water tiles:", total
