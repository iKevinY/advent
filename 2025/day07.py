import fileinput
from functools import cache

def bfs(start):
    """Returns the number of splits from `start`."""
    splits = 0
    horizon = [start]
    seen = set()
    while horizon:
        p = horizon.pop()
        if p in seen:
            continue
        if p not in BOARD:
            continue

        seen.add(p)
        x, y = p

        if BOARD[p] == '^':
            splits += 1
            horizon.append((x - 1, y))
            horizon.append((x + 1, y))
        else:
            horizon.append((x, y + 1))

    return splits


@cache
def dp(pos):
    """Returns the number of ways a tachyon travels from x, y"""
    x, y = pos
    if pos not in BOARD:
        return 1

    if BOARD[pos] == '^':
        return dp((x - 1, y)) + dp((x + 1, y))

    return dp((x, y + 1))


# Parse problem input.
BOARD = {}
START = None
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        BOARD[x, y] = c
        if c == 'S':
            START = (x, y)


# Solve problem.
print("Part 1:", bfs(START))
print("Part 2:", dp(START))
