import fileinput
from utils import parse_nums

from z3 import Optimize, Int, And, sat


PART_2_FACTOR = 10000000000000

part_1 = 0
part_2 = 0


INPUT = ''.join(fileinput.input())
for block in INPUT.split('\n\n'):
    lines = block.split('\n')
    ax, ay = parse_nums(lines[0])
    bx, by = parse_nums(lines[1])
    px, py = parse_nums(lines[2])

    a = Int('a')
    b = Int('b')

    for part in range(1, 3):
        o = Optimize()
        o.add(And(
            a >= 0,
            b >= 0,
            a * ax + b * bx == px + (PART_2_FACTOR if part == 2 else 0),
            a * ay + b * by == py + (PART_2_FACTOR if part == 2 else 0),
        ))

        o.minimize(a * 3 + b)

        if o.check() == sat:
            m = o.model()
            result = m[a].as_long() * 3 + m[b].as_long()
            if part == 1:
                part_1 += result
            else:
                part_2 += result

print("Part 1:", part_1)
print("Part 2:", part_2)
