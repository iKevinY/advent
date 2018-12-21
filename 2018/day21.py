import fileinput


def emulate(program, ip_reg):
    """
    Emulate the program while watching register 1, as this program is a
    PRNG that will terminate if regs[0] == regs[1] at instruction 28.
    """
    pc = 0
    regs = [0, 0, 0, 0, 0, 0]

    seen = set()
    first_halt = None
    last_halt = None

    while 0 <= pc < len(program):
        cmd, a, b, c = program[pc]
        regs[ip_reg] = pc

        if cmd == 'addr':   regs[c] = regs[a] + regs[b]
        elif cmd == 'addi': regs[c] = regs[a] + b
        elif cmd == 'mulr': regs[c] = regs[a] * regs[b]
        elif cmd == 'muli': regs[c] = regs[a] * b
        elif cmd == 'banr': regs[c] = regs[a] & regs[b]
        elif cmd == 'bani': regs[c] = regs[a] & b
        elif cmd == 'borr': regs[c] = regs[a] | regs[b]
        elif cmd == 'bori': regs[c] = regs[a] | b
        elif cmd == 'setr': regs[c] = regs[a]
        elif cmd == 'seti': regs[c] = a
        elif cmd == 'gtir': regs[c] = int(a > regs[b])
        elif cmd == 'gtri': regs[c] = int(regs[a] > b)
        elif cmd == 'gtrr': regs[c] = int(regs[a] > regs[b])
        elif cmd == 'eqir': regs[c] = int(a == regs[b])
        elif cmd == 'eqri': regs[c] = int(regs[a] == b)
        elif cmd == 'eqrr': regs[c] = int(regs[a] == regs[b])

        # This is where the program checks to break and halt, so
        # take note of whatever value is in register 1.
        if pc == 28:
            if first_halt is None:
                first_halt = regs[1]
            elif regs[1] in seen:
                break
            else:
                last_halt = regs[1]
                seen.add(regs[1])

        pc = regs[ip_reg]
        pc += 1

    return first_halt, last_halt


PROGRAM = []
IP = None

for line in fileinput.input():
    parts = line.split()

    if fileinput.isfirstline():
        IP = int(parts[1])
    else:
        a, b, c = [int(x) for x in parts[1:4]]
        PROGRAM.append((parts[0], a, b, c))

first_halt, last_halt = emulate(PROGRAM, IP)

print "Lowest value for register 0 with fewest cycles:", first_halt
print "Lowest value for register 0 with the most cycles:", last_halt
