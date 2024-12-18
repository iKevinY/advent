import fileinput
from collections import deque

from utils import Point, parse_nums


def bfs(size, corruptions, time, start, end):
    horizon = deque([(start, 0)])
    seen = set()
    while horizon:
        pos, dist = horizon.popleft()
        if pos in seen:
            continue

        seen.add(pos)

        if pos == END:
            return dist

        for n in pos.neighbours():
            is_corrupted = corruptions.get(n, 1e6)
            if is_corrupted < time:
                continue

            if 0 <= n.x <= size and 0 <= n.y <= size:
                horizon.append((n, dist + 1))


SIZE = 70

# Read problem input.
BYTES = []
CORRUPTIONS = {}
for i, line in enumerate(fileinput.input()):
    BYTES.append(line)
    x, y = parse_nums(line)
    CORRUPTIONS[Point(x, y)] = i

START = Point(0, 0)
END = Point(SIZE, SIZE)

# Solve problem.
for i in range(len(BYTES)):
    dist = bfs(SIZE, CORRUPTIONS, i, Point(0, 0), Point(SIZE, SIZE))
    if i == 1024:
        print("Part 1:", dist)
    if dist is None:
        print("Part 2:", BYTES[i-1])
        break
