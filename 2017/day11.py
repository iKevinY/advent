import fileinput
from collections import Counter

# Represent hex coordinates in 3 dimensions
HEX_DIRS = {
    'n': (1, -1, 0),
    'ne': (1, 0, -1),
    'se': (0, 1, -1),
    's': (-1, 1, 0),
    'sw': (-1, 0, 1),
    'nw': (0, -1, 1),
}


def hex_distance(x, y, z):
    """Returns a given hex point's distance from the origin."""
    return (abs(x) + abs(y) + abs(z)) // 2


x = y = z = 0
furthest = 0

for move in fileinput.input()[0].strip().split(','):
    nx, ny, nz = HEX_DIRS[move]
    x += nx
    y += ny
    z += nz
    furthest = max(furthest, hex_distance(x, y, z))

print "Fewest steps to reach child process:", hex_distance(x, y, z)
print "Furthest distance from start:", furthest
