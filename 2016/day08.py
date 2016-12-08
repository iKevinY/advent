import re
import fileinput
from utils import parse_line

WIDTH = 50
HEIGHT = 6
SCREEN = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

for line in fileinput.input():
    if line.startswith('rect'):
        a, b = parse_line(r'rect (\d+)x(\d+)', line)

        for y in range(b):
            for x in range(a):
                SCREEN[y][x] = True

    else:
        rc, n, offset = parse_line(r'rotate (\w+) .=(\d+) by (\d+)', line)

        if rc == 'row':
            temp = SCREEN[n][:]
            for i, x in enumerate(temp):
                SCREEN[n][(offset+i) % WIDTH] = x

        else:
            temp = [row[n] for row in SCREEN]
            for i, x in enumerate(temp):
                SCREEN[(offset+i) % HEIGHT][n] = x

print "Number of lit pixels: %i" % sum(sum(row) for row in SCREEN)

for row in SCREEN:
    print ''.join('#' if x else ' ' for x in row)
