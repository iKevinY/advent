import advent

day = advent.Day(year=2022, day=1)
elves = [sum(e) for e in day.nparagraphs]

print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves)[-3:]))
