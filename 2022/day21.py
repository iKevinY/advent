import copy
import fileinput
from collections import defaultdict

from utils import topsort


GRAPH = defaultdict(set)
YELLS = {}

for line in fileinput.input():
    monkey, rest = line.strip().split(': ')
    if rest.isnumeric():
        YELLS[monkey] = int(rest)
    else:
        d1, op, d2 = rest.split(' ')
        YELLS[monkey] = (d1, op, d2)
        GRAPH[monkey].add(d1)
        GRAPH[monkey].add(d2)

ORDERING = list(reversed(topsort(GRAPH)))


def simulate(yells, humn=None):
    if humn:
        yells['humn'] = humn
        d1, _, d2 = yells['root']
        yells['root'] = (d1, "==", d2)

    for monkey in ORDERING:
        if type(yells[monkey]) != int:
            d1, op, d2 = yells[monkey]
            yells[monkey] = eval(f"{yells[d1]} {op} {yells[d2]}")

    return int(yells['root'])


print("Part 1:", simulate(copy.deepcopy(YELLS)))

# For my problem input, we analyze some values of the two monkeys that
# the `root` monkey depends on, and how it changes depends on `humn`.
#
#   humn=3 d1=72750855862944 d2=31522134274080
#   humn=8 d1=72750855862880 d2=31522134274080
#
# When `humn` increases by 5, `d1` decreases by 64, and `d2` is constant.
# Therefore, we need to solve the following equation:
#
#   humn = 3 + (72750855862944 - 31522134274080) * (5 / 64)
#        = 3220993874133

HUMN = 3220993874133
part_2 = simulate(copy.deepcopy(YELLS), humn=HUMN); assert part_2 == 1
print("Part 2:", HUMN)


