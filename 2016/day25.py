import fileinput
from copy import deepcopy
from itertools import count


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

    while pc < len(program):
        cmd, x, y = program[pc]

        if cmd == 'cpy':
            # The following set of instructions performs multiplication:
            #   cpy b c
            #   inc a
            #   dec c
            #   jnz c -2
            #   dec d
            #   jnz d -5
            #
            # Perform a peephole optimization by doing the following:
            #   - Set a to b*d
            #   - Set c and d to 0.
            #   - Advance the PC by 6 to jump past the instructions.
            next_cmds, next_regs = zip(*program[pc+1:pc+5])[0:2]

            if x.isalpha() and next_cmds == ('inc', 'dec', 'jnz', 'dec'):
                a, _, c, d = next_regs

                regs[a] = regs[x] * regs[d]
                regs[c] = 0
                regs[d] = 0
                pc += 6
                continue

            # Ignore cpy instructions that try to copy a value into an
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

        elif cmd == "out":
            yield reg_or_val(regs, x)

        elif cmd == 'tgl':
            i = pc + reg_or_val(regs, x)
            try:
                ncmd, nx, ny = program[i]
            except IndexError:
                pass
            else:
                if ny == 'null':
                    program[i][0] = 'dec' if ncmd == 'inc' else 'inc'
                else:
                    program[i][0] = 'cpy' if ncmd == 'jnz' else 'jnz'

        pc += 1


def find_repeated_clock_signal(program, threshold=50):
    for a in count():
        for i, c in enumerate(emulate(program, a=a)):
            if c != (i % 2):
                break
            elif i > threshold:
                return a


PROGRAM = []

for line in fileinput.input():
    # Add null argument to pad inc/dec instructions
    instruction = line + ' null'
    PROGRAM.append(instruction.split()[:3])


print "Lowest candidate for value of a:", find_repeated_clock_signal(PROGRAM)
