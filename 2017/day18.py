import fileinput
from collections import deque, defaultdict


def duet_program(instrs, snd_q, rcv_q, pid=None):
    regs = defaultdict(int)
    if pid is not None:
        regs['p'] = pid

    pc = 0
    sends = 0

    while 0 <= pc < len(instrs):
        op, x, y = instrs[pc]
        y = regs[y] if y.isalpha() else int(y)

        if op == 'snd':
            snd_q.appendleft(regs[x] if x.isalpha() else int(x))
            sends += 1
        elif op == 'set':
            regs[x] = y
        elif op == 'add':
            regs[x] += y
        elif op == 'mul':
            regs[x] *= y
        elif op == 'mod':
            regs[x] %= y
        elif op == 'rcv':
            if len(rcv_q) > 0:
                regs[x] = rcv_q.pop()
            else:
                yield op, sends
                continue
        elif op == 'jgz':
            if (regs[x] if x.isalpha() else int(x)) > 0:
                pc += y
                continue

        pc += 1

    raise StopIteration


# Read puzzle input
INSTRS = []

for line in fileinput.input():
    instr = line.strip() + ' foo'
    op, x, y = instr.split()[:3]
    INSTRS.append((op, x, y))


# Part 1
snd_queue = deque()
program = duet_program(INSTRS, snd_queue, deque())
next(program)

print "Value of recovered frequency:", snd_queue[0]


# Part 2
queue_0 = deque()
queue_1 = deque()

program_0 = duet_program(INSTRS, queue_1, queue_0, pid=0)
program_1 = duet_program(INSTRS, queue_0, queue_1, pid=1)

last_op_0 = None
last_op_1 = None

while not (last_op_0 == last_op_1 == 'rcv' and len(queue_0) == len(queue_1) == 0):
    last_op_0, _ = next(program_0)
    last_op_1, sends = next(program_1)

print "Number of times program 1 sent a value:", sends
