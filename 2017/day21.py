import fileinput
from utils import new_table


def lit_pixels(grid):
    return sum(sum(c == '#' for c in row) for row in grid)


GRID = [
    ['.', '#', '.'],
    ['.', '.', '#'],
    ['#', '#', '#'],
]

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

for i in range(18):
    size = len(GRID[0])
    d = 2 if size % 2 == 0 else 3

    new_size = (size // d) * (d + 1)
    new_grid = new_table(None, width=new_size, height=new_size)

    for y in range(size // d):
        for x in range(size // d):
            # Build the string representation of each 2x2 or 3x3 subgrid
            subgrid = ''

            for k in range(d):
                subgrid += ''.join(GRID[y*d + k][x*d:(x+1)*d])

            # Lookup the corresponding rule and populate the new grid
            out = RULES[subgrid]
            for ny in range(d+1):
                for nx in range(d+1):
                    new_grid[y*(d+1) + ny][x*(d+1) + nx] = out[ny*(d+1) + nx]

    GRID = new_grid

    if i == 4:
        print "Lit pixels after 5 iterations:", lit_pixels(GRID)

print "Lit pixels after 18 iterations:", lit_pixels(GRID)
