import math
import fileinput
from collections import deque, defaultdict

from utils import Point


# Read problem input
asteroids = set()

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        if c == '#':
            asteroids.add(Point(x, y))


# Part 1
detections = {
    a: len(set(a.angle(o) for o in (asteroids - set([a]))))
    for a in asteroids
}

station, num = max(detections.items(), key=lambda x: x[1])
print "Number of detections:", num


# Part 2
asteroids.remove(station)

# Construct a circular list that is sorted by increasing angle,
# and contains sorted lists of the asteroids at that angle from
# the station (going from furthest to closest). We rotate in the
# positive-radian direction as a hack, since the y-axis coordinates
# actually increase going downwards (as opposed to upwards).
by_angle = defaultdict(list)
for a in asteroids:
    by_angle[station.angle(a)].append(a)

for k, v in by_angle.items():
    v.sort(key=station.dist, reverse=True)

queue = deque(sorted(by_angle.items()))

# Rotate the queue to the starting angle
start = math.pi / 2
while abs(queue[0][0] - start) > 1e-6:
    queue.rotate(-1)

# Iterate through the circular list, vaporizing the closest asteroid
# at that angle, then moving to the next angle in the rotation.
for i in range(200):
    at_angle = queue[0][1]
    vaporized = at_angle.pop()
    if not at_angle:
        queue.popleft()
    else:
        queue.rotate(-1)

print "200th asteroid checksum:", vaporized.x * 100 + vaporized.y
