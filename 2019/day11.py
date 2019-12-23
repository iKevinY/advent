import time
import fileinput
from collections import defaultdict

from intcode import emulate


def simulate_robot(tape, start=0):
    grid = {}
    grid[0, 0] = start

    facing = 0
    x, y = 0, 0

    inputs = [start]
    robot = emulate(tape[:], inputs)

    try:
        while True:
            grid[x, y] = next(robot)
            if next(robot) == 0:
                facing = (facing - 1) % 4
            else:
                facing = (facing + 1) % 4

            if facing == 0:
                y += 1
            elif facing == 1:
                x += 1
            elif facing == 2:
                y -= 1
            elif facing == 3:
                x -= 1

            inputs.append(grid.get((x, y), 0))
    except StopIteration:
        return grid


# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000

# Part 1
grid = simulate_robot(TAPE, 0)
print "Number of painted tiles:", len(grid.keys())


# Part 2
grid = simulate_robot(TAPE, 1)

print "Registration ID:\n"
xs, ys = zip(*grid.keys())
for y in reversed(range(min(ys), max(ys) + 1)):
    print ''.join(
        '#' if grid.get((x, y)) else ' '
        for x in range(min(xs), max(xs) + 1))
