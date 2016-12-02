import fileinput

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
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}


def move(keypad, pos, d):
    """Returns the (x, y) coordinate after (possibly) moving."""
    new_x = max(0, min(pos[0] + DIRS[d][0], len(keypad[0]) - 1))
    new_y = max(0, min(pos[1] + DIRS[d][1], len(keypad) - 1))

    if keypad[new_y][new_x] == '_':
        return pos
    else:
        return (new_x, new_y)


pos_1 = (1, 1)  # start in middle
pos_2 = (0, 2)  # start in middle-left

code_1 = ''
code_2 = ''

for i, line in enumerate(fileinput.input()):
    for c in line.strip():
        pos_1 = move(KEYPAD_1, pos_1, c)
        pos_2 = move(KEYPAD_2, pos_2, c)

    code_1 += KEYPAD_1[pos_1[1]][pos_1[0]]
    code_2 += KEYPAD_2[pos_2[1]][pos_2[0]]

print "Theoretical bathroom code: {}".format(code_1)
print "Actual bathroom code: {}".format(code_2)
