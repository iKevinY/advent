import fileinput
from string import ascii_uppercase, ascii_lowercase
from collections import defaultdict, deque
from heapq import heappush, heappop

from utils import Point


BOARD = defaultdict(lambda: '#')
KEYS = {}
DOORS = {}

ent = None

for i, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        BOARD[Point(x, i)] = c
        if c == '@':
            ent = Point(x, i)

        if c in ascii_lowercase:
            KEYS[c] = Point(x, i)

        if c in ascii_uppercase:
            DOORS[c] = Point(x, i)

NUM_KEYS = len(KEYS)


def part_1(start):
    horizon = [(start, frozenset())]
    seen = set()

    level = 0
    while horizon:
        new_horizon = []

        for p, k in horizon:
            for np in p.neighbours_4():
                if (np, k) in seen:
                    continue

                if BOARD[np] != '#':
                    c = BOARD[np]

                    if c in DOORS and c.lower() not in k:
                        continue

                    if c in KEYS:
                        if c in k:
                            state = (np, k)
                        else:
                            state = (np, k | set([c]))
                        # print state

                        if len(state[1]) == NUM_KEYS:
                            return level + 1

                        new_horizon.append(state)
                        seen.add(state)
                    else:
                        new_horizon.append((np, k))
                        seen.add((np, k))

            # print "yes"

        horizon = new_horizon
        level += 1

print "Minimal steps for Part 1:", part_1(ent)

# Manual maze replacement for Part 2
ents = []

for np in ent.neighbours_8():
    if np.dist_manhattan(ent) == 2:
        ents.append(np)
        BOARD[np] = '@'
    else:
        BOARD[np] = '#'

BOARD[ent] = '#'

points = KEYS
for i, ent in enumerate(ents):
    points[str(i)] = ent
# print points

# Preprocess graph to determine distances from each key to each other key
# Edges are represented as start_pos: (steps, new_key, doors_passed).
graph = defaultdict(list)

for i, node in enumerate(points):
    # BFS from start pos to each key in quadrant
    # state is (pos, doors_passed)
    level = 1
    horizon = [(points[node], frozenset())]
    seen = set()
    while horizon:
        new_horizon = []
        for pos, doors in horizon:
            for np in pos.neighbours_4():
                if (np, doors) in seen:
                    continue

                if BOARD[np] == '#':
                    continue

                tile = BOARD[np]
                ndoors = doors
                if tile in ascii_uppercase:
                    ndoors |= set([tile.lower()])

                if tile in ascii_lowercase and tile != node:
                    graph[node].append((level, tile, ndoors))
                    seen.add((np, ndoors))
                    continue

                new_horizon.append((np, ndoors))
                seen.add((np, ndoors))

        horizon = new_horizon
        level += 1

heap = [(0, '0', '1', '2', '3', frozenset())]
seen = set()

while heap:
    steps, a, b, c, d, keys = heappop(heap)

    if len(keys) == NUM_KEYS:
        print "Minimal steps for Part 2:", steps
        break

    for i, p in enumerate((a, b, c, d), start=1):
        for ns, np, nd in graph[p]:
            if not keys.issuperset(nd):
                continue

            next_state = [steps + ns, a, b, c, d, keys | set([np])]

            next_state[i] = np
            next_state = tuple(next_state)
            if next_state[1:] in seen:
                continue

            seen.add(next_state[1:])
            heappush(heap, next_state)
