import fileinput

lefts = []
rights = []

for line in fileinput.input():
    a, b = line.strip().split()
    lefts.append(int(a))
    rights.append(int(b))

lefts.sort()
rights.sort()

print("Part 1:", sum(abs(l - r) for l, r in zip(lefts, rights)))
print("Part 2:", sum(l * rights.count(l) for l in lefts))
