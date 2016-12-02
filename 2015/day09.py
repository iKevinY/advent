#!/usr/bin/env python
import fileinput
import itertools
import re

def parse_line(line):
    departure, arrival, distance = re.match(r'(\w+) to (\w+) = (\d+)', line).groups()
    return departure, arrival, int(distance)

def sum_of_paths(d):
    # Yield sum of all possible routes
    for p in itertools.permutations(locations, len(locations)):
        yield sum(d[p[i]][p[i+1]] for i in range(len(p) - 1))

distances = {}

# Parse input
for line in fileinput.input():
    frm, to, dist = parse_line(line)
    if distances.get(frm):
        distances[frm][to] = dist
    else:
        distances[frm] = {to: dist}

    if distances.get(to):
        distances[to][frm] = dist
    else:
        distances[to] = {frm: dist}

locations = distances.keys()

print "Shortest route: %d" % min(sum_of_paths(distances))
print "Longest route: %d" % max(sum_of_paths(distances))
