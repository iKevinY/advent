import fileinput
from itertools import permutations
from collections import defaultdict

from utils import Point


# Parse problem input.
BOARD = {}
ANTENNAE = defaultdict(set)
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        BOARD[p] = c
        if c != '.':
            ANTENNAE[c].add(p)

# Solve problem.
part_1_antinodes = set()
part_2_antinodes = set()

for freq, locs in ANTENNAE.items():
    for a, b in permutations(locs, 2):
        for i in range(len(line)):
            antinode = b + (b - a) * i
            part_2_antinodes.add(antinode)
            if i == 1:
                part_1_antinodes.add(antinode)

print("Part 1:", len(part_1_antinodes & set(BOARD)))
print("Part 2:", len(part_2_antinodes & set(BOARD)))
