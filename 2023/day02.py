import fileinput
from collections import Counter

from utils import mul

PART_1_LIMITS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

part_1 = 0
part_2 = 0

for line in fileinput.input():
    game, log = line.strip().split(': ')
    game_id = int(game[5:])

    part_1_poss = True
    part_2_mins = Counter()

    for turn in log.split('; '):
        for entry in turn.split(', '):
            n, color = entry.split(' ')
            n = int(n)
            if n > PART_1_LIMITS[color]:
                part_1_poss = False
            part_2_mins[color] = max(part_2_mins[color], n)

    if part_1_poss:
        part_1 += game_id

    part_2 += mul(part_2_mins.values())

print("Part 1:", part_1)
print("Part 2:", part_2)
