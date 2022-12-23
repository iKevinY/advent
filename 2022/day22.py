import re, fileinput

from utils import min_max_xy
from utils import firsts, lasts
from utils import Point, DIRS


# Read problem input.
graph = {}
in_maze = True
start = None
for y, line in enumerate(fileinput.input()):
    if not line.strip():
        in_maze = False
    if in_maze:
        for x, c in enumerate(line.strip("\n")):
            if c != ' ':
                if start is None and c == '.':
                    start = Point(x, -y)
                graph[Point(x, -y)] = c
    else:
        instructions = re.findall(r'(\d+|[LR])', line)


def wrapped_links(graph):
    """Compute link dictionary for part 1."""
    links = {}
    min_x, max_x, min_y, max_y = min_max_xy(list(graph.keys()))

    # Construct the left-to-right wrap-around links.
    for y in range(min_y, max_y + 1):
        first = None
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            if first is None and p in graph:
                first = p
            elif p in graph:
                last = p

        links[last, 1] = (first, 1)
        links[first, 3] = (last, 3)

    # Construct the top-to-bottom wrap-around links.
    for x in range(min_x, max_x + 1):
        first = None
        for y in range(min_y, max_y + 1):
            p = Point(x, y)
            if first is None and p in graph:
                first = p
            elif p in graph:
                last = p

        links[last, 0] = (first, 0)
        links[first, 2] = (last, 2)

    return links


def cube_links():
    """
    This works specifically for my cube, which is shaped as follows:

      1122
      1122
      33
      33
    4455
    4455
    66
    66

    """
    links = {}

    # Define 2D arrays representing the 6 different faces of the cube, as numbered
    # above, in the orientation given by the problem input.
    FS = 50
    f1 = [[Point(x, -y) for x in range(FS*1, FS*2)] for y in range(FS*0, FS*1)]
    f2 = [[Point(x, -y) for x in range(FS*2, FS*3)] for y in range(FS*0, FS*1)]
    f3 = [[Point(x, -y) for x in range(FS*1, FS*2)] for y in range(FS*1, FS*2)]
    f4 = [[Point(x, -y) for x in range(FS*0, FS*1)] for y in range(FS*2, FS*3)]
    f5 = [[Point(x, -y) for x in range(FS*1, FS*2)] for y in range(FS*2, FS*3)]
    f6 = [[Point(x, -y) for x in range(FS*0, FS*1)] for y in range(FS*3, FS*4)]

    # "Glue together" the appropriate edges of each of the face pairs that will
    # be touching when the cube is formed. The "facing" direction changes depending
    # on which direction you're coming into the point from.
    for p, np in zip(f1[0], reversed(firsts(f6))):
        links[(p, 0)] = (np, 1)
        links[(np, 3)] = (p, 2)

    for p, np in zip(firsts(f1), reversed(firsts(f4))):
        links[(p, 3)] = (np, 1)
        links[(np, 3)] = (p, 1)

    for p, np in zip(f2[0], f6[-1]):
        links[(p, 0)] = (np, 0)
        links[(np, 2)] = (p, 2)

    for p, np in zip(reversed(lasts(f2)), lasts(f5)):
        links[(p, 1)] = (np, 3)
        links[(np, 1)] = (p, 3)

    for p, np in zip(f2[-1], reversed(lasts(f3))):
        links[(p, 2)] = (np, 3)
        links[(np, 1)] = (p, 0)

    for p, np in zip(firsts(f3), reversed(f4[0])):
        links[(p, 3)] = (np, 2)
        links[(np, 0)] = (p, 1)

    for p, np in zip(f5[-1], reversed(lasts(f6))):
        links[(p, 2)] = (np, 3)
        links[(np, 1)] = (p, 0)

    return links


def simulate(graph, start, instructions, links):
    pos = start
    dir = 1
    for ins in instructions:
        # Turn clockwise or counterclockwise.
        if not ins.isnumeric():
            if ins == 'L':
                dir = (dir - 1) % 4
            else:
                dir = (dir + 1) % 4
            continue

        # Move some number of steps (or stop at a wall).
        for _ in range(int(ins)):
            np = pos + DIRS[dir]

            # Bump into a wall, stop going forward.
            if graph.get(np) == '#':
                break
            elif graph.get(np) == '.':
                pos = np
                continue
            else:
                # We need to wrap around to another spot. The link mapping
                # tells us what the new position is, and what our new facing is.
                np, nf = links[pos, dir]

                if graph.get(np) == '#':
                    break
                elif graph.get(np) == '.':
                    pos = np
                    dir = nf
                    continue

    row = -pos.y + 1
    col = pos.x + 1
    facing = (dir - 1) % 4

    return (1000 * row) + (4 * col) + facing

print("Part 1:", simulate(graph, start, instructions, wrapped_links(graph)))
print("Part 2:", simulate(graph, start, instructions, cube_links()))
