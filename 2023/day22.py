import fileinput
import copy
from itertools import permutations

from utils import parse_nums


def supports(b1, b2):
    # Returns true if b1 supports b2.
    ax, ay, az, bx, by, bz = b1
    cx, cy, cz, dx, dy, dz = b2

    b1_top = max(az, bz)
    b2_base = min(cz, dz)

    if b1_top + 1 != b2_base:
        return False

    ax, bx = min(ax, bx), max(ax, bx)
    ay, by = min(ay, by), max(ay, by)

    cx, dx = min(cx, dx), max(cx, dx)
    cy, dy = min(cy, dy), max(cy, dy)

    # can't support because off on one axis
    if bx < cx or ax > dx:
        return False

    if by < cy or ay > dy:
        return False

    return True

def simulate(bricks):
    """Returns the set of brick IDs that moved in the simulation."""
    all_touched = set()
    stationary = set()
    while True:
        moved = False
        for i, brick in enumerate(bricks):
            if i in stationary:
                continue

            # If the brick is on the ground, it can't fall more.
            if brick[2] == 1 or brick[5] == 1:
                stationary.add(i)
                continue

            # See if brick is supported by any other b2
            supported = False
            for j, b2 in enumerate(bricks):
                if i == j:
                    continue

                if supports(b2, brick):
                    # Can't fall because b2 supports brick,
                    # but it might fall in a later tick.
                    supported = True

                    if j in stationary:
                        # Nah, it won't.
                        stationary.add(i)
                    break

            if not supported:
                # Make the brick fall one tick.
                brick[2] -= 1
                brick[5] -= 1

                # Brick i has now moved in this simulation.
                all_touched.add(i)
                moved = True
                break

        if not moved:
            break

    return all_touched


# Read problem input.
BRICKS = []
for line in fileinput.input():
    BRICKS.append(list(parse_nums(line.strip())))

# Try to simulate bricks lower to the ground first.
BRICKS.sort(key=lambda b: min(b[2], b[5]))
simulate(BRICKS)

# graph[a] -> b means a supports b.
graph = {i: set() for i in range(len(BRICKS))}
for i, j in permutations(range(len(BRICKS)), 2):
    if supports(BRICKS[i], BRICKS[j]):
        graph[i].add(j)

part_1 = 0
part_2 = 0

for k in graph:
    # Nothing above this brick.
    if not graph[k]:
        part_1 += 1
        continue

    # Simulate removing the brick.
    without_brick = [copy.copy(BRICKS[i]) for i in range(len(BRICKS)) if i != k]
    num_moved = len(simulate(without_brick))
    if num_movedd == 0:
        part_1 += 1
    else:
        part_2 += num_moved

print("Part 1:", part_1)
print("Part 2:", part_2)
