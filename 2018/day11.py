import fileinput


def power_level(x, y, serial):
    x += 1
    y += 1
    rack_id = x + 10
    return (((rack_id * y + serial) * rack_id // 100) % 10) - 5


SERIAL = int(fileinput.input()[0])
SIZE = 300
GRID = [[power_level(x, y, SERIAL) for x in range(SIZE)] for y in range(SIZE)]

overall_sum = 0
overall_x = 0
overall_y = 0
overall_size = 0

for size in range(3, 16):  # window size of 16 is good enough...right?
    best_sum = 0
    best_x = 0
    best_y = 0

    for y in range(SIZE - size):
        for x in range(SIZE - size):
            total = 0
            for j in range(size):
                for i in range(size):
                    total += GRID[y + j][x + i]

            if total > best_sum:
                best_sum = total
                best_x = x
                best_y = y

    if size == 3:
        print "Coordinate of most powerful 3x3 grid: {},{}".format(best_x + 1, best_y + 1)

    if best_sum > overall_sum:
        overall_sum = best_sum
        overall_x = best_x
        overall_y = best_y
        overall_size = size

print "Identifier of the largest total power: {},{},{}".format(overall_x + 1, overall_y + 1, overall_size)
