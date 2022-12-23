import fileinput
from collections import defaultdict

from utils import Point, N, NE, E, SE, S, SW, W, NW, min_max_xy


BOARD = {}

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        BOARD[Point(x, y)] = c

# N and S are switched from the problem statement because of
# the convention of using +y -> N in my utils, which does have
# an effect on the interaction between elves in this problem.
CHECKS = [
    [[S, SE, SW], S],
    [[N, NE, NW], N],
    [[W, NW, SW], W],
    [[E, NE, SE], E],
]

for i in range(100000):
    proposal = defaultdict(list)
    for p, c in BOARD.items():
        if c == '#':
            # If elf has no neighbours in all 8 directions, don't consider moving.
            if not any(BOARD.get(n) == '#' for n in p.neighbours_8()):
                continue
            
            # Add elf's proposed location to `proposal`.
            for d in range(4):
                checks, move = CHECKS[(i + d) % 4]
                if any(BOARD.get(p + c, ' ') == '#' for c in checks):
                    continue

                proposal[p + move].append(p)
                break

    for new_loc in proposal:
        elves = proposal[new_loc]
        # If only one elf wants to move there, they can move (and vacate their old spot).
        if len(elves) == 1:
            BOARD[elves[0]] = '.'
            BOARD[new_loc] = '#'

    # Answer to part 1, compute number of empty squares within the bounds.
    if i == 9:
        elves = [p for p in BOARD if BOARD[p] == '#']
        min_x, max_x, min_y, max_y = min_max_xy(elves)
        blanks = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                p = Point(x, y)
                if BOARD.get(p) != '#':
                    blanks += 1

        print("Part 1:", blanks)

    # Empty proposal list -> no elves moved, the answer to part 2.
    if len(proposal) == 0:
        print("Part 2:", i + 1)
        break
