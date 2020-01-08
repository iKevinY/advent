import fileinput

from intcode import emulate
from utils import Point


# Read problem input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]


# Part 1
vm = emulate(TAPE[:], [])
board = []

try:
    while True:
        resp = next(vm)
        board.append(chr(resp))
except StopIteration:
    pass

signal = [a for a in ''.join(board).split()]

height = len(signal)
width = len(signal[0])

grid = {}

for y in range(height):
    for x in range(width):
        grid[Point(x, y)] = signal[y][x]
        if signal[y][x] == '^':
            START = Point(x, y)

alignment = 0
for p in grid:
    if grid.get(p, ' ') != '#':
        continue

    for np in p.neighbours_4():
        if grid.get(np, ' ') != '#':
            break
    else:
        alignment += p.x * p.y

print "Sum of alignment parameters:", alignment


# Part 2
main = "A,B,A,C,A,B,C,B,C,B"
fn_a = "L,10,R,8,L,6,R,6"
fn_b = "L,8,L,8,R,8"
fn_c = "R,8,L,6,L,10,L,10"
camera = "n"

instructions = []
for ins in (main, fn_a, fn_b, fn_c, camera):
    for c in ins:
        instructions.append(ord(c))
    instructions.append(ord('\n'))

TAPE[0] = 2
for c in emulate(TAPE[:], instructions[::-1]):
    try:
        print chr(c),
    except Exception:
        print "Dust collected:", c
