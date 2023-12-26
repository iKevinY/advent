import fileinput
from collections import deque, defaultdict

from utils import Point, N, S, E, W, DIRS


SLOPES = {
    '^': S,
    'v': N,
    '<': W,
    '>': E,
}


def get_neighbours(graph, node, part_2=False):
    """In part 2, we ignore slopes."""
    if graph.get(node) == '#':
        return

    if not part_2:
        if graph.get(node) in SLOPES:
            yield node + SLOPES[graph.get(node)]
            return

    for d in DIRS:
        np = node + d
        if np not in graph:
            continue

        neighbour = graph.get(np)

        if neighbour == '#':
            continue

        if not part_2 and neighbour in SLOPES and d != SLOPES[neighbour]:
            continue

        yield np


def longest_path(graph, start, end, part_2=False):
    BITMASK_MAPPING = {k: i for i, k in enumerate(graph)}
    horizon = [(start, 0, 0b0)]
    best = 0

    while horizon:
        curr, dist, seen = horizon.pop()

        if curr == end:
            best = max(best, dist)
            continue

        mask = (1 << BITMASK_MAPPING[curr])

        if seen & mask:
            continue

        new_seen = seen | mask

        for neighbour, weight in graph[curr]:
            horizon.append((neighbour, dist + weight, new_seen))

    return best


def compress_graph(graph, part_2=False):
    # Sort all points in graph by their degree.
    degrees = defaultdict(set)
    for node in graph:
        degrees[len(list(get_neighbours(graph, node, part_2)))].add(node)

    key_points = degrees[1] | degrees[3] | degrees[4]


    # Find the distance from node to all other "key points" it can reach.
    def bfs(start):
        horizon = deque([(start, 0)])
        seen = set()

        while horizon:
            curr, dist = horizon.pop()

            if curr != start and curr in key_points:
                yield curr, dist
                continue

            if curr in seen:
                continue

            seen.add(curr)

            for neighbour in get_neighbours(graph, curr, part_2):
                horizon.appendleft((neighbour, dist + 1))


    # Create the compressed weighted graph.
    compressed = defaultdict(list)

    for node in key_points:
        for neighbour, weight in bfs(node):
            compressed[node].append((neighbour, weight))

    return compressed


# Parse problem input.
GRAPH = {}
START = None
END = None
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        if c == '.':
            if y == 0:
                START = p

            END = p

        GRAPH[p] = c

print("Part 1:", longest_path(compress_graph(GRAPH), START, END))
print("Part 2:", longest_path(compress_graph(GRAPH, part_2=True), START, END, part_2=True))

