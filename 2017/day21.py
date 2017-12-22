import fileinput
from collections import Counter

from utils import new_table


def lit_pixels(grid):
    return sum(sum(c == '#' for c in row) for row in grid)


RULES = {}

for line in fileinput.input():
    rule_in, rule_out = line.strip().split(' => ')

    # Build all rule rotations and reflections
    grid = [list(x) for x in rule_in.split('/')]
    n = 2 if rule_in.count('/') == 1 else 3

    for _ in range(4):
        norm = ''.join(''.join(p) for p in grid)
        refl = ''.join(''.join(p[::-1]) for p in grid)
        RULES[norm] = RULES[refl] = rule_out.replace('/', '')

        rotated = new_table(None, width=n, height=n)

        for y in range(n):
            for x in range(n):
                rotated[y][x] = grid[n - x - 1][y]

        grid = rotated

SUBGRIDS = Counter()
SUBGRIDS['.#...####'] += 1

for it in range(18):
    # Build up our list of subgrids
    if it % 3 == 0:
        GRIDS = []
        ORIG_GRIDS = []
        for inp in SUBGRIDS:
            GRIDS.append([list(inp[n:n+3]) for n in range(0, 9, 3)])
            ORIG_GRIDS.append(inp)

    NEW_GRIDS = []
    for grid in GRIDS:
        size = len(grid)
        d = 2 if size % 2 == 0 else 3

        new_size = (size // d) * (d + 1)
        new_grid = new_table(None, width=new_size, height=new_size)

        for y in range(size // d):
            for x in range(size // d):
                # Build the string representation of each 2x2 or 3x3 subgrid
                subgrid = ''

                for k in range(d):
                    subgrid += ''.join(grid[y*d + k][x*d:(x+1)*d])

                # Lookup the corresponding rule and populate the new grid
                out = RULES[subgrid]
                for ny in range(d+1):
                    for nx in range(d+1):
                        new_grid[y*(d+1) + ny][x*(d+1) + nx] = out[ny*(d+1) + nx]

        NEW_GRIDS.append(new_grid)

    GRIDS = NEW_GRIDS

    if it in (4, 17):
        num_pixels = sum(lit_pixels(g) * SUBGRIDS[ORIG_GRIDS[i]] for i, g in enumerate(GRIDS))
        print "Lit pixels after {} iterations:".format(it + 1), num_pixels

    # Update the count of independent 3x3 subgrids
    if it % 3 == 2:
        next_subgrids = Counter()
        for i, grid in enumerate(GRIDS):
            mult = SUBGRIDS[ORIG_GRIDS[i]]
            for y in range(0, 9, 3):
                for x in range(0, 9, 3):
                    key = ''.join(
                        ''.join(grid[y+n][x:x+3])
                        for n in range(3)
                    )
                    next_subgrids[key] += mult

        SUBGRIDS = next_subgrids
