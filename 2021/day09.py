import fileinput
from collections import Counter, defaultdict, deque, namedtuple  # NOQA
from utils import Point, mul

# Read in problem input.
WIDTH = HEIGHT = 0
BOARD = {}

for y, line in enumerate(fileinput.input()):
    line = line.strip()
    for x, c in enumerate(line):
        BOARD[Point(x, y)] = int(c)
        WIDTH = x + 1

    HEIGHT = y + 1


LOW_POINTS = set()
part_1 = 0

# Solve part 1.
for y in range(HEIGHT):
    for x in range(WIDTH):
        p = Point(x, y)
        val = BOARD[p]

        for n in p.neighbours_4():
            if n in BOARD:
                if BOARD[n] <= val:
                    break
        else:
            LOW_POINTS.add(p)
            part_1 += (val + 1)

print "Part 1:", part_1


# Solve part 2.
def compute_basin_size(board, start):
    """Return the set of all explored points from a given point."""
    seen = set()

    def _dfs(node):
        val = board[node]
        seen.add(node)
        for n in node.neighbours_4():
            if n in board and n not in seen:
                if val <= board[n] and board[n] != 9:
                    _dfs(n)

    _dfs(start)
    return len(seen)

BASIN_SIZES = {}
for p in LOW_POINTS:
    BASIN_SIZES[p] = compute_basin_size(BOARD, p)

print "Part 2:", mul(sorted(BASIN_SIZES.values(), reverse=True)[:3])

