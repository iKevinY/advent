import fileinput
from collections import Counter

BOXES = [line.strip() for line in fileinput.input()]

DOUBLES = 0
TRIPLES = 0
COMMON = None

for box_1 in BOXES:
    doubles = 0
    triples = 0

    for char, count in Counter(box_1).items():
        if count == 2:
            doubles += 1
        elif count == 3:
            triples += 1

    if doubles > 0:
        DOUBLES += 1

    if triples > 0:
        TRIPLES += 1

    for box_2 in BOXES:
        if box_1 == box_2:
            continue

        diffs = 0

        for i in range(len(box_1)):
            if box_1[i] != box_2[i]:
                diffs += 1

        if diffs == 1:
            COMMON = ''.join(a for a, b in zip(box_1, box_2) if a == b)


print "Checksum for list of box IDs:", DOUBLES * TRIPLES
print "Common letters for right IDs:", COMMON
