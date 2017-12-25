import fileinput
from collections import defaultdict

from utils import parse_line

PROG = {}

# Parse puzzle input
for i, line in enumerate(fileinput.input()):
    if i == 0:
        STATE = parse_line(r'Begin in state (\w+).', line)[0]
    elif i == 1:
        STEPS = int(parse_line(r'Perform a diagnostic checksum after (\d+) steps.', line)[0])

    if i <= 2:
        continue

    if i % 10 == 3:
        start = parse_line(r'In state (\w+):', line)[0]
    elif i % 10 == 5:
        write_0 = parse_line(r'    - Write the value (\d+).', line)[0]
    elif i % 10 == 6:
        move_0 = parse_line(r'    - Move one slot to the (\w+).', line)[0]
        move_0 = 1 if move_0 == 'right' else -1
    elif i % 10 == 7:
        next_0 = parse_line(r'    - Continue with state (\w+).', line)[0]
    elif i % 10 == 9:
        write_1 = parse_line(r'    - Write the value (\d+).', line)[0]
    elif i % 10 == 0:
        move_1 = parse_line(r'    - Move one slot to the (\w+).', line)[0]
        move_1 = 1 if move_1 == 'right' else -1
    elif i % 10 == 1:
        next_1 = parse_line(r'    - Continue with state (\w+).', line)[0]
        PROG[start] = ((write_0, move_0, next_0), (write_1, move_1, next_1))


TAPE = defaultdict(int)
CURSOR = 0

for _ in range(STEPS):
    write, dx, ns = PROG[STATE][TAPE[CURSOR]]
    TAPE[CURSOR] = write
    CURSOR += dx
    STATE = ns

print "Diagnostic checksum:", sum(x for x in TAPE.values())
