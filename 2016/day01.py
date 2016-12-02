import fileinput
from utils import Point

DIRS = [
    Point(1, 0),  # north
    Point(0, 1),  # east
    Point(-1, 0), # south
    Point(0, -1)  # west
]

seen = set()
double_visit = ''

pos = Point(0, 0)
facing = 0

for line in fileinput.input():
    directions = line.split(', ')

    for d in directions:
        turn = d[0]
        steps = int(d[1:])

        if turn == 'L':
            facing = (facing - 1) % 4
        else:
            facing = (facing + 1) % 4

        for _ in range(steps):
            pos += DIRS[facing]
            if not double_visit and pos in seen:
                double_visit = "First double-visit at ({}, {}) ({} blocks away)".format(pos.x, pos.y, pos.manhattan)
            else:
                seen.add(pos)

print "Easter Bunny HQ is at ({}, {}) ({} blocks away)".format(pos.x, pos.y, pos.manhattan)
print double_visit
