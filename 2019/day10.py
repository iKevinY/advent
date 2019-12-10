import math
import fileinput
from collections import deque, defaultdict


def dist(x, y):
    return (((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2)) ** 0.5


def angle(a, b):
    return math.atan2(a[1] - b[1], a[0] - b[0])


# Read problem input
asteroids = set()

for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        if c == '#':
            asteroids.add((x, y))


# Part 1
detections = {
    ast: len(set(angle(ast, other) for other in (asteroids - set(ast))))
    for ast in asteroids
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
by_angles = defaultdict(list)
for a in asteroids:
    by_angles[angle(station, a)].append(a)

for k, v in by_angles.items():
    v.sort(key=lambda a: -dist(station, a))

queue = deque(sorted(by_angles.items()))

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

print "200th asteroid checksum:", vaporized[0] * 100 + vaporized[1]
