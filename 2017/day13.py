import fileinput
from itertools import count


def scanner(height, time):
    """Return the position of a given scanner height at a given time."""
    offset = time % ((height - 1) * 2)

    if offset > height - 1:
        return 2 * (height - 1)
    else:
        return offset


HEIGHTS = {}

for line in fileinput.input():
    depth, rnge = [int(x) for x in line.strip().split(': ')]
    HEIGHTS[depth] = rnge

# Part 1
severity = 0
for pos in HEIGHTS:
    if scanner(HEIGHTS[pos], pos) == 0:
        severity += pos * HEIGHTS[pos]

print "Severity of whole trip:", severity

# Part 2
for delay in count():
    for pos in HEIGHTS:
        if scanner(HEIGHTS[pos], delay + pos) == 0:
            break
    else:
        print "Minimal delay to not get caught:", delay
        break
