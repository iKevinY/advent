import sys
import fileinput

from utils import memoize
from intcode import emulate


@memoize
def affected(x, y):
    if x < 0 or y < 0:
        return 0

    vm = emulate(TAPE, [y, x])
    return next(vm)


# Read problem input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000


part_1 = sum(affected(x, y) for y in range(50) for x in range(50))
print "Points affected by tractor beam:", part_1

# Arbitrary starting point for my input that skips past the incontinuity
x = 37
y = 49

while True:
    while affected(x, y):
        y += 1

    assert affected(x, y) == 0

    while not affected(x, y):
        x += 1

    while affected(x, y + 1):
        y += 1

    assert affected(x, y) == 1
    assert affected(x + 1, y) == 1
    assert affected(x - 1, y) == 0
    assert affected(x, y + 1) == 0
    assert affected(x, y - 1) == 1

    if affected(x, y - 99) == 1 and affected(x + 99, y) == 1:
        for yy in range(y - 99, y + 1):
            for xx in range(x, x + 100):
                if not affected(xx, yy):
                    break
            else:
                continue

            break
        else:
            print "100x100 point checksum:", x * 10000 + (y - 99)
            sys.exit()
