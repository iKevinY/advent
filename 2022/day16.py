import fileinput
from collections import deque, defaultdict
from functools import reduce
from itertools import permutations
from concurrent.futures import ProcessPoolExecutor

from utils import parse_line


GRAPH = defaultdict(set)
FLOW = {}

# Parse input.
for line in fileinput.input():
    valve, rate, tunnels = parse_line(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)

    for tunnel in tunnels.split(", "):
        GRAPH[valve].add(tunnel)

    FLOW[valve] = rate


# Create compressed graph representations that only contain
# information between valves that have a non-zero flow, where
# rather than a unweighted graph of implicit distance 1, the
# graph contains edge weights of the distance to get from
# valve X to Y via the shortest path in the global graph.
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

START = "AA"
START_TO_REAL = {}
real = [v for v in GRAPH if FLOW[v] > 0]
REAL = {v: i for i, v in enumerate(real)}
COMPRESSED = defaultdict(set)

for valve in REAL:
    START_TO_REAL[valve] = bfs(START, valve)

for a, b in permutations(REAL, 2):
    dist = bfs(a, b)
    COMPRESSED[a].add((b, dist))
    COMPRESSED[b].add((a, dist))


# Define helper functions to operate on bitstring representations
# of which valves have been visited, rather than using sets.
def is_node_set_in_bitstring(bitstring, node):
    return bool(bitstring & (1 << REAL[node]))

def set_node_in_bitstring(bitstring, node):
    return bitstring | (1 << REAL[node])

def is_bitstring_complete(bitstring):
    return bitstring + 1 == (1 << len(REAL))


def search(init_opened, max_time):
    best = 0
    seen = {}
    horizon = deque()

    # Recompute compressed graph based on limited nodes available.
    compressed = {
        a: [(n, d) for n, d in b if not is_node_set_in_bitstring(init_opened, n)]
        for a, b in COMPRESSED.items() if not is_node_set_in_bitstring(init_opened, a)
    }

    # Seed start positions with time and pressure based on the time it takes
    # to get from AA to that valve, + 1 minute to open the valve.
    for node in REAL:
        if is_node_set_in_bitstring(init_opened, node):
            continue

        start_time = START_TO_REAL[node] + 1
        start_pressure = (max_time - start_time) * FLOW[node]
        start_opened = set_node_in_bitstring(init_opened, node)
        state = (start_time, node, start_pressure, start_opened)
        horizon.append(state)

    while horizon:
        time, curr, pressure, opened = horizon.popleft()
        key = (curr, time, opened)

        if seen.get(key, -1) > pressure:
            continue

        seen[key] = pressure

        if time >= max_time:
            continue
        elif is_bitstring_complete(opened):
            continue

        if pressure > best:
            best = pressure

        # move
        for n, dist in COMPRESSED[curr]:
            if not is_node_set_in_bitstring(opened, n):
                new_time = time + dist + 1  # time to move + 1 minute to open
                extra_pressure = (max_time - new_time) * FLOW[n]
                new_opened = set_node_in_bitstring(opened, n)
                new_state = (new_time, n, pressure + extra_pressure, new_opened)

                horizon.append(new_state)

    return best


# Solve part 1.
print("Part 1:", search(0b0, 30))

# Solve part 2.
def dual_search(partition):
    a, b = partition
    return search(a, 26) + search(b, 26)

part_2 = 0

# Given the bitstring representation of opened nodes, the set of all possibilities is
# just all pairs of numbers that sum to 2^(len(REAL)) - 1. We iterate over the range
# of half this amount to ensure we don't double-up on pairs, thus removing the need
# for any sort of memoization (we compute precisely the results we need).
target = (1 << len(REAL)) - 1
partitions = [(n, target - n) for n in range(1 << (len(REAL) - 1))]

# This is not the optimal solution yet. If it were, I wouldn't be parallelizing.
parallel = False

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

    for p in loading(partitions, total=len(partitions)):
        part_2 = max(part_2, dual_search(p))

print("Part 2:", part_2)

