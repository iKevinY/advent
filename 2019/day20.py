import fileinput
from string import ascii_uppercase
from collections import defaultdict

from utils import Point


MAZE = defaultdict(lambda: '#')
PORTALS = defaultdict(set)
PORTAL_MAP = {}

AA = None
ZZ = None

INNERS = set()
OUTERS = set()

MAX_X = 0
MAX_Y = 0

# Read problem input
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line[:-1]):
        MAZE[Point(x, y)] = c
        MAX_X = max(MAX_X, x)
        MAX_Y = max(MAX_Y, y)

# Determine the true label name and grid position of portals
for p, c in MAZE.items():
    if c in ascii_uppercase:
        for np in p.neighbours_4():
            if MAZE[np] in ascii_uppercase:
                if np.x > p.x or np.y > p.y:
                    name = c + MAZE[np]
                else:
                    name = MAZE[np] + c

                break

        for pp in p.neighbours_4():
            if MAZE[pp] == '.':
                portal_loc = pp
        for pp in np.neighbours_4():
            if MAZE[pp] == '.':
                portal_loc = pp

        if name == 'AA':
            AA = portal_loc
        elif name == 'ZZ':
            ZZ = portal_loc
        else:
            PORTALS[name].add(portal_loc)

# Map portal positions and track inner/outer edges
for x in PORTALS:
    a, b = PORTALS[x]
    PORTAL_MAP[a] = b
    PORTAL_MAP[b] = a
    if a.x == 2 or a.x == (MAX_X - 2) or a.y == 2 or a.y == (MAX_Y - 2):
        OUTERS.add(a)
        INNERS.add(b)
    else:
        OUTERS.add(b)
        INNERS.add(a)


def bfs(start, end, recursive=False):
    horizon = [(start, 0)]
    seen = set()
    steps = 1

    while horizon:
        new_horizon = []
        for p, level in horizon:
            neighbours = p.neighbours_4()
            if p in PORTAL_MAP:
                if not (p in OUTERS and level == 0) or not recursive:
                    neighbours.append(PORTAL_MAP[p])

            for np in neighbours:
                new_level = level
                if recursive:
                    if p in INNERS and np in OUTERS:
                        new_level += 1
                    elif p in OUTERS and np in INNERS and level > 0:
                        new_level -= 1

                if (np, new_level) in seen:
                    continue

                if MAZE[np] != '.':
                    continue

                if np == end and new_level == 0:
                    return steps

                seen.add((np, new_level))
                new_horizon.append((np, new_level))

        horizon = new_horizon
        steps += 1


print "Steps in basic maze:", bfs(AA, ZZ)
print "Steps in recursive maze:", bfs(AA, ZZ, recursive=True)
