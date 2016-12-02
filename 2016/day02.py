import fileinput

KEYPAD_1 = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

KEYPAD_2 = [
    [None, None, '1', None, None],
    [None, '2',  '3',  '4', None],
    ['5',  '6',  '7',  '8',  '9'],
    [None, 'A',  'B',  'C', None],
    [None, None, 'D', None, None],
]

DIRS = {
    'U': lambda (x, y), keypad: move(x, y, keypad,  0, -1),
    'D': lambda (x, y), keypad: move(x, y, keypad,  0,  1),
    'L': lambda (x, y), keypad: move(x, y, keypad, -1,  0),
    'R': lambda (x, y), keypad: move(x, y, keypad,  1,  0),
}


def move(x, y, keypad, d_x, d_y):
    """Returns the (x, y) coordinate after (possibly) moving"""
    new_x = x + d_x
    new_y = y + d_y

    if new_x < 0 or new_x >= len(keypad[0]):
        return (x, y)
    elif new_y < 0 or new_y >= len(keypad):
        return (x, y)
    elif keypad[y + d_y][x + d_x] is None:
        return (x, y)
    else:
        return (x + d_x, y + d_y)


pos_1 = (1, 1)  # start in middle
pos_2 = (0, 2)  # start in middle-left

code_1 = ''
code_2 = ''

for i, line in enumerate(fileinput.input()):
    for c in line.strip():
        pos_1 = DIRS[c](pos_1, KEYPAD_1)
        pos_2 = DIRS[c](pos_2, KEYPAD_2)

    code_1 += KEYPAD_1[pos_1[1]][pos_1[0]]
    code_2 += KEYPAD_2[pos_2[1]][pos_2[0]]

print "Theoretical bathroom code: {}".format(code_1)
print "Actual bathroom code: {}".format(code_2)
