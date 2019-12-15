import random
import fileinput
from collections import defaultdict

from utils import Point
from intcode import emulate


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
TAPE += [0] * 100000

GLOBAL_INPUTS = [0]
BOARD = {}
OXYGEN = None

ROBOT_DIRS = [
    Point(1, 0),   # north
    Point(-1, 0),  # south
    Point(0, -1),  # west
    Point(0, 1),   # east
]


# Build up board state by exploration
vm = emulate(TAPE, 0, GLOBAL_INPUTS)

try:
    curr = Point(0, 0)
    for _ in range(1000000):
        facing = random.choice(xrange(4))
        while BOARD.get(curr + ROBOT_DIRS[facing], 1) == 0:
            facing = random.choice(xrange(4))

        GLOBAL_INPUTS[0] = facing + 1
        resp = next(vm)

        if resp == 0:
            BOARD[curr + ROBOT_DIRS[facing]] = 0
        elif resp == 1:
            curr += ROBOT_DIRS[facing]
            BOARD[curr] = 1
        elif resp == 2:
            curr += ROBOT_DIRS[facing]
            OXYGEN = curr
            BOARD[curr] = 2

except StopIteration:
    pass

# We should have found the oxygen tank after this many ticks
assert 2 in BOARD.values()

print "Optimal movement to oxygen:", bfs(BOARD, Point(0, 0), OXYGEN)
print "Minutes taken to fill up:", bfs(BOARD, OXYGEN)
