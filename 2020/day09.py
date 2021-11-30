import fileinput
from itertools import permutations

SEQ = [int(x) for x in fileinput.input()]
LEN = 25

for i in range(LEN, len(SEQ)):
    for x, y in permutations(SEQ[i-LEN:i], 2):
        if x + y == SEQ[i]:
            break
    else:
        INVALID = SEQ[i]
        print "Part 1:", INVALID
        break

for n in range(2, len(SEQ)):
    tot = 0
    for i in range(len(SEQ)-n):
        tot = sum(SEQ[i:i+n])
        if tot == INVALID:
            print "Part 2:", min(SEQ[i:i+n]) + max(SEQ[i:i+n])

