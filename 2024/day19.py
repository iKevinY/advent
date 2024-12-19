import fileinput
import functools


@functools.lru_cache()
def num_designs(towel, patterns):
    poss = 0

    for pattern in patterns:
        l = len(pattern)
        if towel == pattern:
            poss += 1
        elif towel[:l] == pattern:
            sub_poss = num_designs(towel[l:], patterns)
            if sub_poss:
                poss += sub_poss

    return poss


# Read problem input.
TOWELS = []
for line in fileinput.input():
    if ',' in line:
        PATTERNS = frozenset(line.strip().split(', '))
    elif line.strip():
        TOWELS.append(line.strip())


# Solve problem.
designs = [num_designs(towel, PATTERNS) for towel in TOWELS]
print("Part 1:", sum(1 for d in designs if d))
print("Part 2:", sum(designs))
