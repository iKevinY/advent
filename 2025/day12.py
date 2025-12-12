import fileinput
from collections import Counter


BLOCK_SIZES = Counter()

part_1 = 0
curr_block = None

for line in fileinput.input():
    line = line.strip()

    # Reading a region.
    if 'x' in line:
        size, counts = line.split(': ')
        w, h = [int(x) for x in size.split('x')]
        counts = [int(x) for x in counts.split()]

        region_area = w * h
        block_area = sum(BLOCK_SIZES[i] * n for i, n in enumerate(counts))

        # The puzzle input is constructed to nicely tessellate the rectangular
        # grid, so all we need to do is check if the area amount would work.
        if block_area <= region_area:
            ans += part_1

    else:
        if ':' in line:
            curr_block = int(line[:-1])
        elif '#' in line or '.' in line:
            BLOCK_SIZES[curr_block] += line.count('#')

print("Part 1:", part_1)

