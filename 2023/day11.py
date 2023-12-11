import fileinput
from itertools import combinations


# Parse problem input.
GALAXIES = set()

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        if c == '#':
            GALAXIES.add((x, y))

# Find "expanded" rows and columns.
empty_row = set(range(y))
empty_col = set(range(x))

for (gx, gy) in GALAXIES:
    empty_col.discard(gx)
    empty_row.discard(gy)

# Solve problem.
part_1 = 0
part_2 = 0

for (sx, sy), (ex, ey) in combinations(GALAXIES, 2):
    crossed = 0
    for y in range(min(sy, ey), max(sy, ey) + 1):
        if y in empty_row:
            crossed += 1

    for x in range(min(sx, ex), max(sx, ex) + 1):
        if x in empty_col:
            crossed += 1

    # Raw distance is the Manhattan distance between the pair.
    raw_distance = abs(sy - ey) + abs(sx - ex)
    part_1 += raw_distance + crossed * 1
    part_2 += raw_distance + crossed * 999999

print("Part 1:", part_1)
print("Part 2:", part_2)

