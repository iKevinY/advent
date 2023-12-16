import fileinput
from utils import Point, DIRS, N, E, S, W


# Parse problem input.
GRID = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        GRID[Point(x, y)] = c

MAX_X = x
MAX_Y = y


def simulate_light(grid, start, initial_d):
    photons = [(start, initial_d)]
    seen = set()
    while photons:
        photon, d = photons.pop()

        if photon not in grid:
            continue

        if (photon, d) in seen:
            continue

        seen.add((photon, d))

        if grid[photon] == '.':
            photons.append((photon + d, d))
        elif grid[photon] == '/':
            nd = [W, E, S, N][[N, S, E, W].index(d)]
            photons.append((photon + nd, nd))
        elif grid[photon] == '\\':
            nd = [E, W, N, S][[N, S, E, W].index(d)]
            photons.append((photon + nd, nd))
        elif grid[photon] == '|':
            if d in (N, S):
                photons.append((photon + d, d))
            else:
                photons.append((photon + N, N))
                photons.append((photon + S, S))
        elif grid[photon] == '-':
            if d in (E, W):
                photons.append((photon + d, d))
            else:
                photons.append((photon + E, E))
                photons.append((photon + W, W))

    return len(set(p for p, d in seen))


def part_2_starts(grid):
    for x in range(MAX_X):
        yield Point(x, 0), N
        yield Point(x, MAX_Y - 1), S

    for y in range(MAX_Y):
        yield Point(0, y), E
        yield Point(MAX_X - 1, y), W


print("Part 1:", simulate_light(GRID, Point(0, 0), E))
print("Part 2:", max(simulate_light(GRID, p, d) for p, d in part_2_starts(GRID)))
