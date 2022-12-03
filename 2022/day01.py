import fileinput

elves = []
elf = 0
for line in fileinput.input():
    if line.strip():
        elf += int(line)
    else:
        # New line -> new elf.
        elves.append(elf)
        elf = 0

elves.append(elf)

print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves)[-3:]))
