import fileinput
from utils import parse_nums


def solve(vel_x=0, vel_y=0):
    x = 0
    y = 0
    max_y = 0

    while x <= END_X and y >= END_Y - 30:
        x += vel_x
        y += vel_y
        max_y = max(max_y, y)

        if vel_x > 0:
            vel_x -= 1
        elif vel_x < 0:
            vel_x += 1

        vel_y -= 1

        # We are in the target zone.
        if START_X <= x <= END_X and START_Y <= y <= END_Y:
            return max_y


# Parse problem input.
START_X, END_X, START_Y, END_Y = parse_nums(fileinput.input()[0])

# Compute viable start velocities.
viables = [solve(x, y) for y in range(START_Y, -START_Y + 1) for x in range(END_X + 1)]
viables = [v for v in viables if v is not None]

print "Part 1:", max(viables)
print "Part 2:", sum(1 for v in viables)
