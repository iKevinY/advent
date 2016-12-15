import re
import fileinput
import itertools
from utils import parse_line


def button_timing(discs):
    """Returns the first time at which the button should be pressed."""
    for i in itertools.count():
        for time, (positions, initial) in enumerate(discs, start=i+1):
            if (initial + time) % positions != 0:
                break
        else:
            return i


DISCS = []
DISC_RE = re.compile(r'Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).')

for line in fileinput.input():
    disc = parse_line(DISC_RE, line.strip())
    DISCS.append(disc)

print "Timing to press button:", button_timing(DISCS)
print "Timing with added disc:", button_timing(DISCS + [(11, 0)])
