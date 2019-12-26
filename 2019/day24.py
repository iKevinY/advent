import fileinput
from utils import Point


def solve_part_1(board):
    def serialize(board):
        res = ''
        for y in range(5):
            res += ''.join(board[Point(x, y)] for x in range(5))
        return res

    def diversity_score(board):
        return sum(2 ** i if c == '#' else 0 for i, c in enumerate(serialize(board)))

    seen = set()

    while True:
        new_board = {}
        for p in board:
            count = 0
            for np in p.neighbours_4():
                if board.get(np, '.') == '#':
                    count += 1

            if board.get(p, '.') == '#':
                new_board[p] = '#' if count == 1 else '.'
            else:
                new_board[p] = '#' if count == 1 or count == 2 else '.'

        if serialize(new_board) in seen:
            return diversity_score(new_board)

        seen.add(serialize(new_board))
        board = new_board


def solve_part_2(board):
    def recursive_neighbours(x, y, z):
        for np in Point(x, y).neighbours_4():
            if np.x == 2 and np.y == 2:
                for i in range(5):
                    if x == 1:
                        yield (0, i, z + 1)
                    elif x == 3:
                        yield (4, i, z + 1)
                    elif y == 1:
                        yield (i, 0, z + 1)
                    elif y == 3:
                        yield (i, 4, z + 1)
            elif np.x == -1:
                yield (1, 2, z - 1)
            elif np.x == 5:
                yield (3, 2, z - 1)
            elif np.y == -1:
                yield (2, 1, z - 1)
            elif np.y == 5:
                yield (2, 3, z - 1)
            else:
                yield (np.x, np.y, z)


    for minutes in range(200):
        new_board = {}

        for z in range(-(minutes + 1), minutes + 2):
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue

                    count = 0
                    for nx, ny, nz in recursive_neighbours(x, y, z):
                        if board.get((nx, ny, nz), '.') == '#':
                            count += 1

                    if board.get((x, y, z), '.') == '#':
                        new_board[(x, y, z)] = '#' if count == 1 else '.'
                    else:
                        new_board[(x, y, z)] = '#' if count == 1 or count == 2 else '.'

        board = new_board

    return board.values().count('#')


# Read problem input
PART_1 = {}
PART_2 = {}

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        PART_1[Point(x, y)] = c
        if not (x == 2 and y == 2):
            PART_2[(x, y, 0)] = c

print "Biodiversity rating for first repeated layout:", solve_part_1(PART_1)
print "Bugs in recursive space after 200 minutes:", solve_part_2(PART_2)
