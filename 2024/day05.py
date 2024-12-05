import fileinput
from collections import defaultdict

from utils import parse_nums


def is_unordered(graph, update):
    """Returns -1 if ordered, else the index of the first bad page."""
    for i, n in enumerate(update):
        if any(n in graph[m] for m in update[i+1:]):
            return i

    return -1

def mid(lst):
    return lst[(len(lst) - 1) // 2]


on_updates = False
graph = defaultdict(set)
updates = []
for line in fileinput.input():
    if on_updates:
        updates.append(parse_nums(line))
    else:
        if line.strip():
            x, y = parse_nums(line)
            graph[x].add(y)
        else:
            on_updates = True

part_1 = 0
part_2 = 0

for update in updates:
    if is_unordered(graph, update) == -1:
        part_1 += mid(update)
    else:
        while True:
            swap = False
            for i, n in enumerate(update):
                afters = update[i+1:]
                if any(n in graph[a] for a in afters):
                    update[i], update[i + 1] = update[i + 1], update[i]
                    swap = True
            if not swap:
                break

        part_2 += mid(update)

print("Part 1:", part_1)
print("Part 2:", part_2)
