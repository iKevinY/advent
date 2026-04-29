import fileinput
import math
import re

GROUP_RE = r'[\d*+]+'


# Parse problem input.
MATRIX = []
ALL_NUMS = []
for y, line in enumerate(fileinput.input()):
    # Parse whole groups for part 1.
    groups = re.findall(GROUP_RE, line)
    if '*' not in groups:
        ALL_NUMS.append(groups)
    else:
        OPS = groups

        # Add a "simulated" blank line before the list of
        # operations to make part 2 processing easier.
        MATRIX.append([' ' for _ in range(len(MATRIX[-1]))])

    # Create a matrix to transpose for part 2.
    MATRIX.append(list(line))


# Solve part 1.
OPERANDS = list(zip(*ALL_NUMS))
PART_1 = 0
for operands, op in zip(OPERANDS, OPS):
    operands = [int(n) for n in operands]
    if op == '+':
        PART_1 += sum(operands)
    else:
        PART_1 += math.prod(operands)

print("Part 1:", PART_1)


# Solve part 2.
FLIPPED = list(zip(*MATRIX))
TAPE = ''.join(''.join(col) for col in reversed(FLIPPED))
PART_2 = 0

buffer = []
for group in re.findall(GROUP_RE, TAPE):
    if group == '+':
        PART_2 += sum(buffer)
        buffer = []
    elif group == '*':
        PART_2 += math.prod(buffer)
        buffer = []
    else:
        buffer.append(int(group))

print("Part 2:", PART_2)


