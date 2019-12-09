import fileinput


# True = read, False = write
INSTRUCTIONS = {
    1: (True, True, False),
    2: (True, True, False),
    3: (False, None, None),
    4: (True, None, None),
    5: (True, True, None),
    6: (True, True, None),
    7: (True, True, False),
    8: (True, True, False),
    9: (True, None, None),
    99: (None, None, None)
}


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

    def resolve_modes(op, params, modes):
        res = [a, b, c]

        for i, (is_read, p, m) in enumerate(zip(INSTRUCTIONS[op], params, modes)):
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
