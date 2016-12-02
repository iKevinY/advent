import fileinput
import itertools
import re

LITRES = 150

def permute_containers(containers, litres):
    for i in range(1, len(containers) + 1):
        for c in itertools.combinations(containers, i):
            if sum(c) == litres:
                yield c

containers = [int(n) for n in fileinput.input()]
permutations = list(permute_containers(containers, LITRES))
min_perm_len = min(len(p) for p in permutations)

print "Containers: {}".format(containers)
print "Litres of eggnog: %d" % LITRES

print "Valid combinations: %d" % len(permutations)
print "Minimal combinations: %d" % len([p for p in permutations if len(p) == min_perm_len])
