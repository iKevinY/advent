import fileinput


def reg_or_val(regs, x):
    try:
        return int(x)
    except ValueError:
        return regs[x]


def emulate(program, a=0, b=0, c=0, d=0):
    pc = 0
    regs = {'a': a, 'b': b, 'c': c, 'd': d}

    while True:
        if pc >= len(program):
            return regs

        cmd, x, y = program[pc]

        if cmd == 'cpy':
            regs[y] = reg_or_val(regs, x)

        elif cmd == 'inc':
            regs[x] += 1

        elif cmd == 'dec':
            regs[x] -= 1

        elif cmd == 'jnz':
            x = reg_or_val(regs, x)

            if x != 0:
                pc += int(y)
                continue

        pc += 1


PROGRAM = []

for line in fileinput.input():
    # Add null argument to pad inc/dec instructions
    instruction = line + ' null'
    PROGRAM.append(instruction.split()[:3])

print "Value in register a:", emulate(PROGRAM)['a']
print "When setting c to 1:", emulate(PROGRAM, c=1)['a']
