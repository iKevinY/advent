import sys
import fileinput
from collections import Counter

from utils import parse_nums, mul


MAX_X = 101
MAX_Y = 103
TREE_CRITERIA = 15


# Parse problem input.
robots = []
for line in fileinput.input():
    px, py, vx, vy = parse_nums(line)
    robots.append((px, py, vx, vy))


# Simulate robots.
for iteration in range(1, 10000):
    new_robots = []
    for px, py, vx, vy in robots:
        nx = (px + vx) % MAX_X
        ny = (py + vy) % MAX_Y
        new_robots.append((nx, ny, vx, vy))

    robots = new_robots

    # The "Christmas tree" is nicely outlined by a border, so if we
    # find a contiguous line of robots, it's probably the tree.
    picture = set((px, py) for px, py, _, _ in robots)

    contig = 0
    max_contig = 0

    for y in range(MAX_Y):
        for x in range(MAX_X):
            if (x, y) in picture:
                contig += 1
                max_contig = max(contig, max_contig)
            else:
                contig = 0

    if max_contig > TREE_CRITERIA:
        print("Part 2:", iteration)
        sys.exit()


    if iteration == 100:
        quadrants = Counter()
        for px, py, _, _ in robots:
            if px < MAX_X // 2 and py < MAX_Y // 2:
                quadrants[1] += 1
            elif px < MAX_X // 2 and py > MAX_Y // 2:
                quadrants[2] += 1
            elif px > MAX_X // 2 and py < MAX_Y // 2:
                quadrants[3] += 1
            elif px > MAX_X // 2 and py > MAX_Y // 2:
                quadrants[4] += 1

        print("Part 1:", mul(quadrants.values()))
