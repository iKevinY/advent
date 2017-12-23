import math
import fileinput
from collections import defaultdict

from utils import parse_line, mul, all_unique, factors, memoize, primes  # NOQA

INSTRS = []
B = None

# Read puzzle input
for line in fileinput.input():
    instr = line.strip() + ' foo'
    op, x, y = instr.split()[:3]
    INSTRS.append((op, x, y))

    if fileinput.isfirstline():
        B = int(y)

# Part 1
REGS = defaultdict(int)
pc = 0
muls = 0

while 0 <= pc < len(INSTRS):
    op, x, y = INSTRS[pc]
    y = REGS[y] if y.isalpha() else int(y)

    if op == 'set':
        REGS[x] = y
    elif op == 'sub':
        REGS[x] -= y
    elif op == 'mul':
        REGS[x] *= y
        muls += 1
    elif op == 'mod':
        REGS[x] %= y
    elif op == 'jnz':
        if (REGS[x] if x.isalpha() else int(x)) != 0:
            pc += y
            continue

    pc += 1

print "`mul` instruction invocations:", muls

# Part 2
b = (B * 100) + 100000
c = b + 17000
h = 0

for n in range(b, c + 1, 17):
    for i in range(2, int(math.sqrt(n))):
        if n % i == 0:
            h += 1
            break

print "Value in register h, ie. primes in [{}, {}]: {}".format(b, c, h)
