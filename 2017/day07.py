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


BAD_WEIGHTS = {}


def program_weight(node):
    if not node.aboves:
        return node.weight

    weights = [program_weight(a) for a in node.aboves]

    # Keep track of discs whose children have different weights
    if len(set(weights)) != 1:
        BAD_WEIGHTS[node.name] = weights

    return sum(weights) + node.weight


# Seed `BAD_WEIGHTS`
program_weight(root)

# Traverse from root until the offending disc is found
bad_disc = root
while True:
    for a in bad_disc.aboves:
        if a.name in BAD_WEIGHTS:
            bad_disc = a
            break
    else:
        break

# Determine the correct weight of the child disc
weights = BAD_WEIGHTS[bad_disc.name]

for i, w in enumerate(weights):
    if weights.count(w) == 1:
        diff = w
        wrong_disc = bad_disc.aboves[i].name
    else:
        same = w

proper_weight = DISCS[wrong_disc].weight + (same - diff)
print "Proper weight of `{}`: {}".format(wrong_disc, proper_weight)
