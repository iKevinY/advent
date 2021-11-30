import fileinput


grid = [line.strip() for line in fileinput.input()]

max_y = len(grid)
max_x = len(grid[0])

part_1 = 0
part_2 = 1

for xs, ys in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    x = 0
    y = 0
    tot = 0

    while y < max_y:
        if grid[y][x] == '#':
            tot += 1

        x = (x + xs) % max_x
        y += ys

    part_2 *= tot

    if (xs, ys) == (3, 1):
        part_1 = tot

print part_1
print part_2
