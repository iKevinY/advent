import fileinput
from utils import Point


def knot_hash(msg):
    lengths = [ord(x) for x in msg] + [17, 31, 73, 47, 23]
    sparse = range(0, 256)
    pos = 0
    skip = 0

    for _ in range(64):
        for l in lengths:
            for i in range(l // 2):
                x = (pos + i) % len(sparse)
                y = (pos + l - i - 1) % len(sparse)
                sparse[x], sparse[y] = sparse[y], sparse[x]

            pos = pos + l + skip % len(sparse)
            skip += 1

    sparse = sparse
    dense = []

    for i in range(16):
        res = 0
        for j in range(0, 16):
            res ^= sparse[(i * 16) + j]

        dense.append(res)

    return ''.join('%02x' % x for x in dense)


KEY_STRING = fileinput.input()[0].strip()
DISK = set()

for x in range(128):
    hash_hex = knot_hash(KEY_STRING + '-' + str(x))
    hash_bits = ''.join('{0:04b}'.format(int(x, 16)) for x in hash_hex)
    for y, b in enumerate(hash_bits):
        if b == '1':
            DISK.add(Point(x, y))

regions = 0
seen = set()

for p in DISK:
    if p in seen:
        continue

    queue = [p]
    while queue:
        np = queue.pop()
        seen.add(np)
        for n in np.neighbours_4():
            if n in DISK and n not in seen:
                queue.append(n)

    regions += 1

print "Number of used squares:", len(DISK)
print "Number of regions:", regions
