import fileinput
from utils import Point, N, S, E, W

DIR_MAPPING = {
    'U': N,
    'D': S,
    'L': W,
    'R': E,

    '0': E,
    '1': S,
    '2': W,
    '3': N,
}

def discrete_polygon_area(points):
    # Use shoelace formula to compute internal area.
    area = 0

    for a, b in zip(points, points[1:] + [points[0]]):
        area += (b.x + a.x) * (b.y - a.y)

    area = int(abs(area / 2.0))

    # Calculate perimeter.
    perimeter = sum(a.dist_manhattan(b) for a, b in zip(points, points[1:] + [points[0]]))

    # Account for outer perimeter strip in final area computation.
    return area + (perimeter // 2) + 1


# Parse problem input.
p1_pos = Point(0, 0)
p2_pos = Point(0, 0)

p1_points = [p1_pos]
p2_points = [p2_pos]

for line in fileinput.input():
    direction, distance, hex_code = line.split()
    p1_dir = DIR_MAPPING[direction]
    p1_dist = int(distance)

    p2_dir = DIR_MAPPING[hex_code[-2]]
    p2_dist = int(hex_code[2:-2], 16)

    p1_pos += p1_dir * p1_dist
    p2_pos += p2_dir * p2_dist

    p1_points.append(p1_pos)
    p2_points.append(p2_pos)


# Solve problem.
print("Part 1:", discrete_polygon_area(p1_points))
print("Part 2:", discrete_polygon_area(p2_points))
