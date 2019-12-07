import fileinput
from itertools import permutations


def parse_mode(tape, mode_op, a, b, c):
    op = mode_op % 100
    mode_a = (mode_op // 100) % 10
    mode_b = (mode_op // 1000) % 10
    mode_c = (mode_op // 10000) % 10

    return op, mode_a, mode_b, mode_c


GLOBAL_INPUTS = [0, 0, 0, 0, 0]


def emulate(phase, amp_num, pc=0):
    tape = TAPE[:]
    outs = []
    read_phase = False

    while pc < len(tape):
        mode_op, a, b, c = tape[pc:pc+4]
        op, mode_a, mode_b, mode_c = parse_mode(tape, mode_op, a, b, c)
        modes = [mode_a, mode_b, mode_c]
        last_pc = pc

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
            if read_phase:
                tape[a] = GLOBAL_INPUTS[amp_num]
            else:
                tape[a] = phase
                read_phase = True
            pc += 2

        # OUT b
        elif op == 4:
            outs.append(a if mode_a else tape[a])
            yield a if mode_a else tape[a]
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
            raise StopIteration()


def emulate_sequence(phases):
    global GLOBAL_INPUTS
    GLOBAL_INPUTS = [0] * 5
    amps = [emulate(phases[i], i) for i in range(5)]
    inp = 0
    on_amp = 0
    last_output = 0

    try:
        while True:
            inp = next(amps[on_amp])
            last_output = inp
            on_amp = (on_amp + 1) % 5
            GLOBAL_INPUTS[on_amp] = inp
    except StopIteration:
        return last_output


# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [None, None, None, None]

print "Part 1:", max(emulate_sequence(p) for p in permutations(range(5), 5))
print "Part 2:", max(emulate_sequence(p) for p in permutations(range(5, 10), 5))
