import fileinput
from collections import defaultdict
from itertools import product

grid_1 = defaultdict(lambda: '.')
grid_2 = defaultdict(lambda: '.')

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        grid_1[x, y, 0] = c
        grid_2[x, y, 0, 0] = c

max_dim = max(x, y)


for i in range(6):
    new_grid_1 = defaultdict(lambda: '.')
    new_grid_2 = defaultdict(lambda: '.')

    for x, y, z, w in product(range(-i - 1, max_dim + i + 1), repeat=4):
        neighs_1 = 0
        neighs_2 = 0

        for dx, dy, dz, dw in product(range(-1, 2), repeat=4):
            if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                continue

            if grid_1[x + dx, y + dy, z + dz] == '#' and dw == 0:
                neighs_1 += 1
            if grid_2[x + dx, y + dy, z + dz, w + dw] == '#':
                neighs_2 += 1


        if grid_1[x, y, z] == '#' and (neighs_1 == 2 or neighs_1 == 3):
            new_grid_1[x, y, z] = '#'

        elif grid_1[x, y, z] == '.' and neighs_1 == 3:
            new_grid_1[x, y, z] = '#'

        if grid_2[x, y, z, w] == '#' and (neighs_2 == 2 or neighs_2 == 3):
            new_grid_2[x, y, z, w] = '#'

        elif grid_2[x, y, z, w] == '.' and neighs_2 == 3:
            new_grid_2[x, y, z, w] = '#'

    grid_1 = new_grid_1
    grid_2 = new_grid_2


print "Part 1:", sum(c == '#' for c in grid_1.values())
print "Part 2:", sum(c == '#' for c in grid_2.values())

