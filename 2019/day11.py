import time
import fileinput
from collections import defaultdict


GLOBAL_INPUTS = [0]

# True = read, False = write
INSTRUCTIONS = {
    1: ('ADD', (True, True, False)),
    2: ('MUL', (True, True, False)),
    3: ('INP', (False, None, None)),
    4: ('OUT', (True, None, None)),
    5: ('JZ ', (True, True, None)),
    6: ('JNZ', (True, True, None)),
    7: ('LT ', (True, True, False)),
    8: ('EQ ', (True, True, False)),
    9: ('REL', (True, None, None)),
    99: ('HLT', (None, None, None)),
}


def parse_mode(tape, mode_op, a, b, c):
    op = mode_op % 100
    mode_a = (mode_op // 100) % 10
    mode_b = (mode_op // 1000) % 10
    mode_c = (mode_op // 10000) % 10

    return op, mode_a, mode_b, mode_c


def emulate(pid, pc=0):
    tape = TAPE[:]
    outs = []
    relative_base = 0

    def resolve_modes(op, params, modes):
        res = [a, b, c]

        for i, (is_read, p, m) in enumerate(zip(INSTRUCTIONS[op][1], params, modes)):
            if is_read is None:
                continue

            if is_read:
                if m == 0:
                    res[i] = tape[p]
                elif m == 1:
                    res[i] = p
                elif m == 2:
                    res[i] = tape[relative_base + p]
            else:
                if m == 0:
                    res[i] = p
                elif m == 2:
                    res[i] = relative_base + p

        return res

    while pc < len(tape):
        mode_op, a, b, c = tape[pc:pc+4]
        op, mode_a, mode_b, mode_c = parse_mode(tape, mode_op, a, b, c)
        a, b, c = resolve_modes(op, (a, b, c), (mode_a, mode_b, mode_c))

        # ADD a b c
        if op == 1:
            tape[c] = a + b
            pc += 4

        # MUL a b c
        elif op == 2:
            tape[c] = a * b
            pc += 4

        # INP a
        elif op == 3:
            tape[a] = GLOBAL_INPUTS[pid]
            pc += 2

        # OUT b
        elif op == 4:
            yield a
            pc += 2

        # JZ a b
        elif op == 5:
            if a != 0:
                pc = b
            else:
                pc += 3

        # JNZ a b
        elif op == 6:
            if a == 0:
                pc = b
            else:
                pc += 3

        # LT a b c
        elif op == 7:
            tape[c] = 1 if a < b else 0
            pc += 4

        # EQ a b c
        elif op == 8:
            tape[c] = 1 if a == b else 0
            pc += 4

        elif op == 9:
            relative_base += a
            pc += 2

        # HALT
        elif op == 99:
            raise StopIteration()


def simulate_robot(start=0):
    grid = {}
    grid[0, 0] = start

    facing = 0
    x, y = 0, 0

    robot = emulate(0)

    try:
        while True:
            grid[x, y] = next(robot)
            if next(robot) == 0:
                facing = (facing - 1) % 4
            else:
                facing = (facing + 1) % 4

            if facing == 0:
                y += 1
            elif facing == 1:
                x += 1
            elif facing == 2:
                y -= 1
            elif facing == 3:
                x -= 1

            GLOBAL_INPUTS[0] = grid.get((x, y), 0)
    except StopIteration:
        return grid


# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000


# Part 1
grid = simulate_robot(0)
print "Number of painted tiles:", len(grid.keys())


# Part 2
grid = simulate_robot(1)

print "Registration ID:\n"
xs, ys = zip(*grid.keys())
for y in reversed(range(min(ys), max(ys) + 1)):
    print ''.join(
        '#' if grid.get((x, y)) else ' '
        for x in range(min(xs), max(xs) + 1))
