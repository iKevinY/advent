import fileinput


CRABS = [int(x) for x in fileinput.input()[0].split(',')]

part_1 = part_2 = 10000000000000

for pos in range(max(CRABS) + 1):
    part_1_fuel = 0
    part_2_fuel = 0

    for c in CRABS:
        part_1_fuel += abs(pos - c)

        delta = abs(pos - c)
        part_2_fuel += ((delta + 1) * delta) // 2

    part_1 = min(part_1, part_1_fuel)
    part_2 = min(part_2, part_2_fuel)

print "Part 1:", part_1
print "Part 2:", part_2
