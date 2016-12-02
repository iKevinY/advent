#!/usr/bin/env python
import fileinput
import itertools
import re

def parse_line(line):
    p1, gl, diff, p2 = re.search(r'(\w+) .* (gain|lose) (\d+) .* (\w+).', line).groups()
    return p1, p2, int(diff) * (-1 if gl == 'lose' else 1)

def happiness_deltas(d):
    # Not optimal because it includes cyclic permutations and reversals
    for p in itertools.permutations(d.keys(), len(d.keys())):
        total = 0
        for i in range(len(p)):
            total += d[p[i]][p[(i+1) % len(p)]]
            total += d[p[(i+1) % len(p)]][p[i]]

        yield total


people = {}

# Parse input
for line in fileinput.input():
    p1, p2, diff = parse_line(line)
    if p1 in people:
        people[p1][p2] = diff
    else:
        people[p1] = {p2: diff}


print "Largest total change in happiness: %d" % max(happiness_deltas(people))

# Add self into list of keys for second part of problem
for person in people.keys():
    people[person]["iKevinY"] = 0

people["iKevinY"] = {person: 0 for person in people.keys()}

print "After adding me: %d" % max(happiness_deltas(people))
