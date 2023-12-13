import fileinput
from utils import memoize

@memoize
def ways(spring, groups):
    # Base cases
    if len(spring) == 0:
        if not groups:
            return 1
        else:
            return 0

    # trust_the_natural_recursion.jpg
    if spring[0] == '#':
        if not groups:
            return 0

        if any(c == '.' for c in spring[:groups[0]]):
            return 0

        if len(spring) == groups[0]:
            if len(groups) == 1:
                return 1
            else:
                return 0

        if len(spring) < groups[0]:
            return 0

        # If the character after this "group" is a `#`, we have a mismatch.
        if spring[groups[0]] == '#':
            return 0

        return ways(spring[groups[0]+1:], groups[1:])


    elif spring[0] == '.':
        return ways(spring[1:], groups)

    elif spring[0] == '?':
        return ways('#' + spring[1:], groups) + ways('.' + spring[1:], groups)


part_1 = 0
part_2 = 0

for line in fileinput.input():
    spring, groups = line.strip().split()
    groups = tuple(int(n) for n in groups.split(','))
    part_1 += ways(spring, groups)
    part_2 += ways('?'.join(spring for _ in range(5)), groups * 5)

print("Part 1:", part_1)
print("Part 2:", part_2)



