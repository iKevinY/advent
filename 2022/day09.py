import fileinput
from utils import Point


def sign(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0


def update(head, tail):
    """
    Given the current position of head and tail,
    return the new tail position.
    """

    # This occurs if we have moved diagonally away from the tail,
    # and it is far enough for the tail to come and chase us.
    if abs(head.x - tail.x) + abs(head.y - tail.y) > 2:
        tail += Point(sign(head.x, tail.x), sign(head.y, tail.y))

    # Check if we need to move horizontally/vertically.
    elif (head.x == tail.x or head.y == tail.y) and (abs(head.x - tail.x) + abs(head.y - tail.y) > 1):
        tail += Point(sign(head.x, tail.x), sign(head.y, tail.y))

    return tail


mapping = {
    "U": Point(0, 1),
    "R": Point(1, 0),
    "D": Point(0, -1),
    "L": Point(-1, 0),
}

INSTRUCTIONS = [line.strip() for line in fileinput.input()]

# Solve problem.
for part, bridge_len in ((1, 2), (2, 10)):
    bridge = [Point(0, 0) for _ in range(bridge_len)]
    seen = set()

    for line in INSTRUCTIONS:
        d, amt = line.split()
        amt = int(amt)

        for _ in range(amt):
            # First, move the head in the given direction.
            bridge[0] += mapping[d]
            for i in range(1, bridge_len):
                bridge[i] = update(bridge[i-1], bridge[i])
            seen.add(bridge[-1])

    print(f"Part {part}: {len(seen)}")

