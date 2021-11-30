import fileinput
from copy import deepcopy
from utils import parse_nums

TAPE = []

for line in fileinput.input():
    ins = line.split(' ')[0]
    TAPE.append([ins, parse_nums(line)])


def emulate(tape, pc=0, acc=0):
    """Returns (acc, pc, loop_detected)"""
    seen = set()
    while pc < len(tape):
        if pc in seen:
            return (acc, pc, True)
        else:
            seen.add(pc)

        ins, ops = tape[pc]

        if ins == 'acc':
            acc += ops[0]
            pc += 1
        elif ins == 'jmp':
            pc += ops[0]
        else:
            pc += 1

    return (acc, pc, False)


print "ACC at repeated instruction:", emulate(TAPE)[0]

for i in range(len(TAPE)):
    tape = deepcopy(TAPE)

    if tape[i][0] == 'acc':
        continue
    else:
        if tape[i][0] == 'jmp':
            tape[i][0] = 'nop'
        else:   # ins == 'nop'
            tape[i][0] = 'jmp'

    acc, pc, loop_detected = emulate(tape)
    if not loop_detected:
        print "ACC with modified termination:", acc
