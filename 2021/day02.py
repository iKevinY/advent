import fileinput

pos = 0
aim = 0
part_1_depth = 0
part_2_depth = 0

for line in fileinput.input():
    ins, num = line.split()
    num = int(num)

    if ins == 'forward':
        pos += num
        part_2_depth += (aim * num)
    elif ins == 'down':
        part_1_depth += num
        aim += num
    elif ins == "up":
        part_1_depth -= num
        aim -= num

print "Part 1:", pos * part_1_depth
print "Part 2:", pos * part_2_depth
