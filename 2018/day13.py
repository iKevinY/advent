import fileinput


DIRS = {
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3,
}

SLASH = {
    '>': '^',
    'v': '<',
    '<': 'v',
    '^': '>',
}

BACKSLASH = {
    '>': 'v',
    'v': '>',
    '<': '^',
    '^': '<',
}

CARTS = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^',
}

DELTAS = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1),
}

grid = []
carts = {}

for y, line in enumerate(fileinput.input()):
    line = line.replace('\n', '')
    row = []
    for x, t in enumerate(line):
        if t in DIRS:
            carts[(x, y)] = (t, 0)
            row.append('|' if t in ['v', '^'] else '-')
        else:
            row.append(t)

    grid.append(row)

part_1 = False

while len(carts) > 1:
    new_carts = {}
    crashed = set()
    cart_pos = set(carts.keys())

    for (x, y), (c, t) in sorted(carts.items(), key=lambda x: x[0]):
        if (x, y) in crashed:
            continue

        d = DIRS[c]
        dx, dy = DELTAS[c]
        nx, ny = x + dx, y + dy

        if grid[ny][nx] == '\\':
            c = BACKSLASH[c]
        elif grid[ny][nx] == '/':
            c = SLASH[c]
        elif grid[ny][nx] == '+':
            c = CARTS[(d + ((t % 3) - 1)) % 4]
            t += 1

        if (nx, ny) in cart_pos:
            if not part_1:
                print "Location of first crash: {},{}".format(nx, ny)
                part_1 = True

            crashed.add((nx, ny))
        else:
            cart_pos.remove((x, y))
            cart_pos.add((nx, ny))
            new_carts[nx, ny] = (c, t)

    carts = {x: y for x, y in new_carts.items() if x not in crashed}

print "Location of last cart: {},{}".format(*carts.keys()[0])
