import fileinput
from collections import deque, defaultdict
from functools import reduce
from itertools import permutations
from concurrent.futures import ProcessPoolExecutor

from utils import parse_line, memoize

from more_itertools import set_partitions


GRAPH = defaultdict(set)
FLOW = {}

# Parse input.
for line in fileinput.input():
    valve, rate, tunnels = parse_line(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)

    for tunnel in tunnels.split(", "):
        GRAPH[valve].add(tunnel)

    FLOW[valve] = rate

# Construct compressed graph
def bfs(start, end):
    seen = set()
    horizon = deque([(start, 0)])
    while horizon:
        curr, dist = horizon.popleft()
        if curr in seen:
            continue

        if curr == end:
            return dist

        seen.add(curr)

        for n in GRAPH[curr]:
            horizon.append((n, dist + 1))


# Solve part 1.
START = "AA"
START_TO_REAL = {}
REAL = [v for v in GRAPH if FLOW[v] > 0]
COMPRESSED = defaultdict(set)

for valve in REAL:
    START_TO_REAL[valve] = bfs(START, valve)

for a, b in permutations(REAL, 2):
    dist = bfs(a, b)
    COMPRESSED[a].add((b, dist))
    COMPRESSED[b].add((a, dist))


@memoize
def search(nodes, max_time):
    best = 0
    seen = {}
    horizon = deque()

    # Recompute compressed graph based on limited nodes available.
    compressed = {
        a: [(n, d) for n, d in b if n in nodes]
        for a, b in COMPRESSED.items() if a in nodes
    }

    # Seed start positions with time and pressure based on the time it takes
    # to get from AA to that valve, + 1 minute to open the valve.
    for node in nodes:
        start_time = START_TO_REAL[node] + 1
        start_pressure = (max_time - start_time) * FLOW[node]
        state = (start_time, node, start_pressure, frozenset([node]))
        horizon.append(state)

    while horizon:
        time, curr, pressure, opened = horizon.popleft()
        key = (curr, time, opened)

        if seen.get(key, -1) > pressure:
            continue

        seen[key] = pressure

        if time >= max_time:
            continue
        elif len(opened) >= len(nodes):
            continue

        if pressure > best:
            best = pressure

        # move
        for n, dist in compressed[curr]:
            if n not in opened:
                new_time = time + dist + 1
                extra_pressure = (max_time - new_time) * FLOW[n]
                new_opened = frozenset([n]) | opened
                new_state = (new_time, n, pressure + extra_pressure, new_opened)

                horizon.append(new_state)

    return best

print("Part 1:", search(COMPRESSED, 30))


# Solve part 2.
def dual_search(partition):
    a, b = partition
    return search(frozenset(a), 26) + search(frozenset(b), 26)


part_2 = 0
partitions = list(set_partitions(REAL, 2))

# This is not the optimal solution yet. If it were, I wouldn't be parallelizing.
parallel = True

if parallel:
    with ProcessPoolExecutor() as pool:
        try:
            results = pool.map(dual_search, partitions)
        except:
            pass
    part_2 = reduce(max, results)

else:
    # Render loading bar if tqdm installed.
    try:
        from tqdm import tqdm as loading
    except ImportError:
        loading = lambda x, total: x

    for p in loading(set_partitions(REAL, 2), total=len(partitions)):
        part_2 = max(part_2, dual_search(p))

print("Part 2:", part_2)

