
import sys
import fileinput

from utils import parse_nums, Point, NE, SE, SW, NW

# How far to the closest beacon?
manhattan = {}
sensors = set()
beacons = set()

min_x = 1e9
max_x = -1e9

# Parse input
for line in fileinput.input():
    sx, sy, bx, by = parse_nums(line)
    min_x = min(min_x, sx)
    max_x = max(max_x, sx)
    s = Point(sx, sy)
    b = Point(bx, by)
    sensors.add(s)
    beacons.add(b)
    manhattan[s] = s.dist_manhattan(b)


# Part 1
TARGET_Y = 2000000
part_1 = 0

# Only consider the sensors whose area could possibly overlap with the given row.
close_sensors = set(s for s in sensors if s.y - manhattan[s] <= TARGET_Y <= s.y + manhattan[s])

# Compute the intervals created by the sensor areas along this row.
intervals = []
for s in close_sensors:
    vertical_delta = abs(s.y - TARGET_Y)
    half_chord = manhattan[s] - vertical_delta
    intervals.append((s.x - half_chord, s.x + half_chord))

# Merge the intervals to de-duplicate overlaps.
intervals.sort()
merged_intervals = []
merged = set()
for i, (a, b) in enumerate(intervals):
    if i in merged:
        continue

    end = b
    for j, (c, d) in enumerate(intervals):
        if i == j:
            continue
        if a <= c <= end:
            end = max(end, d)
            merged.add(j)

    merged_intervals.append((a, end))

# Answer is the sum of merged intervals minus any beacons in that row.
part_1 = sum(b - a + 1 for a, b in merged_intervals)
part_1 -= sum(1 for b in beacons if b.y == TARGET_Y)
print("Part 1:", part_1)


# Part 2
MIN_BEACON = 0
MAX_BEACON = 4000000

def gen_outskirts():
    """Yields the set of points outside-neighbouring the perimeter of all sensors."""
    for s in sensors:
        d = manhattan[s] + 1
        p = Point(s.x - d, s.y)
        for move in [NE, SE, SW, NW]:
            for _ in range(d):
                p += move
                if MIN_BEACON <= p.x <= MAX_BEACON and MIN_BEACON <= p.y <= MAX_BEACON:
                    yield p

# Check all outskirt positions for whether it could be the undetected beacon.
for p in gen_outskirts():
    for s in sensors:
        if p.dist_manhattan(s) <= manhattan[s]:
            break
    else:
        tuning_freq = p.x * 4000000 + p.y
        print("Part 2:", tuning_freq)
        break

