import fileinput

# Initialize emulator.
cycle = 1
X = 1

WIDTH = 40
HEIGHT = 6

def draw_pixel():
    pos = ((cycle - 1) % WIDTH) + 1
    if X <= pos < X + 3:
        print("#", end="")
    else:
        print(".", end="")

    if pos == WIDTH:
        print()


# Part 1
interesting_cycle = [20, 60, 100, 140, 180, 220]
signal_strengths = []

for line in fileinput.input():
    ins = line.split()
    op = ins[0]

    if op == 'noop':
        draw_pixel()
        if cycle in interesting_cycle:
            signal_strengths.append(X * cycle)
        cycle += 1

    elif op == 'addx':
        arg = int(ins[1])

        # Process first cycle of draw_pixelx.
        draw_pixel()
        if cycle in interesting_cycle:
            signal_strengths.append(X * cycle)
        cycle += 1

        # Process second cycle of draw_pixelx.
        draw_pixel()
        X += arg
        if cycle in interesting_cycle:
            signal_strengths.append(X * cycle)
        cycle += 1

print()
print("Part 1:", sum(signal_strengths))
