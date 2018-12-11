import fileinput


SIZE = 300


def power_level(x, y, serial):
    rack_id = x + 10
    return (((rack_id * y + serial) * rack_id // 100) % 10) - 5


def power_search(partials, conv_size):
    best_power = 0
    best_x = 0
    best_y = 0

    for y in range(1, SIZE - conv_size + 1):
        for x in range(1, SIZE - conv_size + 1):
            xx = x + conv_size
            yy = y + conv_size
            power = PARTIALS[yy][xx] + PARTIALS[y][x] - PARTIALS[y][xx] - PARTIALS[yy][x]

            if power > best_power:
                best_power = power
                best_x = x + 1
                best_y = y + 1

    return best_power, best_x, best_y, conv_size,


SERIAL = int(fileinput.input()[0])
PARTIALS = [[0 for _ in range(SIZE + 1)] for _ in range(SIZE + 1)]

for y in range(1, SIZE + 1):
    for x in range(1, SIZE + 1):
        PARTIALS[y][x] = power_level(x, y, SERIAL) + PARTIALS[y][x-1] + PARTIALS[y-1][x] - PARTIALS[y-1][x-1]

print "Coordinate of most powerful 3x3 grid: {1},{2}".format(*power_search(PARTIALS, 3))
print "Identifier of the largest total power: {1},{2},{3}".format(*max(power_search(PARTIALS, n) for n in range(1, SIZE)))
