import fileinput
from collections import defaultdict, deque

from utils import Point, DIRS, N, S, E, W


def process_plot(garden, start, visited):
    """
    Walk through the garden using BFS from `start`, only
    visiting the same plant as present in `garden[start]`.

    Write seen locations back to `visited` so that we can
    keep track of which garden plots have already been seen.

    Returns the area, perimeter, and side count of the plot.
    """
    plot = set()
    horizon = deque([start])
    plant = garden.get(start)

    while horizon:
        node = horizon.popleft()
        if node in plot:
            continue

        plot.add(node)
        visited.add(node)

        for n in node.neighbours():
            if n in garden and garden.get(n) == plant:
                horizon.append(n)

    # The area of the plot is simply how many locations we visited.
    area = len(plot)

    # Compute the perimeter by taking every plant location in the
    # plot, and counting how many neighbouring locations are *not*
    # also in the plot. Each of those locations contributes 1 unit
    # length to the overall perimeter of the plot.
    perimeter = sum(len(set(p.neighbours()) - plot) for p in plot)

    # Compute the number of sides. This one is a bit tricky.

    # Walk every row in the garden. For each position that is part
    # of this plot, look to see if there is a non-plot location above
    # and below it (similar to the perimeter calculation). Add this
    # to a set of "potential sides". We will need to eliminate extra
    # sides in a future step.
    row_sides = {
        N: defaultdict(set),
        S: defaultdict(set),
    }
    for y in range(-2, 150):
        for d in [N, S]:
            for x in range(-2, 150):
                p = Point(x, y)
                if p in plot and p + d not in plot:
                    row_sides[d][y].add(p)

    # Do the same for every column in the garden, looking left/right.
    col_sides = {
        E: defaultdict(set),
        W: defaultdict(set)
    }

    for x in range(-2, 150):
        for d in [E, W]:
            for y in range(-2, 150):
                p = Point(x, y)
                if p in plot and p + d not in plot:
                    col_sides[d][x].add(p)

    # Do another horizonal/vertical sweep of the garden. When we
    # "enter" a position that is part of a "side", increment the
    # side count. Continue to walk until we are not in that side
    # anymore. At this point, the polygon has turned or something,
    # or we might be passing over a "break" (imagine walking down
    # the horizontal legs of the letter "E" vertically). Don't start
    # counting another side until we reach an in-plot location again.
    sides = 0

    for d in [N, S]:
        for y in range(-2, 150):
            x = -2
            inside = False
            while x < 150:
                p = Point(x, y)
                if p in row_sides[d][y]:
                    if not inside:
                        sides += 1
                        inside = True
                else:
                    if inside:
                        inside = False

                x += 1

    for d in [E, W]:
        for x in range(-2, 150):
            y = -2
            inside = False
            while y < 150:
                p = Point(x, y)
                if p in col_sides[d][x]:
                    if not inside:
                        sides += 1
                        inside = True
                else:
                    if inside:
                        # print("exit inside")
                        inside = False

                y += 1

    return area, perimeter, sides


# Parse problem input.
GARDEN = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        GARDEN[Point(x, y)] = c

# Solve problem.
part_1 = 0
part_2 = 0
visited = set()

for pos in GARDEN:
    if pos not in visited:
        area, perim, sides = process_plot(GARDEN, pos, visited)
        part_1 += area * perim
        part_2 += area * sides

print("Part 1:", part_1)
print("Part 2:", part_2)
