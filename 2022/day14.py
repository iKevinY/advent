import copy
import fileinput

from utils import parse_nums, chunks
from utils import Point, N, NE, NW


# Parse input.
max_y = 0
traces = []
for line in fileinput.input():
    nums = parse_nums(line)
    trace = []
    for x, y in chunks(nums, 2):
        trace.append(Point(x, y))
        max_y = max(max_y, y)
    traces.append(trace)


# Fill in the board with all the rock locations.
board = {}
for trace in traces:
    last = trace[0]
    for nxt in trace[1:]:
        if last.x == nxt.x:
            for y in range(min(last.y, nxt.y), max(last.y, nxt.y) + 1):
                board[Point(last.x, y)] = "#"
        else:
            for x in range(min(last.x, nxt.x), max(last.x, nxt.x) + 1):
                board[Point(x, last.y)] = "#"

        last = nxt


def simulate(board, floor=100000000):
    board = copy.deepcopy(board)
    sand = source
    while True:
        if sand.y > 10000:
            return board

        # Inverted directions because this problem uses "+Y is down" convention.
        if board.get(sand + N, '.') not in ("#", "o") and sand.y + 1 < floor:
            sand += N
            continue
        elif board.get(sand + NW, '.') not in ("#", "o") and sand.y + 1 < floor:
            sand += NW
            continue
        elif board.get(sand + NE, '.') not in ("#", "o") and sand.y + 1 < floor:
            sand += NE
            continue
        elif sand == source:
            board[sand] = "o"
            return board
        else:
            board[sand] = "o"
            sand = source


source = Point(500, 0)
board[source] = "+"

part_1_board = simulate(board)
print("Part 1:", sum(1 for v in part_1_board.values() if v == "o"))

part_2_board = simulate(board, floor=(max_y + 2))
print("Part 2:", sum(1 for v in part_2_board.values() if v == "o"))
