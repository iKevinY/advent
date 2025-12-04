import fileinput
from copy import deepcopy
from utils import Point, DIRS_8


# Read problem input.
BOARD = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        BOARD[Point(x, y)] = c

# Solve problem.
TOTAL_PAPER = 0

while True:
    new_board = deepcopy(BOARD)
    removed = 0
    for p, c in BOARD.items():
        if c != '@':
            continue

        adjacent = sum(BOARD.get(p + d) == '@' for d in DIRS_8)

        if adjacent < 4:
            new_board[p] = '.'
            removed += 1

    if TOTAL_PAPER == 0:
        print("Part 1:", removed)

    TOTAL_PAPER += removed
    BOARD = new_board
    if removed == 0:
        break

print("Part 2:", TOTAL_PAPER)

