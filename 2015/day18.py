import fileinput
import itertools
import re

def get_neighbours(x, y):
    square = [(a, b)
        for a in range(max(0, x-1), min(x+2, WIDTH))
        for b in range(max(0, y-1), min(y+2, HEIGHT))]
    square.remove((x, y))
    return square

def next_state(grid, x, y, sticky_corners=False):
    if sticky_corners:
        if (x in (0, WIDTH-1)) and (y in (0, HEIGHT-1)):
            return True

    neighbours = get_neighbours(x, y)
    on_neighbours = sum(grid[b][a] for a, b in neighbours)

    if grid[y][x]:
        return int(on_neighbours in (2, 3))
    else:
        return int(on_neighbours == 3)

def next_grid(grid, sticky_corners=False):
    return [[next_state(grid, x, y, sticky_corners) for x in range(WIDTH)] for y in range(HEIGHT)]

def count_lights(grid):
    return sum(sum(x for x in row) for row in grid)

def print_grid(grid):
    for row in grid:
        print ''.join('#' if c else '.' for c in row)


# Parse input
rows = [line for line in fileinput.input()]
LIGHTS = [[1 if c == '#' else 0 for c in row.strip()] for row in rows]

# Define constants
WIDTH = len(LIGHTS[0])
HEIGHT = len(LIGHTS)
ITERATIONS = 100

print "Simulating {}x{} grid of lights.".format(WIDTH, HEIGHT)

grid = LIGHTS
for _ in range(ITERATIONS):
    grid = next_grid(grid)

print "Lights on after {} iterations: {}".format(ITERATIONS, count_lights(grid))

# Stick corners initially
grid = LIGHTS
for x in (0, WIDTH-1):
    for y in (0, HEIGHT-1):
        grid[y][x] = 1

for _ in range(ITERATIONS):
    grid = next_grid(grid, sticky_corners=True)

print "Lights on with stuck corners: {}".format(count_lights(grid))
