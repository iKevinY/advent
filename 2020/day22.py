import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import copy  # NOQA
import fileinput
from string import ascii_uppercase, ascii_lowercase  # NOQA
from collections import Counter, defaultdict, deque, namedtuple  # NOQA
from itertools import count, product, permutations, combinations, combinations_with_replacement  # NOQA

from utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes, resolve_mapping  # NOQA
from utils import chunks, gcd, lcm, print_grid, min_max_xy  # NOQA
from utils import new_table, transposed, rotated  # NOQA
from utils import md5, sha256, knot_hash  # NOQA
from utils import VOWELS, CONSONANTS  # NOQA
from utils import Point, DIRS, DIRS_4, DIRS_8  # NOQA   # N (0, 1) -> E (1, 0) -> S (0, -1) -> W (-1, 0)

tot = 0
res = []
board = {}
table = new_table(None, width=2, height=4)

p1 = deque()
p2 = deque()

is1 = True

for y, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = parse_nums(line)
    data = parse_line(r'', line)

    if ':' in line:
        continue

    if not line:
        is1 = False

    if nums:
        if is1:
            p1.append(nums[0])
        else:
            p2.append(nums[0])


def serialize(p1, p2):
    a = ','.join(str(x) for x in p1)
    b = ','.join(str(x) for x in p2)
    return a + '~' + b

SEEN = set()

depth = 0

@memoize
def combat(p1, p2):
    # print "triggered new combat", p1, p2
    while p1 and p2:
        state = serialize(p1, p2)
        if state in SEEN:
            return p1, True

        SEEN.add(state)

        a = p1.popleft()
        b = p2.popleft()

        if len(p1) >= a and len(p2) >= b:
            # print "triggering combat for", a, b
            p1_win = combat(deque(list(p1)[:a]), deque(list(p2)[:b]))[1]
        else:
            p1_win = a > b

        if p1_win:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)

    return p1 if p1 else p2, True if p1 else False


deck, winner = combat(p1, p2)
print deck, winner


ans = 0
for i, a in enumerate(reversed(deck), start = 1):
    ans += i * a

print ans
