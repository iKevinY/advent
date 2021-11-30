import fileinput
from utils import Point, DIRS

DIR_MAP = 'NESW'

p1 = Point(0, 0)
p2 = Point(0, 0)
wp = Point(10, 1)

facing = 1  # start at 1 to match DIRS

for line in fileinput.input():
    d = line[0]
    n = int(line[1:])

    if d in DIR_MAP:
        delta = DIRS[DIR_MAP.index(d)] * n
        p1 += delta
        wp += delta

    elif d == 'L' or d == 'R':
        turns = n // 90
        if d == 'L':
            turns = 4 - turns

        facing = (facing + turns) % 4

        wp = wp.rotate(turns)

    elif d == 'F':
        p1 += DIRS[facing] * n
        p2 += wp * n

print "Part 1:", p1.manhattan
print "Part 2:", p2.manhattan
