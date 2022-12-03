import advent
from utils import chunks, parts

day = advent.Day(year=2022, day=3)


# Part 1
part_1 = 0
for line in day:
    n = len(line)
    fst, snd = parts(line, 2)

    common = set(fst) & set(snd)

    for c in common:
        if c == c.lower():
            part_1 += ord(c) - ord('a') + 1
        else:
            part_1 += ord(c) - ord('A') + 27

print("Part 1:", part_1)

# Part 2
part_2 = 0
for a, b, c in chunks(day, 3):
    common = set(a) & set(b) & set(c)

    for c in common:
        if c == c.lower():
            part_2 += ord(c) - ord('a') + 1
        else:
            part_2 += ord(c) - ord('A') + 27

print("Part 2:", part_2)
