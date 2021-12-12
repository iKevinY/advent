import copy
import fileinput
from collections import Counter, defaultdict


graph = defaultdict(set)
smalls = set()

for line in fileinput.input():
    a, b = line.strip().split('-')

    graph[a].add(b)
    graph[b].add(a)


def dfs(start, extra_time=False):
    num_paths = [0]
    def _dfs(node, seen=None, doubled=False):
        if seen is None:
            seen = Counter({'start': 1 if extra_time else 0})

        if node == 'end':
            num_paths[0] += 1
            return

        # If small cave, check if part 1/2 and skip accordingly.
        if node == node.lower():
            if (doubled or not extra_time) and seen[node] >= 1:
                return
            elif not doubled and seen[node] >= 2:
                return

        seen[node] += 1
        if node == node.lower() and node not in ('start', 'end') and seen[node] >= 2:
            doubled = True

        for n in graph[node]:
            _dfs(n, copy.deepcopy(seen), doubled=doubled)

    _dfs(start)
    return num_paths[0]


print "Part 1:", dfs('start')
print "Part 2:", dfs('start', extra_time=True)
