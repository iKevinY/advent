import fileinput
from utils import parse_nums


def dist(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


POINTS = [tuple(parse_nums(line)) for line in fileinput.input()]


cliques = [[g] for g in POINTS]
last_len = None

while True:
    if len(cliques) == last_len:
        break

    last_len = len(cliques)

    next_cliques = []
    merged = set()

    for i in range(len(cliques)):
        next_clique = cliques[i][:]

        if i in merged:
            continue

        for j in range(i + 1, len(cliques)):
            for dd in cliques[j]:
                if (any(dist(cc, dd) <= 3 for cc in cliques[i])):
                    next_clique.extend(cliques[j])
                    merged.add(j)
                    break

        next_cliques.append(next_clique)

    cliques = next_cliques

print "Number of constellations:", len(cliques)
