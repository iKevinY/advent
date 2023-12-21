import fileinput
from collections import defaultdict, deque, Counter

from utils import Point


PART_1_STEPS = 64
PART_2_STEPS = 26501365


def search(start, max_dist):
    horizon = deque([(start, 0)])
    cost_so_far = {}

    while horizon:
        curr, dist = horizon.pop()

        if dist > max_dist:
            continue

        if curr in cost_so_far:
            continue

        cost_so_far[curr] = dist

        for n in curr.neighbours_4():
            if GRAPH.get(n) != '.':
                continue

            horizon.appendleft((n, dist + 1))

    return sum(1 for c, v in cost_so_far.items() if v % 2 == ((max_dist % 2)))


# Read problem input.
GRAPH = {}
START = None
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        if c == 'S':
            START = p
            GRAPH[p] = '.'
        else:
            GRAPH[p] = c

# Solve part 1.
print("Part 1:", search(START, 64))

# Solve part 2.
HEIGHT = y + 1
WIDTH = x + 1
assert HEIGHT == WIDTH

assert START.x == START.y == (HEIGHT // 2) == (WIDTH // 2)
RADIUS = START.x
assert (PART_2_STEPS % WIDTH) == RADIUS

# Define the key search-start points for blocks within the infinite diamond.
EDGE_STARTS = [Point(x, y) for x, y in [(RADIUS, 0), (WIDTH - 1, RADIUS), (0, RADIUS), (RADIUS, HEIGHT - 1)]]
CORNER_STARTS = [Point(x, y) for x, y in [(0, 0), (0, HEIGHT - 1), (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1)]]

# Start computing the final answer to part 2. We leverage the following properties of the problem input:
#   - There is a straight path from the central starting point to the outer edges of the block.
#   - The step length is equal to the block radius mod block length, meaning there is perfect
#     symmetry even on the outside edges of the diamond that gets formed.

# First, add in the centre piece of the diamond.
part_2 = search(START, PART_2_STEPS)

# Compute how many times we need to add "full edge pieces" in with parity.
num_edge_pieces = Counter()
for i, x in enumerate(range(WIDTH, PART_2_STEPS - RADIUS, WIDTH), start=1):
    num_edge_pieces[i % 2] += 1

edge_addition = 0
for s in EDGE_STARTS:
    # Add "fully searched" edge blocks.
    edge_addition += num_edge_pieces[PART_2_STEPS % 2] * search(s, PART_2_STEPS)
    edge_addition += num_edge_pieces[(PART_2_STEPS + 1) % 2] * search(s, PART_2_STEPS + 1)

    # Accomodate the outer tips of the infinite diamond.
    edge_addition += search(s, WIDTH - 1)

part_2 += edge_addition

# Compute how many "corner pieces" are scattered on the edge of the diamond with parity.
num_corner_pieces = Counter()  # track parity
for i, _ in enumerate(range(WIDTH, PART_2_STEPS - WIDTH * 1, WIDTH), start=0):
    num_corner_pieces[i % 2] += i

corner_addition = 0
for s in CORNER_STARTS:
    # Add "fully searched" corner blocks.
    corner_addition += search(s, PART_2_STEPS) * num_corner_pieces[1]
    corner_addition += search(s, PART_2_STEPS + 1) * num_corner_pieces[0]

    # Accomodate the outer edges of the infinite diamond.
    corner_addition += search(s, WIDTH + RADIUS - 1) * ((PART_2_STEPS // WIDTH) - 1)
    corner_addition += search(s, RADIUS - 1) * ((PART_2_STEPS // WIDTH))

part_2 += corner_addition

print("Part 2:", part_2)
