import fileinput
from collections import Counter
from itertools import zip_longest

SNAFU_DIGITS = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
REVERSE_DIGITS = {v: k for k, v in SNAFU_DIGITS.items()}


# Read problem input and solve problem.
nums = [line.strip() for line in fileinput.input()]
remainder = Counter()
part_1 = ''

for i, place in enumerate(zip_longest(*(reversed(n) for n in nums), fillvalue='0')):
    count = sum(SNAFU_DIGITS[c] for c in place) + remainder[i]
    while not -2 <= count <= 2:
        if count < 0:
            remainder[i+1] -= 1
            count += 5
        else:
            remainder[i+1] += 1
            count -= 5

    part_1 = REVERSE_DIGITS[count] + part_1

print("Part 1:", part_1)
