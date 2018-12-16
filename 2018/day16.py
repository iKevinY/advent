import fileinput
from utils import parse_nums


def compute(regs, a, b):
    addr = regs[a] + regs[b]
    addi = regs[a] + b
    mulr = regs[a] * regs[b]
    muli = regs[a] * b
    banr = regs[a] & regs[b]
    bani = regs[a] & b
    borr = regs[a] | regs[b]
    bori = regs[a] | b
    setr = regs[a]
    seti = a
    gtir = int(a > regs[b])
    gtri = int(regs[a] > b)
    gtrr = int(regs[a] > regs[b])
    eqir = int(a == regs[b])
    eqri = int(regs[a] == b)
    eqrr = int(regs[a] == regs[b])
    return [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


NUM_OPCODES = 16

newlines = 0
on_program = False
samples = []
program = []

curr_sample = []

# Read problem input
for i, line in enumerate(fileinput.input()):
    nums = parse_nums(line)

    if line == '\n':
        newlines += 1
    elif newlines == 3:
        on_program = True
    else:
        newlines = 0

    if on_program:
        program.append(nums)
        continue

    if i % 4 != 3:
        curr_sample.append(nums)
    else:
        samples.append(curr_sample)
        curr_sample = []

    last_line = line


# Solve part 1 and narrow down possible opcode mapping
three_count = 0
poss_mapping = {n: set(range(NUM_OPCODES)) for n in range(NUM_OPCODES)}

for before, instr, after in samples:
    opcode, a, b, c = instr
    results = compute(before, a, b)

    matches = 0
    for i, n in enumerate(results):
        if n == after[c]:
            matches += 1
        else:
            poss_mapping.get(opcode, set()).discard(i)

    if matches >= 3:
        three_count += 1

print "Samples behaving like 3+ opcodes:", three_count


# Iteratively reduce all possiblities for opcodes
mapping = {}

while len(mapping) < NUM_OPCODES:
    for opcode, instrs in poss_mapping.items():
        if len(instrs) == 1:
            instr = next(iter(instrs))
            if instr not in mapping.values():
                next_opcode = opcode
                next_instr = instr
                break

    mapping[next_opcode] = next_instr
    del poss_mapping[next_opcode]

    for opcode, instrs in poss_mapping.items():
        if opcode != next_opcode:
            instrs.discard(next_instr)


# Solve part 2
REGS = [0, 0, 0, 0]
for op, a, b, c in program:
    REGS[c] = compute(REGS, a, b)[mapping[op]]

print "Value in register 0:", REGS[0]
