import heapq
import fileinput
from collections import defaultdict

from utils import Point, DIRS, E


# Read problem input.
BOARD = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        BOARD[p] = '#' if c == '#' else '.'
        if c == 'S':
            START = p
        elif c == 'E':
            END = p


# Best-first search around the maze.
horizon = [(0, START, E, [])]
seen = {}

best_score = 1e9
best_paths = defaultdict(list)

while horizon:
    score, pos, d, path = heapq.heappop(horizon)

    if seen.get((pos, d), 1e9) < score:
        continue

    if pos == END:
        best_score = min(best_score, score)
        best_paths[score].append(path + [pos])

    seen[pos, d] = score

    for dd in DIRS:
        np = pos + dd
        if dd == -d:
            continue

        if dd == d and BOARD.get(np) == '.':
            heapq.heappush(horizon, (score + 1, np, dd, [pos] + path))
        elif BOARD.get(np) == '.':
            heapq.heappush(horizon, (score + 1001, np, dd, [pos] + path))

nice_tiles = set()
for path in best_paths[best_score]:
    nice_tiles |= set(path)

print("Part 1:", best_score)
print("Part 2:", len(nice_tiles))

