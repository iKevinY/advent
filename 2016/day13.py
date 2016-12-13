import fileinput

INPUT = int(fileinput.input()[0])


def is_open(x, y, seed=INPUT):
    """Open space if number of 1 bits is even, else wall."""
    num = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + seed
    return bin(num)[2:].count('1') % 2 == 0


def pathfind(a, b, c, d, max_steps=None):
    """
    Returns length of the shortest path from (a, b) to (c, d)
    and the number of visited locations along the way.
    """

    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    horizon = [(a, b)]
    seen = set()
    steps = 0

    while horizon:
        new_horizon = []
        for x, y in horizon:
            if x == c and y == d:
                return steps, len(seen)

            seen.add((x, y))

            for dx, dy in deltas:
                nx, ny = x + dx, y + dy
                if is_open(nx, ny) and nx >= 0 and ny >= 0 and (nx, ny) not in seen:
                    new_horizon.append((nx, ny))

        if steps == max_steps:
            break

        horizon = new_horizon
        steps += 1

    return steps, len(seen)


print "Fewest steps to reach 31, 39 from 1, 1:", pathfind(1, 1, 31, 39)[0]
print "Distinct locations reached in 50 steps:", pathfind(1, 1, -1, -1, max_steps=50)[1]
