import fileinput


part_1 = 0
part_2 = 0

for line in fileinput.input():
    elf_1, elf_2 = line.strip().split(',')
    a, b = [int(x) for x in elf_1.split('-')]
    c, d = [int(x) for x in elf_2.split('-')]

    # Part 1
    if a <= c <= b and a <= d <= b:
        part_1 += 1
    elif c <= a <= d and c <= b <= d:
        part_1 += 1


    # Part 2
    if a <= c <= b or a <= d <= b:
        part_2 += 1
    elif c <= a <= d or c <= b <= d:
        part_2 += 1

print("Part 1:", part_1)
print("Part 2:", part_2)
