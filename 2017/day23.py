import math
import fileinput
from collections import defaultdict


def emulate(instrs, **reg_init):
    regs = defaultdict(int)

    for k, v in reg_init.items():
        regs[k] = v

    pc = 0

    while 0 <= pc < len(instrs):
        op, x, y = instrs[pc]
        y = regs[y] if y.isalpha() else int(y)

        if op == 'set':
            regs[x] = y
        elif op == 'sub':
            regs[x] -= y
        elif op == 'mul':
            regs[x] *= y
            regs['_muls'] += 1
        elif op == 'mod':
            regs[x] %= y
        elif op == 'sqrt':
            regs[x] = int(math.sqrt(y)) + 1
        elif op == 'jnz':
            if (regs[x] if x.isalpha() else int(x)) != 0:
                pc += y
                continue

        pc += 1

    return regs


# Read puzzle input
INSTRS = []

for line in fileinput.input():
    instr = line.strip() + ' foo'
    op, x, y = instr.split()[:3]
    INSTRS.append((op, x, y))

# Part 1
print "`mul` instruction invocations:", emulate(INSTRS)['_muls']

# Part 2
#
# Perform peephole optimizations to speed up execution of Part 2
# (inspired by https://www.reddit.com/r/adventofcode/comments/7lrjei)
#
# Speed up composite check using modulo
#    set  e 2   ->  set  g b
#    set  g d   ->  mod  g d
#    mul  g e   ->  jnz  g 8
#    sub  g b   ->  set  f 0
#    jnz  g 2   ->  jnz  1 11
#    set  f 0   ->  nop
#    sub  e -1  ->  nop
#    set  g e   ->  nop
#    sub  g b   ->  nop
#    jnz  g -8  ->  nop
#
# Only check integers up to sqrt(n)
#     set  g d   ->  sqrt g b
#     sub  g b   ->  sub  g d

INSTRS[10] = ['set', 'g', 'b']
INSTRS[11] = ['mod', 'g', 'd']
INSTRS[12] = ['jnz', 'g', '8']
INSTRS[13] = ['set', 'f', '0']
INSTRS[14] = ['jnz', '1', '11']

INSTRS[21] = ['sqrt', 'g', 'b']
INSTRS[22] = ['sub', 'g', 'd']

print "Value in register h:", emulate(INSTRS, a=1)['h']
