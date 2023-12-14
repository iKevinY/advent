import copy
import fileinput

from utils import Point, N, S, E, W


# Parse problem input.
BOARD = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        BOARD[Point(x, y)] = c

WIDTH = x + 1
HEIGHT = y + 1


def tilt(board, direction):
    if direction == N:
        for y in range(1, HEIGHT):
            for x in range(WIDTH):
                p = Point(x, y)
                if board[p] != 'O':
                    continue

                while p.y > 0:
                    np = p + S
                    if board[np] == '.':
                        board[p] = '.'
                        board[np] = 'O'
                    else:
                        break
                    p = np

    elif direction == S:
        for y in reversed(range(HEIGHT - 1)):
            for x in range(WIDTH):
                p = Point(x, y)
                if board[p] != 'O':
                    continue

                while p.y < HEIGHT - 1:
                    np = p + N
                    if board[np] == '.':
                        board[p] = '.'
                        board[np] = 'O'
                    else:
                        break
                    p = np

    elif direction == E:
        for x in reversed(range(WIDTH)):
            for y in range(HEIGHT):
                p = Point(x, y)
                if board[p] != 'O':
                    continue

                while p.x < WIDTH - 1:
                    np = p + E
                    if board[np] == '.':
                        board[p] = '.'
                        board[np] = 'O'
                    else:
                        break
                    p = np

    elif direction == W:
        for x in range(1, WIDTH):
            for y in range(HEIGHT):
                p = Point(x, y)
                if board[p] != 'O':
                    continue

                while p.x > 0:
                    np = p + W
                    if board[np] == '.':
                        board[p] = '.'
                        board[np] = 'O'
                    else:
                        break
                    p = np


def spin_cycle(board):
    for x in [N, W, S, E]:
        tilt(board, x)


def total_load(board):
    return sum(HEIGHT - p.y for p, c in board.items() if c == 'O')


def serialize(board):
    s = ''
    for y in range(HEIGHT):
        for x in range(WIDTH):
            s += board[Point(x, y)]

    return s


# Solve part 1.
part_1_board = copy.deepcopy(BOARD)
tilt(part_1_board, N)
print("Part 1:", total_load(part_1_board))


# Detect cycle length.
board_states = {}

c = 1
while True:
    spin_cycle(BOARD)

    s = serialize(BOARD)
    if s in board_states:
        cycle_len = c - board_states[s]
        print(f"Determined period = {cycle_len} on iteration {c}.")
        break
    else:
        board_states[s] = c

    c += 1

# Simulate further ahead to work out part 2 answer.
while c % cycle_len != 1000000000 % cycle_len:
    spin_cycle(BOARD)
    c += 1

print("Part 2:", total_load(BOARD))

