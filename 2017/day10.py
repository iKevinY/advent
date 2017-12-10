import fileinput


def knot_hash(elems, lengths, pos=0, skip=0):
    for l in lengths:
        for i in range(l // 2):
            x = (pos + i) % len(elems)
            y = (pos + l - i - 1) % len(elems)
            elems[x], elems[y] = elems[y], elems[x]

        pos = pos + l + skip % len(elems)
        skip += 1

    return elems, pos, skip


# Read puzzle input
line = fileinput.input()[0].strip()

# Part 1
try:
    lengths = [int(x) for x in line.split(',')]
    elems = knot_hash(range(0, 256), lengths)[0]
    print "Product of first two items in list:", elems[0] * elems[1]
except ValueError:
    print "Skipping part 1 (can't parse puzzle input into ints)"

# Part 2
lengths = [ord(x) for x in line] + [17, 31, 73, 47, 23]
elems = range(0, 256)
pos = 0
skip = 0

# Perform 64 rounds of Knot Hash
for _ in range(64):
    elems, pos, skip = knot_hash(elems, lengths, pos, skip)

# Convert from sparse hash to dense hash
sparse = elems
dense = []

for i in range(16):
    res = 0
    for j in range(0, 16):
        res ^= sparse[(i * 16) + j]

    dense.append(res)

print "Knot Hash of puzzle input:", ''.join('%02x' % x for x in dense)
