# Python adaptation of Peter Tseng's day 22 solution
# https://www.reddit.com/r/adventofcode/comments/5jor9q/2016_day_22_solutions/dbhw73s

import re
import fileinput
from itertools import permutations
from collections import deque, namedtuple

WIDTH = None
HEIGHT = None
DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

Node = namedtuple('Point', 'x y size used available used_pcnt')


def naive_move_to_top(node, grid):
    queue = deque([(node.x, node.y)])
    dists = {(node.x, node.y): 0}

    while queue:
        x, y = queue.pop()

        if y == 0:
            return dists[x, y], x

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                continue

            if (nx, ny) in dists or grid[ny][nx].used > grid[y][x].size:
                continue

            dists[nx, ny] = dists[x, y] + 1
            queue.appendleft((nx, ny))


def sliding_tile_moves(node, grid):
    # Move the empty spot to y=0 and track x position.
    steps, x = naive_move_to_top(node, grid)

    # Move to (WIDTH - 2, 0), one to the left of the goal.
    steps += WIDTH - 2 - x

    # 1 step moves the goal data into (WIDTH - 2, 0), with empty space behind.
    steps += 1

    # 4 steps each to move the empty space from behind to in front,
    # 1 step to move the goal data
    return steps + 5 * (WIDTH - 2)


if __name__ == '__main__':
    nodes = []

    for line in fileinput.input():
        if line.startswith('/dev/grid/'):
            data = (int(x) for x in re.findall(r'(\d+)', line))
            nodes.append(Node(*data))

    WIDTH = 1 + max(node.x for node in nodes)
    HEIGHT = 1 + max(node.y for node in nodes)

    grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for node in nodes:
        grid[node.y][node.x] = node

    pairs = set()

    for a, b in permutations(nodes, 2):
        if a.used > 0 and a.used <= b.available:
            pairs.add((a, b))

    print "Viable pairs of nodes:", len(pairs)

    empties = [n for n in nodes if n.used == 0]
    fewest_steps = min(sliding_tile_moves(e, grid) for e in empties)
    print "Fewest steps to move goal data:", fewest_steps
