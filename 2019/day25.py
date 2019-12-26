import sys
import fileinput
from itertools import combinations

from intcode import emulate

TAS = """\
south
take space law space brochure
south

take mouse
west
north
north
take wreath
south
south
east

south
take astrolabe
south
take mug
north
north

north
west
take sand
north
take manifold
south
west
take monolith
west
"""

items = ['space law space brochure', 'mouse', 'sand', 'wreath', 'manifold', 'astrolabe', 'mug', 'monolith']

for i in range(1, len(items) + 1):
    for comb in combinations(items, i):
        for item in items:
            TAS += "drop {}\n".format(item)

        for c in comb:
            TAS += "take {}\n".format(c)

        TAS += 'west\n'


TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 10000

vm = emulate(TAPE, [ord(c) for c in TAS][::-1])
try:
    while True:
        resp = chr(next(vm))
        sys.stdout.write(resp)

except Exception as e:
    pass
