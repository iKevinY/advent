import fileinput
from utils import Point

KEYPAD_1 = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

KEYPAD_2 = [
    ['_', '_', '1', '_', '_'],
    ['_', '2', '3', '4', '_'],
    ['5', '6', '7', '8', '9'],
    ['_', 'A', 'B', 'C', '_'],
    ['_', '_', 'D', '_', '_'],
]

DIRS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}


def move(keypad, pos, d):
    """Returns the (x, y) coordinate after (possibly) moving."""
    new = pos + DIRS[d]

    if new.x < 0 or new.y < 0:
        return pos
    elif new.x >= len(keypad[0]) or new.y >= len(keypad):
        return pos
    elif keypad[new.y][new.x] == '_':
        return pos

    return new


pos_1 = Point(1, 1)  # start in middle
pos_2 = Point(0, 2)  # start in middle-left

code_1 = ''
code_2 = ''

for line in fileinput.input():
    for c in line.strip():
        pos_1 = move(KEYPAD_1, pos_1, c)
        pos_2 = move(KEYPAD_2, pos_2, c)

    code_1 += KEYPAD_1[pos_1.y][pos_1.x]
    code_2 += KEYPAD_2[pos_2.y][pos_2.x]

print "Theoretical bathroom code: {}".format(code_1)
print "Actual bathroom code: {}".format(code_2)
