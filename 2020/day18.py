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
    line = line.strip().replace(' ', '')
    nums = parse_nums(line)
    data = parse_line(r'', line)

    for x, c in enumerate(line):
        board[Point(x, y)] = c

    if y == 0:
        print(data)

    res.append(line)

print tot

NUMS = '0123456789'


def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def is_name(str):
    return re.match("\w+", str)

def peek(stack):
    return stack[-1] if stack else None

def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    values.append(eval("{0}{1}{2}".format(left, operator, right)))

def greater_precedence(op1, op2):
    precedences = {'+' : 1, '-' : 0, '*' : 0, '/' : 0}
    return precedences[op1] > precedences[op2]

def evaluate(expression):
    tokens = re.findall("[+/*()-]|\d+", expression)
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)

    return values[0]


for line in res:
    a = evaluate(line)
    print a, '=', line
    tot += a

print tot
