import fileinput


readings = [int(line) for line in fileinput.input()]

part_1 = 0
part_2 = 0


for i in range(1, len(readings)):
    if readings[i] > readings[i-1]:
        part_1 += 1

for i in range(3, len(readings)):
    if readings[i] > readings[i-3]:
        part_2 += 1


print "Part 1:", part_1
print "Part 2:", part_2
