import fileinput
from utils import factors


def emulate(program, ip_reg, start=0, cheat=False):
    """
    Emulate the program to load in the value we're solving for.

    Instruction 0 immediately jumps to 17 to begin the loading
    procedure; when we get back to instruction 1, register 1
    already contains the target number.
    """
    ip = 0
    regs = [start, 0, 0, 0, 0, 0]

    while 0 <= ip <= len(program):
        if ip == 1 and cheat:
            return sum(factors(regs[1]))

        cmd, a, b, c = program[ip]
        regs[ip_reg] = ip

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

        ip = regs[ip_reg]
        ip += 1

    return regs[0]


PROGRAM = []
IP = None

for line in fileinput.input():
    parts = line.split()

    if fileinput.isfirstline():
        IP = int(parts[1])
    else:
        a, b, c = [int(x) for x in parts[1:4]]
        PROGRAM.append((parts[0], a, b, c))


print "Value left in register 0 when initialized to 0:", emulate(PROGRAM, IP, start=0)
print "Value left in register 0 when initialized to 1:", emulate(PROGRAM, IP, start=1, cheat=True)
