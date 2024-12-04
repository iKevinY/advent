import fileinput
from utils import Point, DIRS_8, NW, NE, SW, SE

BOARD = {}
X_LOCS = set()
A_LOCS = set()

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        BOARD[p] = c
        if c == 'X':
            X_LOCS.add(p)
        elif c == 'A':
            A_LOCS.add(p)


# Solve part 1.
part_1 = 0
for loc in X_LOCS:
    for d in DIRS_8:
        if (BOARD.get(loc + d) == 'M'
            and BOARD.get(loc + d * 2) == 'A'
            and BOARD.get(loc + d * 3) == 'S'):
            part_1 += 1

print("Part 1:", part_1)


# Solve part 2.
part_2 = 0
for loc in A_LOCS:
    diag_1 = set([BOARD.get(loc + NW), BOARD.get(loc + SE)])
    diag_2 = set([BOARD.get(loc + NE), BOARD.get(loc + SW)])

    if diag_1 == diag_2 == set(['M', 'S']):
        part_2 += 1

print("Part 2:", part_2)
