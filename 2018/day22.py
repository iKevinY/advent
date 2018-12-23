import os  # NOQA
import sys  # NOQA
import heapq
import fileinput
from collections import Counter, defaultdict, deque, namedtuple  # NOQA

from utils import memoize
from utils import Point, DIRS, DIRS_4, DIRS_8  # NOQA


MOD = 20183


@memoize
def geo_index(x, y):
    if x == 0 and y == 0:
        return 0
    elif x == TX and y == TY:
        return 0
    elif y == 0:
        return (x * 16807) % MOD
    elif x == 0:
        return (y * 48271) % MOD
    else:
        return (ero_level(x - 1, y) * ero_level(x, y - 1)) % MOD


@memoize
def ero_level(x, y):
    return (geo_index(x, y) + DEPTH) % MOD


@memoize
def risk_level(x, y):
    return ero_level(x, y) % 3


lines = fileinput.input()
DEPTH = int(lines[0].split()[1])
TX, TY = (int(x) for x in lines[1].split()[1].split(','))

print "Total risk level for rectangle:", sum(risk_level(x, y) for x in range(TX + 1) for y in range(TY + 1))


# In rocky regions  (0), can use torch   (1) or gear    (2)
# In wet regions    (1), can use gear    (2) or neither (0)
# In narrow regions (2), can use neither (0) or torch   (1)
#
# Start at (0, 0) with the torch equipped.
ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
GEAR = 2

items = [NEITHER, TORCH, GEAR]

allowed = {
    ROCKY: [TORCH, GEAR],
    WET: [GEAR, NEITHER],
    NARROW: [NEITHER, TORCH],
}

State = namedtuple('State', 'time x y item')

state = State(0, 0, 0, TORCH)
horizon = [state]
seen = {}

while horizon:
    time, x, y, item = heapq.heappop(horizon)

    if x == TX and y == TY and item == TORCH:
        print "Minutes to reach the target:", time
        break

    # Hand-wavy upper bound on horizontal search limit (technically should be TX + TY)
    if x > TX * 3:
        continue

    if seen.get((x, y, item), 1e10) <= time:
        continue

    next_entry = (time, x, y, item)

    seen[(x, y, item)] = min(seen.get((x, y, item), 1e10), time)
    region = risk_level(x, y)

    for next_item in items:
        if next_item in allowed[risk_level(x, y)] and next_item != item:
            heapq.heappush(horizon, State(time + 7, x, y, next_item))

    for n in Point(x, y).neighbours_4():
        if n.x >= 0 and n.y >= 0 and risk_level(n.x, n.y) != item:
            heapq.heappush(horizon, State(time + 1, n.x, n.y, item))
