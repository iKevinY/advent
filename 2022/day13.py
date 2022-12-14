import fileinput


def right_order(x, y):
    if type(x) == int and type(y) == int:
        if int(x) < int(y):
            return True
        elif int(x) > int(y):
            return False
        else:
            return None

    if type(x) == int:
        x = [x]
    if type(y) == int:
        y = [y]

    if len(x) == len(y) == 0:
        return None
    elif len(x) == 0:
        return True
    elif len(y) == 0:
        return False

    x, *xs = x
    y, *ys = y

    ret = right_order(x, y)
    if ret is None:
        return right_order(xs, ys)
    return ret


# Solve part 1 while parsing input.
packets = []
pair = []
part_1 = 0
idx = 1
for line in fileinput.input():
    if not line.strip():
        if right_order(*pair):
            part_1 += idx
        pair = []
        idx += 1
    else:
        packet = eval(line.strip())
        pair.append(packet)
        packets.append(packet)

# Final pair because no trailing newline.
if right_order(*pair):
    part_1 += idx

print("Part 1:", part_1)


# Solve Part 2.
packets.insert(0, [[2]])
packets.insert(0, [[6]])

mapping = {}
for i, p1 in enumerate(packets):
    count = 0
    for j, p2 in enumerate(packets):
        if i == j:
            continue

        if right_order(p2, p1):
            count += 1

    mapping[i] = count

two = mapping[0] + 1
six = mapping[1] + 1
print("Part 2:", two*six)
