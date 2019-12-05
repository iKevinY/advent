import fileinput

# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [None, None, None, None]


def handle_mode(tape, mode_op, a, b, c):
    op = mode_op % 100
    mode_a = (mode_op // 100) % 10
    mode_b = (mode_op // 1000) % 10
    mode_c = (mode_op // 10000) % 10

    return op, mode_a, mode_b, mode_c


def emulate(input):
    pc = 0
    tape = TAPE[:]
    outs = []

    while pc < len(tape):
        mode_op, a, b, c = tape[pc:pc+4]
        op, mode_a, mode_b, mode_c = handle_mode(tape, mode_op, a, b, c)

        # ADD a b c
        if op == 1:
            tape[c] = (a if mode_a else tape[a]) + (b if mode_b else tape[b])
            pc += 4

        # MUL a b c
        elif op == 2:
            tape[c] = (a if mode_a else tape[a]) * (b if mode_b else tape[b])
            pc += 4

        # INP a
        elif op == 3:
            tape[a] = input
            pc += 2

        # OUT b
        elif op == 4:
            outs.append(a if mode_a else tape[a])
            pc += 2

        # JZ a b
        elif op == 5:
            if (a if mode_a else tape[a]) != 0:
                pc = (b if mode_b else tape[b])
            else:
                pc += 3

        # JNZ a b
        elif op == 6:
            if (a if mode_a else tape[a]) == 0:
                pc = (b if mode_b else tape[b])
            else:
                pc += 3

        # LT a b c
        elif op == 7:
            tape[c] = 1 if (a if mode_a else tape[a]) < (b if mode_b else tape[b]) else 0
            pc += 4

        # EQ a b c
        elif op == 8:
            tape[c] = 1 if (a if mode_a else tape[a]) == (b if mode_b else tape[b]) else 0
            pc += 4

        # HALT
        elif op == 99:
            if not all(x == 0 for x in outs[:-1]):
                return "Bad output", outs
            return outs[-1]

print "Diagnostic code for system ID 1:", emulate(1)
print "Diagnostic code for system ID 5:", emulate(5)
