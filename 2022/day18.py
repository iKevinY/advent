import fileinput
from collections import deque

from utils import parse_nums, memoize


cubes = []

min_x = 1e9
max_x = -1e9
min_y = 1e9
max_y = -1e9
min_z = 1e9
max_z = -1e9

for line in fileinput.input():
    x, y, z = parse_nums(line)
    cubes.append((x, y, z))
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)
    min_z = min(z, min_z)
    max_z = max(z, max_z)

cubes = set(cubes)


OFFSETS = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]

def outside(x, y, z):
    xx = min_x <= x < max_x
    yy = min_y <= y < max_y
    zz = min_z <= z < max_z
    return not (xx and yy and zz)


KNOWN_INTERNALS = set()

def is_internal(node):
    global KNOWN_INTERNALS

    seen = set()
    horizon = deque([node])

    while horizon:
        n = horizon.popleft()
        x, y, z = n

        if n in seen:
            continue

        if n in KNOWN_INTERNALS:
            return True

        if outside(*n):
            return False

        seen.add(n)

        for dx, dy, dz in OFFSETS:
            nx = x + dx
            ny = y + dy
            nz = z + dz

            if (nx, ny, nz) in cubes:
                continue

            horizon.append((nx, ny, nz))

    # We are internal, so add everything we've seen to KNOWN_INTERNALS.
    KNOWN_INTERNALS |= seen

    return True

part_1 = 0
part_2 = 0

for x, y, z in cubes:
    for dx, dy, dz in OFFSETS:
        nx, ny, nz = x + dx, y + dy, z + dz
        if (nx, ny, nz) not in cubes:
            part_1 += 1
            if not is_internal((nx, ny, nz)):
                part_2 += 1

print("Part 1:", part_1)
print("Part 2:", part_2)
