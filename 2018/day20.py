import fileinput
from collections import defaultdict
from utils import Point, DIRS_4


REGEX = fileinput.input()[0].strip().replace('$', '').replace('^', '')
DIRS = {a: b for a, b in zip('NESW', DIRS_4)}

# Build graph of facility
graph = defaultdict(set)
start = Point(0, 0)
curr = start
stk = []

for d in REGEX:
    if d in DIRS:
        nx = curr + DIRS[d]
        graph[curr].add(nx)
        graph[nx].add(curr)
        curr = nx
    elif d == '(':
        stk.append(curr)
    elif d == '|':
        curr = stk[-1]
    elif d == ')':
        curr = stk.pop()

seen = set()
horizon = [start]
dist = {}

# BFS to solve for minimum distances to rooms
depth = 0
while horizon:
    next_horizon = []

    for h in horizon:
        if h in seen:
            continue

        dist[h] = depth
        seen.add(h)

        for g in graph[h]:
            next_horizon.append(g)

    depth += 1
    horizon = next_horizon


print "Largest number of doors passed through:", max(d for d in dist.values())
print "Rooms passing through at least 1000 doors:", sum(d >= 1000 for d in dist.values())
