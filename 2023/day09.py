import fileinput


part_1 = 0
part_2 = 0

for line in fileinput.input():
    row = [int(x) for x in line.split()]

    # Build up triangle.
    triangle = [row[:]]

    while any(n != 0 for n in triangle[-1]):
        row = []
        for a, b in zip(triangle[-1], triangle[-1][1:]):
            row.append(b - a)

        triangle.append(row)

    triangle.reverse()

    # Extrapolate right column.
    right = [0]
    for *_, n in triangle[1:]:
        right.append(right[-1] + n)

    part_1 += right[-1]

    # Extrapolate left column.
    left = [0]
    for n, *_ in triangle[1:]:
        left.append(n - left[-1])

    part_2 += left[-1]


print("Part 1:", part_1)
print("Part 2:", part_2)

