import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import fileinput
from collections import Counter  # NOQA
from itertools import product, permutations, combinations, combinations_with_replacement  # NOQA

from utils import parse_line, mul, factors, memoize, primes, Point  # NOQA

# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

total = 0
result = []

for i, line in enumerate(fileinput.input()):
    line = line.strip()

    # data = [x for x in line.split(', ')]
    # data = [x for x in line]
    # data = [int(x) for x in line.split()]
    data = parse_line(line, r'')

    if i == 0:
        print(data)
