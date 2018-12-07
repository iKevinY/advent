import fileinput
from copy import deepcopy
from collections import defaultdict


def toposort(data):
    """
    Topological sort implementation via:
    https://bitbucket.org/ericvsmith/toposort/src/e63ddf93ccb68a7e33ba97680ecdb72ea9f96669/toposort.py
    """
    from functools import reduce as _reduce

    # Special case empty input.
    if len(data) == 0:
        return

    # Copy the input so as to leave it unmodified.
    data = data.copy()

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = _reduce(set.union, data.values()) - set(data.keys())
    # Add empty dependences where needed.
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if len(dep) == 0)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered) for item, dep in data.items() if item not in ordered}
    if len(data) != 0:
        raise Exception()


def purge_val(graph, val):
    for k in graph:
        graph[k].discard(val)

    try:
        del graph[val]
    except Exception:
        pass


# Read problem input
GRAPH = defaultdict(set)

for line in fileinput.input():
    words = line.split()
    a, b = words[1], words[7]
    GRAPH[b].add(a)


# Solve Part 1
graph = deepcopy(GRAPH)
order = ''

while graph:
    candidates = sorted(''.join(next(toposort(graph))))
    a = candidates[0]
    order += a
    purge_val(graph, a)

print "Instruction order:", order


# Solve Part 2
graph = deepcopy(GRAPH)
workers = [('.', 0)] * 5
queued = set()

time = 0
done = ''

while True:
    try:
        okay = set(next(toposort(graph)))
    except StopIteration:
        break

    candidates = list(sorted(okay - queued, reverse=True))

    for i, (step, left) in enumerate(workers):
        if step != '.' and left == 0:
            done += step
            purge_val(graph, step)
            workers[i] = ('.', 0)
            break
    else:
        for i, (step, left) in enumerate(workers):
            if step == '.' and candidates:
                a = candidates.pop()
                queued.add(a)
                workers[i] = (a, 60 + (ord(a) - ord('A')))
            elif step != '.':
                a, b = workers[i]
                workers[i] = (a, b - 1)

        # print "t={}\tworkers={}\tdone={}".format(time, ' '.join(w[0] for w in workers), done)
        time += 1

    continue

print "Time to complete all steps:", time
