import fileinput
from itertools import product

from utils import transposed


KEYS = []
LOCKS = []

block = []
for line in fileinput.input():
    if line == '\n':
        if block[0][0] == '#':
            KEYS.append(transposed(block))
        else:
            LOCKS.append(transposed(block))
        block = []
    else:
        block.append(line.strip())

# The last image is a lock.
LOCKS.append(block)

# Solve problem.
KEYS = [[pin.count('#') for pin in key] for key in KEYS]
LOCKS = [[pin.count('#') for pin in lock] for lock in LOCKS]
print("Part 1:", sum(1 if all(a + b <= 7 for a, b in zip(key, lock)) else 0 for key, lock in product(KEYS, LOCKS)))
