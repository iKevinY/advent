import fileinput

DIRS = [
    (1, 0),  # north
    (0, 1),  # east
    (-1, 0), # south
    (0, -1)  # west
]

seen = set()
double_visit = False

x = 0
y = 0
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
            x += DIRS[facing][0]
            y += DIRS[facing][1]

            if not double_visit and (x, y) in seen:
                print "First double-visit at ({}, {}) ({} blocks away)".format(x, y, abs(x) + abs(y))
                double_visit = True
            else:
                seen.add((x, y))

print "Easter Bunny HQ is at ({}, {}) ({} blocks away)".format(x, y, abs(x) + abs(y))
