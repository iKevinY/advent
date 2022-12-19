import fileinput
from utils import Point, N, S, E, W


ROCKS = [
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)],
    [Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)],
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)],
    [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)],
 ]


pattern = fileinput.input()[0].strip()
lcm = len(pattern) * len(ROCKS)

def simulate(target_rocks, key_height=10):
    tower_hats = {}
    curr_rock = None

    move_num = 0
    rocks = 0
    height = 0
    bonus_height = 0

    chamber = {Point(x, 0): "#" for x in range(7)}

    while rocks < target_rocks:
        if curr_rock is None:
            # Check for a cycle.
            if rocks % lcm == 0 and bonus_height == 0:
                key = ''
                for y in range(key_height):
                    key += ''.join(chamber.get(Point(x, height - y), ".") for x in range(7))
                    key += '\n'

                # Jump forward because we found a cycle, then finish up the simulation.
                if key in tower_hats:
                    last_height, last_rocks = tower_hats[key]

                    # Deltas from the last time we saw the hat.
                    cycle_height = height - last_height
                    cycle_rocks = rocks - last_rocks

                    # Safe to jump forward this many cycles.
                    n_cycles = (target_rocks - rocks) // cycle_rocks

                    # Store how much extra height we gained implicitly,
                    # otherwise future pieces will spawn way too high
                    # compared to the state of the chamber.
                    bonus_height += n_cycles * cycle_height
                    rocks += n_cycles * cycle_rocks

                else:
                    tower_hats[key] = (height, rocks)

            # Spawn new rock.
            curr_rock = [p + N * (height + 4) + (E * 2) for p in ROCKS[rocks % len(ROCKS)]]


        # Try to move the falling rock based on the jet of gas.
        if pattern[move_num % len(pattern)] == '>':
            # Does the right wall block us?
            if any(p.x >= 6 for p in curr_rock):
                pass
            # Does another rock at rest block us?
            elif any(p + E in chamber for p in curr_rock):
                pass
            else:
                curr_rock = [p + E for p in curr_rock]
        else:
            if any(p.x <= 0 for p in curr_rock):
                pass
            elif any(p + W in chamber for p in curr_rock):
                pass
            else:
                curr_rock = [p + W for p in curr_rock]

        # Do we come to rest?
        if any(chamber.get(p + S) == '#' for p in curr_rock):
            for r in curr_rock:
                chamber[r] = "#"
                height = max(height, r.y)

            curr_rock = None
            rocks += 1

        else:
            curr_rock = [r + S for r in curr_rock]

        move_num += 1

    return height + bonus_height

print("Part 1:", simulate(2022))
print("Part 2:", simulate(1_000_000_000_000, key_height=16))  # 18 good
