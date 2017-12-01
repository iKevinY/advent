import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import fileinput
from collections import Counter, deque, namedtuple  # NOQA
from itertools import count, product, permutations, combinations, combinations_with_replacement  # NOQA

from utils import (parse_line, mul, factors, memoize, primes, new_table, md5, sha256  # NOQA
    Point, DIRS, DIRS_4, DIRS_8)  # NOQA

# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

total = 0
result = []
table = new_table(None, width=2, height=4)

for i, line in enumerate(fileinput.input()):
    line = line.strip()

    # data = [x for x in line.split(', ')]
    # data = [x for x in line]
    # data = [int(x) for x in line.split()]
    # data = re.findall(r'(\w+)', line)
    data = parse_line(r'', line)

    if i == 0:
        print(data)
