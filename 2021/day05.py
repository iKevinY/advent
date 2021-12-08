import fileinput
from collections import Counter
from utils import parse_nums

lines = []

for line in fileinput.input():
    nums = parse_nums(line)
    lines.append(nums)

part_1 = Counter()
part_2 = Counter()

for (x1, y1, x2, y2) in lines:
    # Horizontal or vertical
    if x1 == x2 or y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1

        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                part_1[x, y] += 1
                part_2[x, y] += 1

    # Diagonal
    else:
        delta = abs(x2 - x1)
        x, y = x1, y1
        for n in range(delta + 1):
            part_2[x, y] += 1
            if x2 > x1:
                x += 1
            else:
                x -= 1

            if y2 > y1:
                y += 1
            else:
                y -= 1

print "Part 1:", sum(1 for v in part_1.values() if v > 1)
print "Part 2:", sum(1 for v in part_2.values() if v > 1)
