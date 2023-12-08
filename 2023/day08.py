import fileinput
from itertools import cycle
from functools import reduce
from utils import parse_line, lcm


# Parse input.
elements = {}
for i, line in enumerate(fileinput.input()):
    if i == 0:
        instructions = line.strip()
    elif i >= 2:
        node, left, right = parse_line(r'(.+) = \((.+), (.+)\)', line)
        elements[node] = (left, right)

# Solve part 1.
curr = 'AAA'
for i, ins in enumerate(cycle(instructions), start=1):
    if ins == 'L':
        curr = elements[curr][0]
    else:
        curr = elements[curr][1]

    if curr == 'ZZZ':
        print("Part 1:", i)
        break

# Solve part 2.
starts = [n for n in elements if n.endswith('A')]
cycles = []
for start in starts:
    curr = start
    seen = {}

    for i, ins in enumerate(cycle(instructions), start=1):
        if ins == 'L':
            curr = elements[curr][0]
        else:
            curr = elements[curr][1]

        if curr.endswith('Z'):
            if curr in seen:
                cycles.append(i - seen[curr])
                break

            seen[curr] = i

        i += 1

print("Part 2:", int(reduce(lcm, cycles, 1)))

