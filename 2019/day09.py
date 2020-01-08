import fileinput

from intcode import emulate

# Read input
TAPE = [int(x) for x in fileinput.input()[0].split(',')]

print "BOOST keycode:", next(emulate(TAPE, [1]))
print "Coordinates of distress signal:", next(emulate(TAPE, [2]))
