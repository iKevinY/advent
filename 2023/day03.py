import fileinput

SYMBOLS = {}
PARTS = []

# Parse input.
for y, line in enumerate(fileinput.input()):
    num = ''
    for x, c in enumerate(line):
        if not c.isdigit() and c != '.' and c != '\n':
            SYMBOLS[x, y] = c

        if c.isdigit():
            if not num:
                start = x
            num += c
        elif num:
            PARTS.append((int(num), y, x - len(num), x - 1))
            num = ''

# Solve problem.
part_1_seen = set()
part_2 = 0

for x, y in SYMBOLS:
    adj = []
    for i, (n, yy, start, end) in enumerate(PARTS):
        if yy - 1 <= y <= yy + 1 and start - 1 <= x <= end + 1:
            part_1_seen.add(i)
            adj.append(n)

    if len(adj) == 2 and SYMBOLS[x, y] == '*':
        part_2 += adj[0] * adj[1]


print("Part 1:", sum(PARTS[i][0] for i in part_1_seen))
print("Part 2:", part_2)
