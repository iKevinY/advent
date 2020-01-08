import random
import fileinput
from collections import defaultdict

from utils import Point
from intcode import emulate


ROBOT_DIRS = [
    Point(1, 0),   # north
    Point(-1, 0),  # south
    Point(0, -1),  # west
    Point(0, 1),   # east
]

INVERSE_DIRS = {
    0: 1,
    1: 0,
    2: 3,
    3: 2,
}


def robot_dfs(vm, instructions, graph, curr, approach_d):
    for d in range(4):
        np = curr + ROBOT_DIRS[d]
        if np in graph:
            continue

        # Attempt to move to next tile
        instructions.append(d + 1)
        resp = next(vm)

        if resp == 0:
            BOARD[np] = 0
        else:
            if resp == 2:
                global OXYGEN
                OXYGEN = np
            BOARD[np] = resp
            robot_dfs(vm, instructions, graph, np, d)

    # Can't rely on call stack alone to backtrack
    instructions.append(INVERSE_DIRS[approach_d] + 1)
    next(vm)


def bfs(graph, start, end=None):
    seen = set()
    dist = 0
    horizon = [start]
    while horizon:
        new_horizon = []
        for p in horizon:
            for np in p.neighbours_4():
                if graph.get(np, 1) == 0:
                    continue

                if end is not None and np == end:
                    return dist + 1

                if np not in seen:
                    new_horizon.append(np)

                seen.add(np)

        horizon = new_horizon
        dist += 1

    return dist


# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]

BOARD = {}
OXYGEN = None

instructions = [0]
vm = emulate(TAPE, instructions)
robot_dfs(vm, instructions, BOARD, Point(0, 0), 0)

print "Optimal movement to oxygen:", bfs(BOARD, Point(0, 0), OXYGEN)
print "Minutes taken to fill up:", bfs(BOARD, OXYGEN) - 1
