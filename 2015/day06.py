import fileinput
import re

lights = [[0 for x in range(1000)] for x in range(1000)]

for line in fileinput.input():
    cmd, x1, y1, x2, y2 = re.match(r'(.+) (\d+),(\d+) through (\d+),(\d+)', line).groups()
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if cmd == "turn off":
                # lights[x][y] = 0
                lights[x][y] = max(0, lights[x][y] - 1)
            elif cmd == "turn on":
                # lights[x][y] = 1
                lights[x][y] += 1
            elif cmd == "toggle":
                # lights[x][y] ^= 1
                lights[x][y] += 2

# print "Lights on: %d" % sum([sum(x) for x in lights])
print "Total brightness: %d" % sum([sum(x) for x in lights])
