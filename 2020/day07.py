import fileinput
from collections import defaultdict
from utils import parse_line

GOAL = 'shiny gold'

graph = defaultdict(set)

for i, line in enumerate(fileinput.input()):
    line = line.strip()
    color, rest = parse_line(r'(\w+ \w+) bags contain (.+)+', line)
    rest = rest.replace('.', '').split(',')

    for r in rest:
        if r != 'no other bags':
            parts = r.split()
            new_color = ' '.join(parts[1:3])
            graph[color].add((new_color, int(parts[0])))


def dfs_1(node):
    if node == GOAL:
        return True

    return any(dfs_1(n) for n, _ in graph[node])


def dfs_2(node, count=1):
    tot = 1

    for nxt, amt in graph[node]:
        tot += dfs_2(nxt, amt)

    return count * tot

part_1 = 0

keys = graph.keys()

for bag in keys:
    print bag
    if dfs_1(bag):
        part_1 += 1
        print "good"

print part_1 - 1


print dfs_2(GOAL) - 1
