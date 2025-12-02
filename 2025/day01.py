import fileinput


START_POS = 50
DAY_1 = 0
DAY_2 = 0

POS = START_POS

for line in fileinput.input():
    direction = line[0]
    distance = int(line[1:])

    if direction == 'L':
        distance *= -1

    new_pos = POS + distance

    # If new_pos >= 100, we crossed or landed on 0 going clockwise.
    if new_pos >= 100:
        # We crossed the number of times of the hundreds-digit.
        DAY_2 += new_pos // 100

    # If new_pos <= 0, we crossed or landed on 0 going counterclockwise.
    elif new_pos <= 0:
        # We crossed the number of times of the hundreds-digit + 1.
        DAY_2 += abs(new_pos // 100)

        # However, if we started this move at 0, remove our double-count.
        if POS == 0:
            DAY_2 -= 1

        # If we landed on 0, we need to add one more zero in this direction,
        # because `-100 // 100 == 1`.
        if new_pos % 100 == 0:
            DAY_2 += 1

    # Fix our position on the dial.
    POS = new_pos % 100

    if POS == 0:
        DAY_1 += 1

print("Day 1:", DAY_1)
print("Day 2:", DAY_2)

