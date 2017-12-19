import fileinput
from utils import Point, DIRS


DIAGRAM = {}

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip('\n')):
        if y == 0 and c == '|':
            start = Point(x, y)

        DIAGRAM[Point(x, y)] = c

d = 0
pos = start

steps = 0
letters = []

while True:
    tile = DIAGRAM.get(pos, ' ')

    if tile.isalpha():
        letters.append(tile)

    elif tile == '+':
        # Determine whether to turn left or right
        right_tile = DIAGRAM.get(pos + DIRS[(d + 1) % 4], ' ')
        if right_tile == ' ':
            d = (d - 1) % 4
        else:
            d = (d + 1) % 4

    elif tile == ' ':
        break

    pos = pos + DIRS[d]
    steps += 1

print "Letters seen in path:", ''.join(letters)
print "Total number of steps:", steps
