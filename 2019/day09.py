import fileinput


GLOBAL_INPUTS = [0]


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

    def resolve_modes(a, b, c, mode_a, mode_b, mode_c):
        res = [a, b, c]
        try:
            if mode_a == 0:
                res[0] = tape[a]
            elif mode_a == 1:
                res[0] = a
            elif mode_a == 2:
                res[0] = tape[relative_base + a]
        except e:
            pass

        try:
            if mode_b == 0:
                res[1] = tape[b]
            elif mode_b == 1:
                res[1] = b
            elif mode_b == 2:
                res[1] = tape[relative_base + b]
        except e:
            pass

        # Third param always output, instruction handles indirection
        try:
            if mode_c == 0:
                res[2] = c
            elif mode_c == 2:
                res[2] = relative_base + c
        except e:
            pass

        return res

    while pc < len(tape):
        mode_op, a, b, c = tape[pc:pc+4]
        op, mode_a, mode_b, mode_c = parse_mode(tape, mode_op, a, b, c)

        # INP uses first param to determine indirection, special case
        if op != 3:
            a, b, c = resolve_modes(a, b, c, mode_a, mode_b, mode_c)

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
            if mode_a == 0:
                tape[a] = GLOBAL_INPUTS[pid]
            elif mode_a == 2:
                tape[relative_base + a] = GLOBAL_INPUTS[pid]

            pc += 2

        # OUT b
        elif op == 4:
            outs.append(a)
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
            return outs

# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000  # Pad memory

GLOBAL_INPUTS[0] = 1
print "BOOST keycode:", emulate(0)[0]

GLOBAL_INPUTS[0] = 2
print "Coordinates of distress signal:", emulate(0)[0]
