import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import fileinput
from itertools import product, permutations, combinations, combinations_with_replacement  # NOQA

from utils import mul, factors, memoize, primes, Point  # NOQA

# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

for i, line in enumerate(fileinput.input()):
    pass
