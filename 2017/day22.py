import fileinput
from utils import Point, DIRS


def simulate_activity(x, y, facing, grid, mapping):
    node = grid.get((x, y), '.')
    new_node, df = mapping[node]

    # Update node
    grid[x, y] = new_node

    # Update direction and position
    nf = (facing + df) % 4
    x += DIRS[nf].x
    y += DIRS[nf].y

    return x, y, nf, new_node == '#'


# Maps node transformations and turn-direction
PART_1_MAP = {
    '#': ('.', -1),
    '.': ('#',  1),
}

PART_2_MAP = {
    '.': ('W',  1),
    'W': ('#',  0),
    '#': ('F', -1),
    'F': ('.',  2),
}

GRID = {}
HEIGHT = 0
WIDTH = 0

# Read puzzle input
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        GRID[x, y] = c

    WIDTH = x + 1
    HEIGHT += 1

# Part 1
x = WIDTH // 2
y = HEIGHT // 2
facing = 2
grid = GRID.copy()
infections_caused = 0

for _ in range(10000):
    x, y, facing, caused = simulate_activity(x, y, facing, grid, PART_1_MAP)
    if caused:
        infections_caused += 1

print "Infections caused in Part 1:", infections_caused

# Part 2
x = WIDTH // 2
y = HEIGHT // 2
facing = 2
grid = GRID.copy()
infections_caused = 0

for _ in range(10000000):
    x, y, facing, caused = simulate_activity(x, y, facing, grid, PART_2_MAP)
    if caused:
        infections_caused += 1

print "Infections caused in Part 2:", infections_caused
