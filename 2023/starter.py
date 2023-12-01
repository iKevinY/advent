import os, sys, re, math, copy, fileinput
from string import ascii_uppercase, ascii_lowercase
from collections import Counter, defaultdict, deque, namedtuple
from itertools import count, product, permutations, combinations, combinations_with_replacement

import advent
from utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes, resolve_mapping
from utils import chunks, parts, gcd, lcm, print_grid, min_max_xy
from utils import new_table, transposed, rotated, firsts, lasts
from utils import md5, sha256, VOWELS, CONSONANTS
from utils import Point, DIRS, DIRS_4, DIRS_8, N, NE, E, SE, S, SW, W, NW
# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                        AB AC AD BA    BC BD CA CB    CD DA DB DC
# combinations_with_replacement('ABCD', 2)    AA AB AC AD    BB BC BD       CC CD          DD
# combinations('ABCD', 2)                        AB AC AD       BC BD          CD

# day  .lines  .nlines(negs=True)  .pars  .npars(negs=True)  .board  .pboard  .tboard

tot = 0
res = []

day = advent.Day(year=2023, day=0)

