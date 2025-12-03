import fileinput
from utils import parts


# Read problem input.
RANGES = []
for line in fileinput.input():
    for r in line.split(','):
        x, y = r.split('-')
        RANGES.append((int(x), int(y)))


# Solve puzzle.
PART_1 = 0
PART_2 = 0

for x, y in RANGES:
    part_1_invalids = set()
    part_2_invalids = set()

    for n in range(x, y + 1):
        invalid = False
        for d in range(2, len(str(n)) + 1):
            n = str(n)
            if len(n) % d != 0:
                continue

            # Split the string `n` into `d` parts and
            # check if they're all the same string.
            if len(set(parts(n, d))) == 1:
                if d == 2:
                    part_1_invalids.add(int(n))

                part_2_invalids.add(int(n))
                break

    PART_1 += sum(part_1_invalids)
    PART_2 += sum(part_2_invalids)


print("Part 1:", PART_1)
print("Part 2:", PART_2)
