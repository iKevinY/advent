import fileinput
from collections import deque, Counter
from itertools import permutations

from utils import Point


def bfs(board, start, end):
    horizon = deque([(start, 0)])
    seen = {}
    while horizon:
        pos, dist = horizon.popleft()
        if pos in seen:
            continue

        seen[pos] = dist

        if pos == END:
            return seen

        for n in pos.neighbours():
            if BOARD.get(n) == '#' or n not in BOARD:
                continue
            horizon.append((n, dist + 1))


def num_cheat_paths(distances, max_cheat_dist):
    cheat_saves = Counter()
    for start, end in permutations(distances, 2):
        if distances[end] < distances[start]:
            continue

        cheat_dist = abs(start.dist_manhattan(end))

        if cheat_dist > max_cheat_dist:
            continue

        saved = distances[end] - distances[start] - cheat_dist
        cheat_saves[saved] += 1

    num_cheats = 0
    for cheat_dist, count in cheat_saves.items():
        if cheat_dist >= 100:
            num_cheats += count

    return num_cheats


# Read problem input.
BOARD = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        if c == '#':
            BOARD[p] = '#'
        else:
            BOARD[p] = '.'
            if c == 'S':
                START = p
            elif c == 'E':
                END = p


# Solve problem.
distances = bfs(BOARD, START, END)

print("Part 1:", num_cheat_paths(distances, 2))
print("Part 2:", num_cheat_paths(distances, 20))
