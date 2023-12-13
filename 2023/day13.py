import fileinput
from utils import transposed


def find_reflections(pattern):
    """Returns all possible reflections for pattern."""
    sols = []

    # First try solving as-is, then transpose for vertical reflections.
    for multiplier in [100, 1]:
        for y in range(len(pattern) - 1):
            bad = False
            for a, b in zip(reversed(pattern[:y+1]), pattern[y+1:]):
                if a != b:
                    bad = True
                    break

            if not bad:
                sols.append((y + 1) * multiplier)

        pattern = transposed(pattern)

    return sols


def unsmudge(pattern, reflection):
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            cell = pattern[y][x]
            pattern[y][x] = '.' if cell == '#' else '#'

            for new_reflection in find_reflections(pattern):
                if new_reflection != reflection:
                    return new_reflection

            pattern[y][x] = cell


part_1 = 0
part_2 = 0

for pattern in ''.join(fileinput.input()).split('\n\n'):
    pattern = [list(x) for x in pattern.splitlines()]

    reflection = solve(pattern)[0]
    part_1 += reflection
    part_2 += unsmudge(pattern, reflection)

print("Part 1:", part_1)
print("Part 2:", part_2)

