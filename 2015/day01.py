import fileinput

floor = 0
basement = None

for line in fileinput.input():
    for i, char in enumerate(line, start=1):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1

        if floor == -1 and basement is None:
            basement = i

print "Santa's floor: %d" % floor
print "Entered basement at character %d" % basement
