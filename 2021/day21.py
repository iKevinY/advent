import fileinput
from collections import Counter
from itertools import product

from utils import parse_nums


# Read problem input.
start_pos = {}
for line in fileinput.input():
    nums = parse_nums(line)
    start_pos[nums[0]] = nums[1]


# Solve part 1.
curr_die = 1
total_rolls = 0

p1_score = 0
p2_score = 0

p1 = start_pos[1]
p2 = start_pos[2]

while p1_score < 1000 and p2_score < 1000:
    p1 -= 1
    for i in range(3):
        total_rolls += 1
        p1 += curr_die
        curr_die += 1
        if curr_die == 101:
            curr_die = 1
    p1 = p1 % 10
    p1 += 1

    p1_score += p1

    if p1_score >= 1000:
        break

    p2 -= 1
    for i in range(3):
        total_rolls += 1
        p2 += curr_die
        curr_die += 1
        if curr_die == 101:
            curr_die = 1
    p2 = p2 % 10
    p2 += 1

    p2_score += p2

print "Part 1:", total_rolls * min(p1_score, p2_score)


# Solve part 2.

# All possible roll totals of the quantum dice for a given turn.
rolls = [sum(p) for p in product([1, 2, 3], repeat=3)]

p1 = start_pos[1]
p2 = start_pos[2]

# Each universe is represented by (p1_pos, p2_pos, p1_score, p2_score).
universes = Counter([(p1, p2, 0, 0)])

while not all(s1 >= 21 or s2 >= 21 for p1, p2, s1, s2 in universes):
    next_universes = Counter()
    for (p1, p2, s1, s2), count in universes.items():
        if s1 >= 21 or s2 >= 21:
            next_universes[p1, p2, s1, s2] += count
            continue

        for r in rolls:
            np = (((p1 + r) - 1) % 10) + 1
            next_universes[(np, p2, s1 + np, s2)] += count

    universes = next_universes

    next_universes = Counter()
    for (p1, p2, s1, s2), count in universes.items():
        if s1 >= 21 or s2 >= 21:
            next_universes[p1, p2, s1, s2] += count
            continue

        for r in rolls:
            np = (((p2 + r) - 1) % 10) + 1
            next_universes[(p1, np, s1, s2 + np)] += count

    universes = next_universes

p1_wins = 0
p2_wins = 0

for (p1, p2, s1, s2), v in universes.items():
    if s1 >= 21:
        p1_wins += v
    else:
        p2_wins += v

print "Part 2:", max(p1_wins, p2_wins)
