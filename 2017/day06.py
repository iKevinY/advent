import fileinput
from itertools import count

banks = [int(n) for n in fileinput.input()[0].split()]
seen = {}

for i in count(start=1):
    m = max(banks)
    idx = banks.index(m)
    banks[idx] = 0

    for j in range(1, m + 1):
        banks[(idx + j) % len(banks)] += 1

    t = tuple(banks)
    if t in seen:
        break

    seen[t] = i

print "Number of redistribution cycles:", i
print "Length of infinite loop cycle:", i - seen[t]
