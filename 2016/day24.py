import fileinput
from collections import deque
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


def bfs(grid, start, goal):
    horizon = deque([(start, 0)])
    seen = set(start)

    while horizon:
        (x, y), dst = horizon.pop()

        if (x, y) == goal:
            return dst

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and valid(grid, nx, ny):
                horizon.appendleft(((nx, ny), dst + 1))
                seen.add((nx, ny))


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
        distances[a, b] = distances[b, a] = bfs(grid, locations[a], locations[b])

    paths = list(permutations(range(1, max(locations) + 1)))
    print "Fewest steps to visit all numbers:", min(navigate(distances, path) for path in paths)
    print "Fewest steps to also return to 0:", min(navigate(distances, path, complete=True) for path in paths)
