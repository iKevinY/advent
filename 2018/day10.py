import fileinput
from copy import deepcopy
from itertools import count

from utils import parse_nums

INF = 1e9


def simulate(points, seconds=None):
    best_x = INF
    best_y = INF

    if seconds:
        loop = range(seconds)
    else:
        loop = count()

    for tick in loop:
        min_x = INF
        max_x = -INF
        min_y = INF
        max_y = -INF

        for i, (x, y, dx, dy) in enumerate(points):
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

            points[i][0] += dx
            points[i][1] += dy

        diff_x = max_x - min_x
        diff_y = max_y - min_y

        improved = False

        if diff_x < best_x:
            best_x = diff_x
            improved = True
        if diff_y < best_y:
            best_y = diff_y
            improved = True

        if not improved:
            return tick - 1


POINTS = []

for line in fileinput.input():
    x, y, dx, dy = parse_nums(line)
    POINTS.append([x, y, dx, dy])


points = deepcopy(POINTS)
seconds_to_message = simulate(points)
simulate(POINTS, seconds=seconds_to_message)


points = {(x, y) for x, y, dx, dy in POINTS}
xs, ys = zip(*points)
min_x, max_x = sorted(xs)[0], sorted(xs)[-1]
min_y, max_y = sorted(ys)[0], sorted(ys)[-1]

for y in range(min_y, max_y + 1):
    print ''.join('#' if (x, y) in points else '.' for x in range(min_x, max_x + 1))

print "Seconds until the above message is formed:", seconds_to_message
