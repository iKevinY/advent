import fileinput

seen = {}
ints = {}

for wire, line in enumerate(fileinput.input()):
    commands = line.split(',')
    x = y = 0
    steps = 1

    for cmd in commands:
        direction = cmd[0]
        dist = int(cmd[1:])

        for _ in range(dist):
            if direction == 'U':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1
            else:
                y += 1

            if (x, y) in seen and wire == 1 and (x, y) not in ints:
                ints[(x, y)] = steps + seen[(x, y)]

            if wire == 0 and (x, y) not in seen:
                seen[x, y] = steps

            steps += 1

print "Distance to closest intersection:", min(abs(a) + abs(b) for a, b in ints.keys())
print "Fewest steps to intersection:", min(n for n in ints.values())
