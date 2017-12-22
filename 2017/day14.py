import fileinput
from utils import Point, knot_hash


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
