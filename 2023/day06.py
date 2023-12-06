import fileinput
from utils import mul


def solve(time, record):
    num_wins = 0
    for hold_time in range(time + 1):
        total_distance = hold_time * (time - hold_time)
        if total_distance > record:
            num_wins += 1

    return num_wins


# Parse problem input.
for i, line in enumerate(fileinput.input()):
    if i == 0:
        times = [int(x) for x in line.split()[1:]]
    else:
        distances = [int(x) for x in line.split()[1:]]


# Solve problem.
print("Part 1:", mul(solve(time, record) for time, record in zip(times, distances)))

part_2_time = int(''.join(str(n) for n in times))
part_2_distance = int(''.join(str(n) for n in distances))
print("Part 2:", solve(part_2_time, part_2_distance))

