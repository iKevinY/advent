import fileinput
from collections import defaultdict


def bfs(graph, start, end=None):
    dist = -1
    seen = set()
    frontier = [start]
    while frontier:
        new_frontier = []
        for _ in range(len(frontier)):
            p = frontier.pop()
            for c in graph[p]:
                if c == end:
                    return dist
                if c not in seen:
                    new_frontier.append(c)
                seen.add(c)

        frontier = new_frontier
        dist += 1

    return dist


orbits = defaultdict(set)
undirected = defaultdict(set)
planets = set()

for line in fileinput.input():
    a, b = line.strip().split(')')

    orbits[b].add(a)
    undirected[b].add(a)
    undirected[a].add(b)
    planets.add(a)
    planets.add(b)

print "Total orbits:", sum(bfs(orbits, p) for p in planets)
print "Minimum orbital transfers:", bfs(undirected, 'YOU', 'SAN')
