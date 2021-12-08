import fileinput
from collections import OrderedDict


# Read input
data = ''.join([line for line in fileinput.input()])
groups = [g.split('\n') for g in data.split('\n\n')]

order = groups[0]
order = [int(x) for x in order[0].split(',')]

boards = groups[1:]


BOARDS = []
for b in boards:
    board = [[int(x) for x in line.split()] for line in b]
    BOARDS.append(board)

MARKS = [[[False for _ in range(5)] for _ in range(5)] for _ in range(len(BOARDS))]


def is_win(marks):
    for line in marks:
        if all(line):
            return True

    for line in zip(*marks):
        if all(line):
            return True

    return False


scores = OrderedDict()

for n in order:
    for board, marks in zip(BOARDS, MARKS):
        for y, line in enumerate(board):
            for x, val in enumerate(line):
                if n == val:
                    marks[y][x] = True

    # Check for winners
    for i, b in enumerate(MARKS):
        if is_win(b) and i not in scores:
            unmarked = 0
            for y, line in enumerate(MARKS[i]):
                for x, val in enumerate(line):
                    if not val:
                        unmarked += BOARDS[i][y][x]

            scores[i] = unmarked * n

print "Part 1:", scores.values()[0]
print "Part 2:", scores.values()[-1]
