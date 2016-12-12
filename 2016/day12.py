import fileinput


def simulate(program, a=0, b=0, c=0, d=0):
    pc = 0
    regs = {'a': a, 'b': b, 'c': c, 'd': d}

    while True:
        if pc >= len(program):
            return regs

        inst = program[pc].split()

        if len(inst) == 2:
            cmd, x = inst
            y = None
        else:
            cmd, x, y = inst

        if cmd == 'cpy':
            regs[y] = int(x) if x.isdigit() else regs[x]

        elif cmd == 'inc':
            regs[x] += 1

        elif cmd == 'dec':
            regs[x] -= 1

        elif cmd == 'jnz':
            x = int(x) if x.isdigit() else regs[x]

            if x == 0:
                pc += 1
                continue
            else:
                pc += int(y)
                continue

        pc += 1


PROGRAM = [line.strip() for line in fileinput.input()]

print "Value in register a:", simulate(PROGRAM)['a']
print "When setting c to 1:", simulate(PROGRAM, c=1)['a']
