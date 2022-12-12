import fileinput
from collections import deque
from utils import Point

# Parse input.
board = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        board[Point(x, y)] = c
        if c == 'S':
            start = Point(x, y)
            board[start] = 'a'
        elif c == 'E':
            end = Point(x, y)
            board[end] = 'z'


def bfs(start):
    horizon = deque([(start, 0)])
    seen = set()
    while horizon:
        p, depth = horizon.popleft()
        if p in seen:
            continue
        elif p == end:
            return depth

        seen.add(p)

        for n in p.neighbours():  # returns the 4 adjacent points
            if n not in board:
                continue
            if (ord(board[n]) - 1 <= ord(board[p])):
                horizon.append((n, depth + 1))

    return 1e9


print("Part 1:", bfs(start))
print("Part 2:", min(bfs(s) for s in board if board[s] == 'a'))
