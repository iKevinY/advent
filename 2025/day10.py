import fileinput
from collections import defaultdict

from z3 import Int, Optimize


def solve(goal, toggles, part_2=False):
    s = Optimize()

    # Create z3 variables for each "light" (light/counter).
    lights = [Int('j' + str(i)) for i, g in enumerate(goal)]

    # Create z3 variables to count each button press.
    buttons = [Int('t' + str(i)) for i in range(len(toggles))]

    # Count instances of indicator light appearing in toggle.
    appearances = defaultdict(list)
    for i, toggle in enumerate(toggles):
        for t in toggle:
            appearances[t].append(i)

    # Add constraints for `counter == sum of buttons pressed`.
    for i, ts in appearances.items():
        s.add(lights[int(i)] == sum(buttons[x] for x in ts))

    # Enforce non-negative numbers of button presses.
    for b in buttons:
        s.add(b >= 0)

    # Add constraints depending on if we're solving part 1 or 2.
    for i, g in enumerate(goal):
        if part_2:
            s.add(lights[i] == g)
        else:
            # We just care about parity in part 1.
            s.add(lights[i] % 2 == g)

    # Minimize the total number of button presses.
    s.minimize(sum(buttons))

    # Answer is the sum of button presses from the solver.
    s.check()
    m = s.model()
    return sum(m[b].as_long() for b in buttons)


part_1 = 0
part_2 = 0
for line in fileinput.input():
    parts = line.strip().split()
    lights, *toggles, joltage = parts

    toggles = [t[1:-1].split(',') for t in toggles]
    p1_goal = [1 if c == '#' else 0 for c in lights[1:-1]]
    p2_goal = [int(x) for x in joltage[1:-1].split(',')]

    part_1 += solve(p1_goal, toggles)
    part_2 += solve(p2_goal, toggles, part_2=True)

print("Part 1:", part_1)
print("Part 2:", part_2)
