import fileinput

from intcode import emulate

# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 100000  # Pad memory

print "BOOST keycode:", next(emulate(TAPE, [1]))
print "Coordinates of distress signal:", next(emulate(TAPE, [2]))
