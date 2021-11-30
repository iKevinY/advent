import fileinput
from collections import Counter
from utils import memoize

NUMS = [int(x) for x in fileinput.input()]

NUMS.append(0)
NUMS.append(max(NUMS) + 3)
NUMS.sort()

deltas = Counter()
curr = 0

for n in NUMS:
    deltas[n - curr] += 1
    curr = n

print "Part 1:", deltas[1] * deltas[3]


@memoize
def dp(i):
    if i >= len(NUMS) - 1:
        return 1

    ways = 0

    if i + 1 < len(NUMS) and NUMS[i + 1] - NUMS[i] <= 3:
        ways += dp(i + 1)

    if i + 2 < len(NUMS) and NUMS[i + 2] - NUMS[i] <= 3:
        ways += dp(i + 2)

    if i + 3 < len(NUMS) and NUMS[i + 3] - NUMS[i] <= 3:
        ways += dp(i + 3)

    return ways

print "Part 2:", dp(0)
