import fileinput
from copy import deepcopy
from itertools import count

from utils import parse_nums


def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


positions = []
for i, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = parse_nums(line)
    positions.append(list(nums))


velocities = [[0] * 3 for _ in range(4)]

INIT_POS = deepcopy(positions)
INIT_VEL = deepcopy(velocities)
CYCLES = [None, None, None]

for i in count(start=1):
    # Update velocities
    for x in range(4):
        for y in range(x + 1, 4):
            for d in range(3):
                if positions[x][d] < positions[y][d]:
                    velocities[x][d] += 1
                    velocities[y][d] -= 1
                elif positions[x][d] > positions[y][d]:
                    velocities[x][d] -= 1
                    velocities[y][d] += 1

    # Update positions
    for x in range(4):
        for d in range(3):
            positions[x][d] += velocities[x][d]

    energy = 0

    for pos, vel in zip(positions, velocities):
        pot = sum(abs(p) for p in pos)
        kin = sum(abs(p) for p in vel)
        energy += pot * kin

    if i == 1000:
        print "Total energy after 1000 steps:", energy

    for d in range(3):
        if CYCLES[d] is not None:
            continue

        for m in range(4):
            if positions[m][d] != INIT_POS[m][d]:
                break
            if velocities[m][d] != INIT_VEL[m][d]:
                break
        else:
            CYCLES[d] = i

    if all(CYCLES):
        print "Steps for full cycle:", lcm(lcm(CYCLES[0], CYCLES[1]), CYCLES[2])
        break
