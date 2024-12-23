import fileinput
import networkx as nx


# Read problem input.
G = nx.Graph()

for line in fileinput.input():
    a, b = line.strip().split('-')
    if a not in G:
        G.add_node(a)
    if b not in G:
        G.add_node(b)

    G.add_edge(a, b)


# Solve problem.
part_1 = 0
largest_clique = []

for clique in nx.enumerate_all_cliques(G):
    if len(clique) > len(largest_clique):
        largest_clique = clique

    if len(clique) == 3 and any(n.startswith('t') for n in clique):
        part_1 += 1

print("Part 1:", part_1)
print("Part 2:", ','.join(n for n in sorted(largest_clique)))
