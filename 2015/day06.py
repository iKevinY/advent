import fileinput
import re

instructions = []

for line in fileinput.input():
    cmd, x1, y1, x2, y2 = re.match(r'(.+) (\d+),(\d+) through (\d+),(\d+)', line).groups()
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    instructions.append((cmd, x1, x2, y1, y2))


def total_lights(instructions, brightness=False):
    lights = [[0 for x in range(1000)] for x in range(1000)]

    for cmd, x1, x2, y1, y2 in instructions:
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if cmd == "turn off":
                    if brightness:
                        lights[x][y] = max(0, lights[x][y] - 1)
                    else:
                        lights[x][y] = 0

                elif cmd == "turn on":
                    if brightness:
                        lights[x][y] += 1
                    else:
                        lights[x][y] = 1

                elif cmd == "toggle":
                    if brightness:
                        lights[x][y] += 2
                    else:
                        lights[x][y] ^= 1

    return sum(sum(x) for x in lights)


print "Lights on: %d" % total_lights(instructions)
print "Total brightness: %d" % total_lights(instructions, brightness=True)
