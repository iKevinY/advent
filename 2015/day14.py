import fileinput
import re

def fly(time, speed, fly_for, rest_for):
    cycle = fly_for + rest_for
    return speed * (
        ((time // cycle) * fly_for) +  # flying time * full cycles completed
        min(fly_for, time % cycle)     # remaining incomplete flying time
    )

TOTAL_TIME = 2503

reindeer = [[int(n) for n in re.findall(r'\d+', line)] for line in fileinput.input()]

print "Winning reindeer distance: %d" % max(fly(TOTAL_TIME, *r) for r in reindeer)

points = [0] * len(reindeer)

for t in range(1, TOTAL_TIME + 1):
    positions = [fly(t, *r) for r in reindeer]
    for i, pos in enumerate(positions):
        if pos == max(positions):
            points[i] += 1

print "Highest point total: %d" % max(points)

