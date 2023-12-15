import fileinput
from utils import Point, DIRS, N, E, S, W


def transition(node, tile, dirr):
    if tile == '|':
        if dirr == N:
            return N, 1
        elif dirr == S:
            return S, 1
        else:
            return None, 0
    elif tile == '-':
        if dirr == W:
            return W, 1
        elif dirr == E:
            return E, 1
        else:
            return None, 0
    elif tile == 'L':
        if dirr == W:
            return S, 1
        elif dirr == N:
            return E, 1
    elif tile == 'J':
        if dirr == N:
            return W, 1
        elif dirr == E:
            return S, 1
        else:
            return None, 1
    elif tile == '7':
        if dirr == E:
            return N, 1
        elif dirr == S:
            return W, 1
        else:
            return None, 0
    elif tile == 'F':
        if dirr == S:
            return E, 1
        elif dirr == W:
            return N, 1
        else:
            return None, 0

    elif tile == 'S':
        return direction, 1

    return None, 0


def walk_loop(graph, start, direction):
    loop = [start]
    node = start
    while True:
        direction, good = transition(node, graph[node], direction)
        if not good:
            return None

        node += direction
        loop.append(node)

        if node == start:
            return loop



board = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        board[Point(x, y)] = c


# Solve part 1.
start = [p for p, v in board.items() if v == 'S'][0]

for direction in DIRS:
    loop = walk_loop(board, start, direction)
    if loop:
        print("Part 1:", len(loop) // 2)
        break


# TODO: Solve part 2 programmatically.
