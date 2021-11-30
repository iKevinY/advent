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
    nums = [int(x) for x in line.split(',')]

    for x, c in enumerate(line):
        board[Point(x, y)] = c

    if y == 0:
        print(data)

print nums



seen = defaultdict(list)

for i, n in enumerate(nums):
    seen[n].append(i)

print seen

spoken = nums[-1]
i = len(nums)

while True:
    # print spoken, i
    if len(seen[spoken]) == 1:
        new_spoke = 0
    else:
        new_spoke = i - seen[spoken][-2] - 1

    # print "newspoke", new_spoke

    spoken = new_spoke
    seen[spoken].append(i)

    i += 1
    if i == 30000000:
        break

print spoken


