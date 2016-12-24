import fileinput
import heapq
from itertools import combinations, permutations

DIRS = [
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1)
]


def valid(grid, x, y):
    try:
        return grid[y][x] != '#'
    except IndexError:
        return False


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start, goal):
    """
    Returns the length of the shortest path, minimizing f(n) = g(n) + h(n)
    as a search strategy. Using a closed set to skip over nodes that have
    already seen is valid so long as h(n) is admissible.
    """

    frontier = [(0, start)]
    seen = set()
    cost_to = {start: 0}  # this is g(n)

    while frontier:
        _priority, (x, y) = heapq.heappop(frontier)

        if (x, y) == goal:
            return cost_to[goal]

        seen.add((x, y))

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy

            if (nx, ny) in seen or not valid(grid, nx, ny):
                continue

            new_dist = cost_to[x, y] + 1

            if (nx, ny) not in cost_to or new_dist < cost_to[nx, ny]:
                cost_to[nx, ny] = new_dist
                priority = new_dist + heuristic(goal, (nx, ny))
                heapq.heappush(frontier, (priority, (nx, ny)))


def navigate(distances, path, complete=False):
    dst = distances[0, path[0]]
    for i in range(len(path) - 1):
        dst += distances[path[i], path[i+1]]

    if complete:
        dst += distances[path[-1], 0]

    return dst


if __name__ == '__main__':
    grid = []
    locations = {}

    for y, line in enumerate(fileinput.input()):
        for x, tile in enumerate(line):
            if tile.isdigit():
                locations[int(tile)] = (x, y)

        grid.append(list(line))

    distances = {}

    for a, b in combinations(range(max(locations) + 1), 2):
        distances[a, b] = distances[b, a] = a_star(grid, locations[a], locations[b])

    paths = list(permutations(range(1, max(locations) + 1)))
    print "Fewest steps to visit all numbers:", min(navigate(distances, path) for path in paths)
    print "Fewest steps to also return to 0:", min(navigate(distances, path, complete=True) for path in paths)
