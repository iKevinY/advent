import math
import fileinput
from itertools import permutations
from collections import Counter, defaultdict
from utils import mul, print_grid, transposed, rotated


TILES = defaultdict(list)

# Read problem input
for line in fileinput.input():
    if line.startswith('Tile'):
        id = int(line.replace(':', '').split(' ')[1])
    elif len(line) > 5:
        TILES[id].append(line.strip())


# Map edges to pieces that share that edge
piece_edges = defaultdict(set)

for id, tile in TILES.items():
    for _ in range(4):
        row = ''.join(tile[0])
        piece_edges[row].add(id)
        piece_edges[row[::-1]].add(id)
        tile = rotated(tile)


# Construct graph of neighbouring pieces
graph = defaultdict(set)

for neighbouring_pieces in piece_edges.values():
    for x, y in permutations(neighbouring_pieces, 2):
        graph[x].add(y)


# Corners are the only pieces that neighbour exactly 2 other tiles.
corners = [tile for tile, neighs in graph.items() if len(neighs) == 2]
print "Corner ID product:", mul(corners)
print


# Build up the full arrangement of the tiles. Arbitrarily pick
# a corner to be the top-left, and assign its neighbours.
puzzle = {}
puzzle[0, 0] = corners[0]


# Let `m` represent the m by m arrangement of tiles.
m = int(math.sqrt(len(TILES)))


# Assign tiles for the top row and left column by choosing from the subset
# of tiles that contain either 2 or 3 neighbours (ie. edges and corners).
# Make sure to not reuse tiles since that ruins this algorithm.
edges = [tile for tile, neighs in graph.items() if len(neighs) == 3]

for x in range(1, m):
    for tile in edges + corners:
        if tile in graph[puzzle[x - 1, 0]] and tile not in puzzle.values():
            puzzle[x, 0] = tile

for y in range(1, m):
    for tile in edges + corners:
        if tile in graph[puzzle[0, y - 1]] and tile not in puzzle.values():
            puzzle[0, y] = tile


# Now assign the remaining tiles. Since the previous tiles were already filled
# in, we can check the left and top neighbour for every candidate location,
# which will uniquely match a single tile's neighbour list.
for y in range(1, m):
    for x in range(1, m):
        for tile, neighbours in graph.items():
            left = puzzle[x - 1, y]
            top = puzzle[x, y - 1]

            if left in neighbours and top in neighbours and tile not in puzzle.values():
                puzzle[x, y] = tile

print "Resolved piece arrangement:"
for y in range(m):
    print ' '.join(str(puzzle[x, y]) for x in range(m))
print


# Now we need to actually orient all the pieces. Let `PUZZLE` be a dictionary
# that maps tile locations to 2D arrays representing the pieces themselves.
PUZZLE = {pos: TILES[id] for pos, id in puzzle.items()}


# Define some helper functions for manipulating tiles.
def orientations(tile):
    """Generates all 8 orientations of a 2D array."""
    for _ in range(2):
        for _ in range(4):
            yield tile
            tile = rotated(tile)

        tile = transposed(tile)

def aligned(a, b):
    """Returns if the final row or col of `a` matches the first row or col of `b`"""
    return (
        ''.join(a[-1]) == ''.join(b[0]) or
        ''.join(transposed(a)[-1]) == ''.join(transposed(b)[0])
    )


# We need to get the top-left corner into an orientation where its bottom and
# right edges match the neighbours based on the arrangement we determined above.
for tile in orientations(PUZZLE[0, 0]):
    bottom = ''.join(tile[-1])
    right = ''.join(transposed(tile)[-1])

    if puzzle[0, 1] in piece_edges[bottom] and puzzle[1, 0] in piece_edges[right]:
        PUZZLE[0, 0] = tile
        break


# Align remaining tiles by matching them up via their top and left edges, if present.
for y in range(m):
    for x in range(m):
        if x == 0 and y == 0:
            continue

        for tile in orientations(PUZZLE[x, y]):
            if (x == 0 or aligned(PUZZLE[x - 1, y], tile)) and (y == 0 or aligned(PUZZLE[x, y - 1], tile)):
                PUZZLE[x, y] = tile
                break


# Process the puzzle to form the image (removing borders of tiles).
# Store as 2D array instead of dictionary so we can re-orient it.
IMG = [[None for _ in range(8 * m)] for _ in range(8 * m)]
for (x, y), tile in PUZZLE.items():
    for j in range(8):
        for i in range(8):
            IMG[y*8 + j][x*8 + i] = tile[j + 1][i + 1]


# Get the offset positions for the sea monster components.
MONSTER = """\
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""

m_pos = []
for y, row in enumerate(MONSTER.split('\n')):
    for x, c in enumerate(row):
        if c == '#':
            m_pos.append((x, y))


# Search for sea monsters!
for image in orientations(IMG):
    occupied = set()
    for y in range(m * 8 - max(y for x, y in m_pos)):
        for x in range(m * 8 - max(x for x, y in m_pos)):
            if all(image[y+j][x+i] == '#' for i, j in m_pos):
                for i, j in m_pos:
                    occupied.add((x+i, y+j))

    if occupied:
        final_img = {}
        for y in range(m * 8):
            for x in range(m * 8):
                if image[y][x] == '#':
                    final_img[x, y] = 'O' if (x, y) in occupied else '~'

        print_grid(final_img)
        print "\nWater roughness:", sum(1 for c in final_img.values() if c == '~')
