import fileinput

def fuel(n):
    return (n // 3) - 2

PART_1 = 0
PART_2 = 0

for line in fileinput.input():
    n = int(line)
    PART_1 += fuel(n)
    while fuel(n) > 0:
        n = fuel(n)
        PART_2 += n

print "Total fuel for Part 1:", PART_1
print "Total fuel for Part 2:", PART_2
