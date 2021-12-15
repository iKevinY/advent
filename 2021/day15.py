import fileinput
import heapq
from utils import Point


def shortest_path(graph, start, end):
    """Returns the shortest path from start to end in graph."""
    horizon = [(0, start)]
    seen = set()

    while horizon:
        depth, node = heapq.heappop(horizon)

        if node == end:
            return depth
        elif node in seen:
            continue

        seen.add(node)

        for neigh in node.neighbours_4():
            if neigh not in graph:
                continue

            heapq.heappush(horizon, (depth + graph[neigh], neigh))

    return -1


CAVE = {}

# Read problem input and solve part 1.
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        CAVE[Point(x, y)] = int(c)
        WIDTH = x + 1

    HEIGHT = y + 1

print "Part 1:", shortest_path(CAVE, Point(0, 0), Point(x, y))


# Replicate CAVE tiles to solve part 2.
for y in range(HEIGHT*5):
    for x in range(WIDTH*5):
        if Point(x, y) not in CAVE:
            dx = x // WIDTH
            dy = y // HEIGHT

            # Need to subtract one, take modulo, then add one because we
            # are dealing with the range 1-9, not 0-8.
            val = (CAVE[Point(x % WIDTH, y % HEIGHT)] + (dx + dy))
            CAVE[Point(x, y)] = ((val - 1) % 9) + 1

print "Part 2:", shortest_path(CAVE, Point(0, 0), Point(x, y))
