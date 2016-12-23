import fileinput
from copy import deepcopy


def reg_or_val(regs, x):
    try:
        return int(x)
    except ValueError:
        return regs[x]


def emulate(program, a=0, b=0, c=0, d=0):
    pc = 0
    regs = {'a': a, 'b': b, 'c': c, 'd': d}

    # Toggling instructions modifes the program, so operate on a copy instead.
    program = deepcopy(program)

    while True:
        if pc >= len(program):
            return regs

        cmd, x, y = program[pc]

        if cmd == 'cpy':
            # Subroutines that look like this perform multiplication:
            #   cpy b c
            #   inc a
            #   dec c
            #   jnz c -2
            #   dec d
            #   jnz d -5
            # Perform a lookahead and optimize it by doing the following:
            #   - Set a to b*d
            #   - Set c and d to 0.
            #   - Move forward 5 instructions.
            next_cmds, next_regs = zip(*program[pc+1:pc+5])[0:2]

            if x.isalpha() and next_cmds == ('inc', 'dec', 'jnz', 'dec'):
                a, _, c, d = next_regs

                regs[a] = regs[x] * regs[d]
                regs[c] = 0
                regs[d] = 0
                pc += 5
                continue

            # Ignore copy instructions that try to copy a value into an
            # immediate value (occurs when toggling instructions).
            if y.isalpha():
                regs[y] = reg_or_val(regs, x)

        elif cmd == 'inc':
            regs[x] += 1

        elif cmd == 'dec':
            regs[x] -= 1

        elif cmd == 'jnz':
            x = reg_or_val(regs, x)

            if x != 0:
                pc += reg_or_val(regs, y)
                continue

        elif cmd == 'tgl':
            x = reg_or_val(regs, x)
            to_toggle = pc + x
            try:
                cng, nx, ny = program[to_toggle]
            except:
                pc += 1
                continue

            if ny == 'null':
                if cng == 'inc':
                    program[to_toggle][0] = 'dec'
                else:
                    program[to_toggle][0] = 'inc'
            else:
                if cng == 'jnz':
                    program[to_toggle][0] = 'cpy'
                else:
                    program[to_toggle][0] = 'jnz'

        pc += 1


PROGRAM = []

for line in fileinput.input():
    # Add null argument to pad inc/dec instructions
    instruction = line + ' null'
    PROGRAM.append(instruction.split()[:3])

# Note: the actual input program computes f(n) = n! + 7708
print "Value to send to safe:", emulate(PROGRAM, a=7)['a']
print "Actual value for safe:", emulate(PROGRAM, a=12)['a']
