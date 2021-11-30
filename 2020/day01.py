import fileinput

nums = [int(x) for x in fileinput.input()]

part_1 = None
part_2 = None

for m in nums:
    for n in nums:
        for o in nums:
            if m + n == 2020:
                part_1 = m * n
            elif m + n + o == 2020:
                part_2 = m * n * o

print "Part 1:", part_1
print "Part 2:", part_2
