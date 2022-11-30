import os
import sys
import re
import math
import copy
import fileinput
from string import ascii_uppercase, ascii_lowercase
from collections import Counter, defaultdict, deque, namedtuple
from itertools import count, product, permutations, combinations, combinations_with_replacement

import advent
from utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes, resolve_mapping
from utils import chunks, gcd, lcm, print_grid, min_max_xy
from utils import new_table, transposed, rotated, firsts, lasts
from utils import md5, sha256, knot_hash
from utils import VOWELS, CONSONANTS
from utils import Point, DIRS, DIRS_4, DIRS_8  # N (0, 1) -> E (1, 0) -> S (0, -1) -> W (-1, 0)

# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

# day  .lines()  .nlines()  .paragraphs()  .board()  .pboard()  .tboard()

tot = 0
res = []

day = advent.Day(year=2022, day=1)


