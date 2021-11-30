import os  # NOQA
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import copy  # NOQA
import fileinput
from string import ascii_uppercase, ascii_lowercase  # NOQA
from heapq import heappush, heappop, heapify
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
table = new_table(None, width=2, height=4)
graph = {}

# Uncomment for multi-group style inputs. :c
# data = ''.join([line for line in fileinput.input()])
# groups = [g.split('\n') for g in data.split('\n\n')]

for i, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = parse_nums(line)
    data = parse_line(r'', line)

    for j, c in enumerate(line):
        graph[Point(j, i)] = c

    res.append(line)

    if i == 0:
        print(data)

max_x = len(res[0])
max_y = len(res)

print graph
print res

state = graph

while True:
    new_state = {}

    for y in range(max_y):
        for x in range(max_x):
            p = Point(x, y)
            occ = 0
            # for n in p.neighbours_8():
            #     if state.get(n, '.') == '#':
            #         occ += 1

            for d in DIRS_8:
                np = p + d
                # np = p
                while 0 <= np.x < max_x and 0 <= np.y < max_y:
                    if state.get(np, '.') == '.':
                        np += d
                        # break
                    elif state.get(np, '.') == '#':
                        occ += 1
                        break
                    else:
                        break


            if state[p] == 'L' and occ == 0:
                new_state[p] = '#'

            elif state[p] == '#' and occ >= 5:
                new_state[p] = 'L'

            else:
                new_state[p] = state[p]



    a = ''
    b = ''
    for y in range(max_y):
        for x in range(max_x):
            p = Point(x, y)
            # print state[p],
            a += state[p]
            b += new_state[p]

        # print

    # print
    # print

    if a == b:
        tot = 0
        for y in range(max_y):
            for x in range(max_x):
                if new_state[Point(x, y)] == '#':
                    tot += 1

        print tot

        break


    state = new_state


