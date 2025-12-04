import fileinput
from functools import cache


@cache
def dp(s, n):
    """Dynamic program to get the max joltage of a string."""
    if n == 1:
        return max(s)

    poss = []
    for i in range(len(s) - n + 1):
        poss.append(s[i] + dp(s[i+1:], n - 1))

    return max(poss)


PART_1 = 0
PART_2 = 0

for bank in fileinput.input():
    bank = bank.strip()
    PART_1 += int(dp(bank, 2))
    PART_2 += int(dp(bank, 12))

print("Part 1:", PART_1)
print("Part 2:", PART_2)

