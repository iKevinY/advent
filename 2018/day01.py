import sys
import fileinput
from itertools import count

FREQ = 0
SEEN = set([0])
TAPE = []

for line in fileinput.input():
    TAPE.append(int(line))

for i in count():
    for n in TAPE:
        FREQ += n
        if FREQ in SEEN:
            print "First duplicate frequency:", FREQ
            sys.exit()
        else:
            SEEN.add(FREQ)

    if i == 0:
        print "First resulting frequency:", FREQ
