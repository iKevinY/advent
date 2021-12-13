import fileinput
from utils import print_grid, Point


DOTS = {}
FOLDS = []


# Read problem input
data = ''.join([line for line in fileinput.input()])
groups = [g.split('\n') for g in data.split('\n\n')]

for line in groups[0]:
    x, y = [int(x) for x in line.split(',')]
    DOTS[Point(x, y)] = '#'

for line in groups[1]:
    axis, n = line.split()[2].split('=')
    FOLDS.append((axis, int(n)))

for i, (axis, n) in enumerate(FOLDS):
    new_dots = {}

    for p in DOTS:
        if axis == 'x':
            if p.x < n:
                new_dots[p] = '#'
            else:
                dx = abs(n - p.x)
                nx = n - dx
                new_dots[Point(nx, p.y)] = '#'
        else:
            if p.y < n:
                new_dots[p] = '#'
            else:
                dy = abs(n - p.y)
                ny = n - dy
                new_dots[Point(p.x, ny)] = '#'

    DOTS = new_dots

    if i == 0:
        print "Part 1:", len(DOTS)

print "Part 2:\n", '\n'.join(print_grid(DOTS, quiet=True))
