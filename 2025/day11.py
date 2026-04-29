import fileinput
from collections import defaultdict
from functools import cache


@cache
def ways(start, end):
    if start == end:
        return 1

    return sum(ways(n, end) for n in GRAPH[start])

# Read problem input.
GRAPH = defaultdict(set)
for line in fileinput.input():
    node, other = line.strip().split(': ')
    for b in other.split():
        GRAPH[node].add(b)

# Solve problem.
print("Part 1:", ways('you', 'out'))
print("Part 2:", ways('svr', 'fft') * ways('fft', 'dac') * ways('dac', 'out'))

