import os, sys, re, math, copy, fileinput
from string import ascii_uppercase, ascii_lowercase
from collections import Counter, defaultdict, deque, namedtuple
from itertools import count, product, permutations, combinations, combinations_with_replacement

import advent
from utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes, resolve_mapping
from utils import chunks, gcd, lcm, print_grid, min_max_xy
from utils import new_table, transposed, rotated, firsts, lasts
from utils import md5, sha256, VOWELS, CONSONANTS
from utils import Point, DIRS, DIRS_4, DIRS_8, N, NE, E, SE, S, SW, W, NW
# Itertools Functions:
# product('ABCD', repeat=2)                   AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                     AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                     AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)    AA AB AC AD BB BC BD CC CD DD

# day  .lines  .nlines  .pars  .npars  .board  .pboard  .tboard

day = advent.Day(year=2022, day=2)

wins = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X',
}

losses = {
    'B': 'X',
    'C': 'Y',
    'A': 'Z',
}

draw = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z',
}

score = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

part_1 = 0
for line in day:
    op, us = line.split(' ')

    part_1 += score[us]
    if wins[op] == us:
        part_1 += 6
    elif losses[op] == us:
        part_1 += 0
    else:
        part_1 += 3

print("Part 1:", part_1)

part_2 = 0
for line in day:
    op, outcome = line.split(' ')
    if outcome == 'X':
        us = losses[op]
        part_2 += score[us]
    elif outcome == 'Y':
        us = draw[op]
        part_2 += score[us] + 3
    else:
        us = wins[op]
        part_2 += score[us] + 6

print("Part 2:", part_2)

