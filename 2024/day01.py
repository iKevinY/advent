import fileinput

lefts = []
rights = []

for line in fileinput.input():
    a, b = line.strip().split()
    lefts.append(int(a))
    rights.append(int(b))

lefts.sort()
rights.sort()

distances = 0
for l, r in zip(lefts, rights):
    distances += abs(l - r)

print("Part 1:", distances)

similarity = 0
for l in lefts:
    similarity += l * rights.count(l)

print("Part 2:", similarity)
