import fileinput
from collections import defaultdict
from utils import parse_nums, memoize

@memoize
def resolve(r):
    if type(rules[r]) == str:
        return [rules[r]]

    matches = []
    for subrule in rules[r]:
        submatches = ['']
        for n in subrule:
            new = []
            for m in resolve(n):
                for existing in submatches:
                    new.append(existing + m)

            submatches = new

        matches.extend(submatches)

    return matches

rules = defaultdict(list)
messages = []

for line in fileinput.input():
    line = line.strip()
    nums = parse_nums(line)

    if nums:
        parts = line.split(": ")[1].split(" | ")
        r = nums[0]
        for p in parts:
            if '"' in p:
                rules[r] = p[1]
            else:
                rules[r].append([int(x) for x in p.split(' ')])

    elif line:
        messages.append(line)


pl = len(resolve(42)[0])

part_1 = 0
part_2 = 0

for line in messages:
    if line in resolve(0):
        part_1 += 1

    orig_line = line
    a = 0
    b = 0

    while line[:pl] in resolve(42):
        line = line[pl:]
        a += 1

    while line[:pl] in resolve(31):
        line = line[pl:]
        b += 1

    if a > b and b > 0 and not line:
        print orig_line
        part_2 += 1

print "Part 1:", part_1
print "Part 2:", part_2
