import fileinput
from itertools import combinations

from utils import parse_nums


def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # https://stackoverflow.com/a/51127674
    px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return [px, py]

# Parse problem input.
HAILSTONES = [tuple(parse_nums(line)) for line in fileinput.input()]

MIN = 200000000000000
MAX = 400000000000000

part_1 = 0

for a, b in combinations(HAILSTONES, 2):
    ax, ay, _, avx, avy, _ = a
    bx, by, _, bvx, bvy, _ = b

    a_slope = avy / avx
    a_b = ay - (a_slope * ax)

    a_start = a_slope * MIN + a_b
    a_end = a_slope * MAX + a_b

    b_slope = bvy / bvx
    b_b = by - (b_slope * bx)

    b_start = b_slope * MIN + b_b
    b_end = b_slope * MAX + b_b

    try:
        px, py = find_intersection(MIN, a_start, MAX, a_end, MIN, b_start, MAX, b_end)
    except:
        # Parallel lines.
        continue

    # Intersection in A's past
    if avx > 0 and px < ax:
        continue
    elif avx < 0 and px > ax:
        continue

    # Intersection in B's past
    if bvx > 0 and px < bx:
        continue
    elif bvx < 0 and px > bx:
        continue

    # Good intersection in zone.
    if MIN <= px <= MAX and MIN <= py <= MAX:
        part_1 += 1

print("Part 1:", part_1)

# Solve Part 2.
try:
    from z3 import Real, Solver
except:
    print("Part 2 requires z3 to be installed (`pip install z3-solver`)")
    import sys
    sys.exit()

mx = Real('mx')
my = Real('my')
mz = Real('mz')
mxv = Real('mxv')
myv = Real('myv')
mzv = Real('mzv')
c = [Real('c' + str(n)) for n in range(len(HAILSTONES))]

s = Solver()

for i, (px, py, pz, vx, vy, vz) in enumerate(HAILSTONES):
    s.add(c[i] >= 0)
    s.add(mx + c[i] * mxv == px + c[i] * vx)
    s.add(my + c[i] * myv == py + c[i] * vy)
    s.add(mz + c[i] * mzv == pz + c[i] * vz)

s.check()
m = s.model()
print("Part 2:", m[mx].as_long() + m[my].as_long() + m[mz].as_long())
