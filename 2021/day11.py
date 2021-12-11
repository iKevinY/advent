import copy
import fileinput
from utils import Point

board = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        board[Point(x, y)] = int(c)


part_1 = 0

for i in range(10000000):
    next_state = copy.copy(board)

    for pos, val in next_state.items():
        next_state[pos] = val + 1

    flashed = set()
    while True: # when steady state
        updated = False

        for pos, val in next_state.items():
            # Flash!
            if next_state[pos] > 9 and pos not in flashed:
                # Increment all 8 neighbours
                for n in pos.neighbours_8():
                    if n not in next_state:
                        continue

                    next_state[n] = next_state[n] + 1

                flashed.add(pos)
                part_1 += 1
                updated = True

        if not updated:
            break

    if len(flashed) == len(next_state):
        print "Part 2:", i + 1
        break

    # Reset all >9s to 0
    for pos, val in next_state.items():
        if val > 9:
            next_state[pos] = 0

    board = next_state

    if i == 99:
        print "Part 1:", part_1
