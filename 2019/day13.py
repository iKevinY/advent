import fileinput
from collections import Counter

from intcode import emulate


# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000
TAPE[0] = 2

inputs = [0]
game = emulate(TAPE, inputs)
grid = {}
ball_x = 0
padd_x = 0
score = None

try:
    while True:
        x = next(game)
        y = next(game)
        n = next(game)

        # Score output
        if x == -1 and y == 0:
            if score is None:
                print "Blocks at start of game:", Counter(grid.values())[2]
            score = n
        else:
            grid[x, y] = n
            if n == 3:
                padd_x = x
            elif n == 4:
                ball_x = x

        if ball_x < padd_x:
            inputs[0] = -1
        elif ball_x > padd_x:
            inputs[0] = 1
        else:
            inputs[0] = 0

except StopIteration:
    print "Score after last block is broken:", score
