import fileinput
from intcode import emulate

TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 10000

walking = """\
OR D J
NOT C T
AND T J
NOT A T
OR T J
WALK
"""

running = """\
NOT C T
OR T J
NOT A T
OR T J
NOT B T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
"""

for instructions in (walking, running):
    program = [ord(c) for c in instructions]
    vm = emulate(TAPE, program)
    try:
        while True:
            resp = next(vm)
            chr(resp),
    except Exception as e:
        print "{} hull damage: {}".format(instructions.split()[-1], resp)
