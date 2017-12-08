import fileinput
from collections import defaultdict

REGS = defaultdict(int)
HIGHEST_VAL = 0

for line in fileinput.input():
    a, op, x, _, b, eq, y = line.strip().split()

    if eval('REGS["{}"] {} {}'.format(b, eq, y)):
        REGS[a] += int(x) * (1 if op == 'inc' else -1)
        HIGHEST_VAL = max(HIGHEST_VAL, REGS[a])

print "Largest value in any register:", max(REGS.values())
print "Highest value held in registers:", HIGHEST_VAL
