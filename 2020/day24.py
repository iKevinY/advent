import fileinput
from collections import defaultdict

HEX_DIRS = {
    'e': (1, -1, 0),
    'ne': (1, 0, -1),
    'se': (0, -1, 1),
    'w': (-1, 1, 0),
    'sw': (-1, 0, 1),
    'nw': (0, 1, -1),
}

def hex_neighbours(x, y, z):
    for dx, dy, dz in HEX_DIRS.values():
        yield x + dx, y + dy, z + dz


TILES = defaultdict(bool)

for line in fileinput.input():
    x = 0
    y = 0
    z = 0
    curr = ''

    for c in line:
        curr += c
        if curr in HEX_DIRS:
            dx, dy, dz = HEX_DIRS[curr]
            x += dx
            y += dy
            z += dz
            curr = ''

    TILES[x, y, z] = not TILES[x, y, z]

print "Part 1:", sum(TILES.values())

for day in range(1, 100 + 1):
    new_tiles = defaultdict(bool)

    for old_pos in TILES.keys():
        for pos in hex_neighbours(*old_pos):
            neighs = 0
            for n in hex_neighbours(*pos):
                if TILES[n]:
                    neighs += 1

            if TILES[pos] and (neighs == 0 or neighs > 2):
                pass
            elif not TILES[pos] and neighs == 2:
                new_tiles[pos] = True
            else:
                if TILES[pos]:
                    new_tiles[pos] = True

    TILES = new_tiles

print "Part 2:", sum(TILES.values())



