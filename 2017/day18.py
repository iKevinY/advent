import fileinput
from collections import deque, defaultdict


def duet_program(ops, regs, snd_q, rcv_q, part_1=False):
    pc = 0
    sends = 0

    while 0 <= pc < len(ops):
        op, x, y = ops[pc]
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
            if part_1:
                raise StopIteration
            else:
                if len(rcv_q) > 0:
                    regs[x] = rcv_q.pop()
                else:
                    yield op, sends
                    continue
        elif op == 'jgz':
            if (regs[x] if x.isalpha() else int(x)) > 0:
                pc += y
                yield op, sends
                continue

        pc += 1
        yield op, sends

    raise StopIteration


# Read puzzle input
OPS = []

for line in fileinput.input():
    parts = line.strip().split()
    op, x = parts[:2]
    y = 'foo' if len(parts) == 2 else parts[2]
    OPS.append((op, x, y))


# Part 1
regs = defaultdict(int)
snd_queue = deque()

for _ in duet_program(OPS, regs, snd_queue, deque(), part_1=True):
    pass

print "Value of recovered frequency:", snd_queue[0]


# Part 2
regs_0 = defaultdict(int)
regs_1 = defaultdict(int)
regs_0['p'] = 0
regs_1['p'] = 1

queue_0 = deque()
queue_1 = deque()

last_op_0 = None
last_op_1 = None

program_0 = duet_program(OPS, regs_0, queue_1, queue_0)
program_1 = duet_program(OPS, regs_1, queue_0, queue_1)

while not (last_op_0 == last_op_1 == 'rcv' and len(queue_0) == len(queue_1) == 0):
    last_op_0, _ = next(program_0)
    last_op_1, sends = next(program_1)

print "Number of times program 1 sent a value:", sends
