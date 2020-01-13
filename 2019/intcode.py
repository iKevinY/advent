#!/usr/bin/env python
from collections import defaultdict

# Potential debug output
BREAKPOINTS = set([])
LAST_SEEN = defaultdict(list)

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


def debug_param_mode(param, mode, relative_base):
    if mode == 0:
        return '%({})'.format(param)
    elif mode == 1:
        return str(param)
    elif mode == 2:
        return '%({}{}{})'.format(relative_base, '+' if param >= 0 else '', param)


def parse_mode(mode_op, a, b, c):
    op = mode_op % 100
    mode_a = (mode_op // 100) % 10
    mode_b = (mode_op // 1000) % 10
    mode_c = (mode_op // 10000) % 10

    return op, mode_a, mode_b, mode_c


def emulate(base_tape, inputs, pc=0, relative_base=0, debug=False):
    tape = defaultdict(int)
    for i, v in enumerate(base_tape):
        tape[i] = v

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

    while True:
        mode_op = tape[pc]
        a = tape[pc+1]
        b = tape[pc+2]
        c = tape[pc+3]
        op, mode_a, mode_b, mode_c = parse_mode(mode_op, a, b, c)
        modes = [mode_a, mode_b, mode_c]
        last_pc = pc

        if debug:
            foo = INSTRUCTIONS.get(op, ('???', ()))
            ins = foo[0]
            n = sum(i is not None for i in foo[1])
            params = ' '.join(debug_param_mode(tape[pc+1+i], modes[i], relative_base) for i in range(n))
            print 'PC: {:3}  RB: {:3} |'.format(pc, relative_base), ins, params

            if pc in BREAKPOINTS:
                if pc in LAST_SEEN:
                    for i, (m, n) in enumerate(zip(LAST_SEEN[pc], tape)):
                        if m != n:
                            print "    | >  {}: {} -> {}".format(i, m, n)

                LAST_SEEN[last_pc] = tape[:]
                time.sleep(0.001)

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
            if len(inputs) == 0:
                tape[a] = -1
            else:
                tape[a] = inputs.pop()
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


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Usage: intcode.py <intcode_program> [stdin]"
        sys.exit(2)

    with open(sys.argv[1]) as f:
        tape = [int(x) for x in f.readlines()[0].split(',')]

    inputs = []

    if len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            inputs = [int(x) for x in f.readlines()[0].split(',')]

    vm = emulate(tape, inputs)

    try:
        while True:
            print(next(vm))
    except StopIteration:
        pass
