import fileinput
from collections import deque

from utils import Point, N, E, S, W


def search(graph, start, goal):
    def gen_neighbours(node, depth):
        """Returns all valid neighbours for a given node."""
        for n in node.neighbours_4():
            if graph.get(n, ' ') == '.':
                if n not in get_blizzard_locs(depth + 1):
                    yield n

        if node not in get_blizzard_locs(depth + 1):
            yield node

    part_1 = None    
    part_2 = None

    horizon = deque([(0, 0, start)])  # priority, checkpoint, node
    seen = set()

    while horizon:
        depth, checkpoint, curr = horizon.popleft()
        
        if (depth, checkpoint, curr) in seen:
            continue

        seen.add((depth, checkpoint, curr))

        # Reached the goal for the second time after making it back to the start.
        if curr == goal and checkpoint == 2:
            part_2 = depth
            print("Part 2:", part_2)
            return part_1, part_2

        # Reached the goal for the first time.
        elif curr == goal and checkpoint == 0:
            if part_1 is None:
                part_1 = depth
                print("Part 1:", part_1)
            checkpoint = 1

        # Reached the start after touching the goal the first time.
        elif curr == start and checkpoint == 1:
            checkpoint = 2

        for n in gen_neighbours(curr, depth):
            horizon.append((depth + 1, checkpoint, n))


# N and S are swapped because of positive-Y direction convention.
MAPPING = {
    'v': N,
    '>': E,
    '^': S,
    '<': W,   
}

BLIZZARDS = {}
BLIZZARD_LOCS = {}

def get_blizzard_locs(step):
    """Returns the set of all blizzard positions for the given time step."""
    if step in BLIZZARDS:
        return BLIZZARD_LOCS[step]

    last_blizzards = BLIZZARDS[step - 1]
    new_blizzards = []
    for p, b in last_blizzards:
        np = p + MAPPING[b]
        if BOARD.get(np) == '#':
            np = p
            while BOARD.get(np) != '#':
                np -= MAPPING[b]
            np += MAPPING[b]

        new_blizzards.append((np, b))

    BLIZZARDS[step] = new_blizzards
    BLIZZARD_LOCS[step] = set(p for p, _ in new_blizzards)
    return BLIZZARD_LOCS[step]


# Read problem input.
BOARD = {}
BLIZZARDS = {0: []}
START = None
GOAL = None
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        p = Point(x, y)
        if c == '.':
            if y == 0:
                START = p
            GOAL = p
            BOARD[p] = '.'
        elif c in MAPPING:
            BLIZZARDS[0].append((p, c))
            BOARD[p] = '.'
        else:
            BOARD[p] = '#'

# Solve problem.
search(BOARD, START, GOAL)