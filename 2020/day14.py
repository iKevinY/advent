import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import copy  # NOQA
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

tot = 0
res = []
board = {}
table = new_table(None, width=2, height=4)

# Uncomment for multi-group style inputs. :c
# data = ''.join([line for line in fileinput.input()])
# groups = [g.split('\n') for g in data.split('\n\n')]

for y, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = parse_nums(line)
    data = parse_line(r'', line)

    a, b = line.split(' = ')
    # print parts

    if a == 'mask':
        res.append((None, b))
    else:
        res.append((nums[0], nums[1]))

mem = defaultdict()

mask = None

for a, b in res:
    if a is None:
        mask = b
    else:
        addr = a
        write = 0
        floats = [i for i, c in enumerate(reversed(mask)) if c == 'X']
        # print floats
        for i, c in enumerate(reversed(mask)):
            if c == '1':
                write |= (1 << i)
            elif c == '0':
                write |= (addr & (1 << i))

        writes = [write]
        print writes, floats
        for i in floats:
            new_writes = []
            for w in writes:
                print w
                new_writes.append(w & ~(1 << i))
                new_writes.append(w | (1 << i))

            print new_writes
            writes = new_writes

        print writes


        for w in writes:
            mem[w] = b

print sum(mem.values())

