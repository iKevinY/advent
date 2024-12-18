import fileinput
from utils import parse_nums


def simulate(program, a, b, c):
    pc = 0
    out = []

    while pc < len(program):
        opcode, literal = program[pc:pc+2]

        if literal <= 3:
            combo = literal
        elif literal == 4:
            combo = a
        elif literal == 5:
            combo = b
        elif literal == 6:
            combo = c

        if opcode == 0:
            a = a // (2 ** combo)
        elif opcode == 1:
            b ^= literal
        elif opcode == 2:
            b = combo % 8
        elif opcode == 3:
            if a != 0:
                pc = literal * 2
                continue
        elif opcode == 4:
            b ^= c
        elif opcode == 5:
            out.append(combo % 8)
        elif opcode == 6:
            b = a // (2 ** combo)
        elif opcode == 7:
            c = a // (2 ** combo)

        pc += 2

    return out


# Read problem input.
for i, line in enumerate(fileinput.input()):
    if i == 0:
        A = parse_nums(line)[0]
    elif i == 1:
        B = parse_nums(line)[0]
    elif i == 2:
        C = parse_nums(line)[0]
    elif i == 4:
        PROGRAM = parse_nums(line)


# Simulate the program for part 1.
part_1 = simulate(PROGRAM, A, B, C)
print("Part 1:", ','.join(str(n) for n in part_1))


# Solve part 2.
#
# For the problem input, note that each "output byte" is affected
# by a byte in order of the starting A register. You can manually
# dial in some of the high bytes of the starting value to narrow
# the search space until it's something viable to be simulated.
start = 0o5322350130000000
for s in range(start, start + 10000000):
    out = []
    A = s
    B = 0
    C = 0
    while True:
        B = A % 8
        B ^= 2
        C = (A // (2**B))
        A >>= 3
        B ^= C
        B ^= 7
        out.append(B % 8)
        if A == 0:
            break

    if out == PROGRAM:
        print("Part 2:", s)
        break
