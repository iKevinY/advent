import fileinput
from utils import Point, N, S, E, W


DIRS = [S, E, N, W]

def simulate(board, start, obs=None):
    BOARD[obs] = '#'
    p = start
    d = 0
    seen = set()

    while True:
        if (p, d) in seen:
            # Loop detected.
            BOARD[obs] = '.'
            return None

        seen.add((p, d))

        np = p + DIRS[d]
        if BOARD.get(np) == '#':
            d = (d + 1) % 4
        elif BOARD.get(np) is None:
            break
        else:
            p += DIRS[d]

    BOARD[obs] = '.'
    return set(p for p, _ in seen)

# Read problem input.
BOARD = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        BOARD[p] = c
        if c == '^':
            START = p

# Solve part 1.
seen = simulate(BOARD, START)
print("Part 1:", len(seen))

# Solve part 2.
candidates = set()
for x in seen:
    for n in x.neighbours():
        candidates.add(n)

part_2 = 0
for p in candidates:
    if p not in seen or BOARD.get(p) != '.':
        continue
    if simulate(BOARD, START, obs=p) is None:
        part_2 += 1

print("Part 2:", part_2)

