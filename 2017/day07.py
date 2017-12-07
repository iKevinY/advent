import sys
import re
import fileinput


class Disc:
    def __init__(self, name, weight, aboves):
        self.name = name
        self.weight = int(weight)
        self.aboves = aboves
        self.below = None


RE_DISC = re.compile(r'(\w+) \((\d+)\)(?: -> (.+))?')
DISCS = {}

# Process input
for line in fileinput.input():
    name, weight, aboves = RE_DISC.findall(line.strip())[0]

    weight = int(weight)
    aboves = aboves.split(', ') if aboves else []

    DISCS[name] = Disc(name, weight, aboves)


# Link discs to their parent/children
for d in DISCS.values():
    for a in d.aboves:
        DISCS[a].below = d
    d.aboves = [DISCS[a] for a in d.aboves]


# Search for the bottom-most disc
for d in DISCS.values():
    if d.below is None:
        root = d

print 'Name of bottom program:', root.name


def program_weight(node):
    if not node.aboves:
        return node.weight

    weights = [program_weight(a) for a in node.aboves]

    # Since we're performing DFS, we are guaranteed to encounter the problem
    # disc here first; therefore, we compute the correct answer and exit.
    if len(set(weights)) != 1:
        for i, w in enumerate(weights):
            if weights.count(w) == 1:
                diff = w
                wrong_disc = node.aboves[i].name
            else:
                same = w

        proper_weight = DISCS[wrong_disc].weight + (same - diff)
        print "Proper weight of `{}`: {}".format(wrong_disc, proper_weight)
        sys.exit()

    return sum(weights) + node.weight


# Initialize the recursion, which will also find the solution.
program_weight(root)
