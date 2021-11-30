import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import time  # NOQA
import fileinput
from string import ascii_uppercase, ascii_lowercase  # NOQA
from collections import Counter, defaultdict, deque, namedtuple  # NOQA
from itertools import count, product, permutations, combinations, combinations_with_replacement  # NOQA

from utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes  # NOQA
from utils import chunks, gcd, lcm, print_grid, min_max_xy  # NOQA
from utils import new_table, transposed, rotated  # NOQA
from utils import md5, sha256, knot_hash  # NOQA
from utils import VOWELS, CONSONANTS  # NOQA
from utils import Point, DIRS, DIRS_4, DIRS_8  # NOQA   # N (0, 1) -> E (1, 0) -> S (0, -1) -> W (-1, 0)

# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

TAPE = []

for line in fileinput.input():
    ins = line.split(' ')[0]
    TAPE.append([ins, parse_nums(line)])


def emulate(tape, pc=0, acc=0, debug=False):
    """Returns (acc, pc, regs, loop_detected)"""
    breakpoints = set([])
    seen = Counter()
    regs = {}
    while pc < len(tape):
        if pc in seen:
            pass
            # print "Exiting on repeat PC:", pc
            # return (acc, pc, regs, True)

        seen[pc] += 1

        ins, ops = tape[pc]
        if debug:
            if pc in breakpoints:
                print '-------'
                time.sleep(0.001)
            print "[{:04d} @ {:03d}] {} {}\t\t{}\t\t{}".format(pc, seen[pc], ins, ops, acc, regs)

        if ins == 'acc':
            acc += ops[0]
            pc += 1
        elif ins == 'jmp':
            pc += ops[0]
        elif ins == 'nop':
            pc += 1
        else:
            print "UNKNOWN OPCODE", ins
            pc += 1

    return (acc, pc, regs, False)

emulate(TAPE, debug=True)
