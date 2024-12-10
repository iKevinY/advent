import fileinput
from collections import deque

from utils import Point


def hike(board, trailhead):
    horizon = deque([trailhead])
    seen = set()

    nines = set()
    trails = 0

    while horizon:
        curr = horizon.pop()
        if curr in seen:
            continue

        if board.get(curr) == 9:
            trails += 1
            nines.add(curr)

        for neigh in curr.neighbours():
            if board.get(neigh, 0) == board.get(curr) + 1:
                horizon.appendleft(neigh)

    return len(nines), trails


# Read problem input.
BOARD = {}
TRAILHEADS = set()

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        BOARD[p] = int(c)
        if BOARD[p] == 0:
            TRAILHEADS.add(p)


# Solve problem.
part_1 = 0
part_2 = 0
for trailhead in TRAILHEADS:
    scores, trails = hike(BOARD, trailhead)
    part_1 += scores
    part_2 += trails

print("Part 1:", part_1)
print("Part 2:", part_2)
