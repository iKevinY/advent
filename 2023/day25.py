import fileinput
from utils import mul

try:
    import networkx as nx
except ImportError:
    print("Solution requires NetworkX (`pip install networkx`)")
    import sys
    sys.exit()

# Parse problem input.
graph = nx.Graph()

for line in fileinput.input():
    src, rest = line.strip().split(': ')
    graph.add_node(src)
    for dest in rest.split():
        graph.add_edge(src, dest)

# Solve part 1.
for a, b in nx.minimum_edge_cut(graph):
    graph.remove_edge(a, b)

print("Part 1:", mul(len(c) for c in nx.connected_components(graph)))
