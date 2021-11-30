import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import copy  # NOQA
import fileinput
from collections import Counter, defaultdict, deque, namedtuple  # NOQA

from utils import parse_nums, mul, print_grid, transposed, rotated, Point, new_table

tot = 0
res = []
board = new_table('.', width=10, height=10)

tiles = {}
curr = 0
sy = 0

MONSTER = """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""

for y, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = parse_nums(line)

    if not line:
        tiles[curr] = copy.deepcopy(board)
        board = new_table('.', width=10, height=10)

    if nums:
        curr = nums[0]
        sy = y
        continue

    for x, c in enumerate(line):
        board[y - sy - 1][x] = c

tiles[curr] = copy.deepcopy(board)

edges = Counter()
piece_edges = defaultdict(set)

# find edges:
for id, t in tiles.items():
    x = copy.deepcopy(t)
    for _ in range(4):
        row = ''.join(x[0])
        edges[row] += 1
        edges[row[::-1]] += 1
        piece_edges[row].add(id)
        piece_edges[row[::-1]].add(id)
        x = rotated(x)

# for c in edges.most_common():
#     print c

cands = []

for id, tile in tiles.items():
    ones = 0
    for _ in range(4):
        row = ''.join(x[0])
        if edges.get(row) == 1:
            ones += 1
        if edges.get(row[::-1]) == 1:
            ones += 1
        x = rotated(x)

    if ones >= 1:
        cands.append(id)

    # print ones

graph = defaultdict(set)

for p, e in piece_edges.items():
    # print p, e
    for x in e:
        for y in e:
            graph[x].add(y)
            graph[y].add(x)


tot = 1
corners = []
for k, v in graph.items():
    # print k, v
    if len(v) == 3:
        corners.append(k)
        # print k
        tot *= k

# print tot

puzzle = {}
x = 0
y = 0

start = corners[0]
puzzle[0, 0] = start
o = [i for i in graph[start] if i != start]
puzzle[0, 1] = o[0]
puzzle[1, 0] = o[1]



m = int(math.sqrt(len(tiles)))
x = 2
y = 2

while x < m:
    for k, v in graph.items():
        if x == m - 1:
            if len(v) == 3 and k in graph[puzzle[x - 1, 0]] and k not in puzzle.values():
                puzzle[x, 0] = k
                x += 1
                break
        else:
            if len(v) == 4 and k in graph[puzzle[x - 1, 0]] and k not in puzzle.values():
                puzzle[x, 0] = k
                x += 1
                break

while y < m:
    for k, v in graph.items():
        if y == m - 1:
            if len(v) == 3 and k in graph[puzzle[0, y - 1]] and k not in puzzle.values():
                puzzle[0, y] = k
                y += 1
                break
        else:
            if len(v) == 4 and k in graph[puzzle[0, y - 1]] and k not in puzzle.values():
                puzzle[0, y] = k
                y += 1
                break

# print puzzle


for y in range(1, m):
    for x in range(1, m):
        # print x, y
        for k, v in graph.items():
            # print k, v, puzzle.get((x, y - 1)), puzzle.get((x - 1, y))
            if puzzle.get((x, y - 1)) in v and puzzle.get((x - 1, y)) in v and k not in puzzle.values():
                puzzle[x, y] = k

assert len(puzzle) == len(tiles)

print "Piece arrangement:"
for y in range(m):
    print ' '.join(str(puzzle[x, y]) for x in range(m))
print

PUZZLE = {}

for y in range(m):
    for x in range(m):
        PUZZLE[x, y] = tiles[puzzle[x, y]]

row = ''.join(PUZZLE[0, 0][-1])
col = ''.join(transposed(PUZZLE[0, 0])[-1])

# print row, piece_edges[row]
# print col, piece_edges[col]

for _ in range(2):
    for _ in range(4):
        row = ''.join(PUZZLE[0, 0][-1])
        col = ''.join(transposed(PUZZLE[0, 0])[-1])
        # print_grid(PUZZLE[0, 0])
        # print
        if puzzle[0, 1] in piece_edges[row] and puzzle[1, 0] in piece_edges[col]:
            # print "good"
            break

        PUZZLE[0, 0] = rotated(PUZZLE[0, 0])

    else:
        PUZZLE[0, 0] = transposed(PUZZLE[0, 0])
        continue

    break

# print puzzle[0, 0], puzzle[0, 1], puzzle[1, 0]
# print_grid(PUZZLE[0, 0])

# x, 0
for x in range(1, m):
    for _ in range(2):
        for _ in range(4):
            row = ''.join(transposed(PUZZLE[x, 0])[0])
            # print "trying", row
            if row == ''.join(transposed(PUZZLE[x - 1, 0])[-1]):
                # print "good for x=", x
                # print_grid(PUZZLE[x, 0])
                break

            PUZZLE[x, 0] = rotated(PUZZLE[x, 0])

        else:
            PUZZLE[x, 0] = transposed(PUZZLE[x, 0])
            continue

        break

    else:
        print "no match for", x

# y, 0
for y in range(1, m):
    for _ in range(2):
        for _ in range(4):
            row = ''.join(PUZZLE[0, y][0])
            # print "trying", row
            if row == ''.join(PUZZLE[0, y - 1][-1]):
                # print "good for y=", y
                # print_grid(PUZZLE[0, y])
                break

            PUZZLE[0, y] = rotated(PUZZLE[0, y])

        else:
            PUZZLE[0, y] = transposed(PUZZLE[0, y])
            continue

        break

    else:
        print "no match for", y


for y in range(1, m):
    for x in range(1, m):
        for _ in range(2):
            for _ in range(4):
                col = ''.join(transposed(PUZZLE[x, y])[0])
                row = ''.join(PUZZLE[x, y][0])

                ocol = ''.join(transposed(PUZZLE[x - 1, y])[-1])
                orow = ''.join(PUZZLE[x, y - 1][-1])
                if row == orow and col == ocol:
                    # print "good for {}, {}".format(x, y)
                    # print_grid(PUZZLE[x, y])
                    break

                PUZZLE[x, y] = rotated(PUZZLE[x, y])

            else:
                PUZZLE[x, y] = transposed(PUZZLE[x, y])
                continue

            break

        else:
            print "no match for", x, y

monster = [[None for _ in range(8 * m)] for _ in range(8 * m)]

for y in range(m):
    for x in range(m):
        for j in range(8):
            for i in range(8):
                # print x, y, i, j
                monster[y*8 + j][x*8 + i] = PUZZLE[x, y][j + 1][i + 1]


MONSTER = []
MONSTER.append("                  # ")
MONSTER.append("#    ##    ##    ###")
MONSTER.append(" #  #  #  #  #  #   ")

minds = []

mx = 20
my = 3
for y in range(len(MONSTER)):
    for x, c in enumerate(MONSTER[y]):
        if c == '#':
            minds.append((x, y))

# print minds

for _ in range(2):
    monster = rotated(monster)

# print_grid(monster)

for _ in range(2):
    for _ in range(4):
        m_count = 0
        occupied = set()
        for y in range(len(monster) - my):
            for x in range(len(monster[0]) - mx):
                if all(monster[y+j][x+i] == '#' for i, j in minds):
                    # print "monster!"
                    m_count += 1

                    for i, j in minds:
                        occupied.add((x+i, y+j))

        if m_count > 1:
            # print m_count, occupied
            final_monster = {}
            tot = 0
            for y in range(m * 8):
                for x in range(m * 8):
                    p = Point(x, y)
                    if monster[y][x] == '#':
                        if (x, y) not in occupied:
                            tot += 1
                            final_monster[p] = '~'
                        else:
                            final_monster[p] = 'O'

                    else:
                        final_monster[p] = ' '

            print_grid(final_monster)
            print
            print "Water roughness:", tot

        monster = rotated(monster)

    monster = transposed(monster)

