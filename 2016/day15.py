import re
import fileinput
from utils import parse_line, mul


def button_timing(discs):
    """Returns the first time at which the button should be pressed."""
    largest_disc = max(discs)
    stride, initial_pos = largest_disc
    disc_num = discs.index(largest_disc) + 1

    i = (stride - initial_pos - disc_num) % stride

    while True:
        for time, (positions, initial) in enumerate(discs, start=i+1):
            if (initial + time) % positions != 0:
                break
        else:
            return i

        i += stride

# https://stackoverflow.com/a/9758173/239076
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def chinese_remainder_theorem(discs):
    M = mul(d[0] for d in discs)
    x = 0

    for i, (size, initial) in enumerate(discs, start=1):
        # Disc #2 has 17 positions; at time=0, it is at position 15.
        # => x \equiv (17 - 15 - 2) (mod 17)
        M_i = (M / size)
        x += (size - initial - i) *  M_i * modinv(M_i, size)

    return x


DISCS = []
DISC_RE = re.compile(r'Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).')

for line in fileinput.input():
    disc = parse_line(DISC_RE, line.strip())
    DISCS.append(disc)

# print "Timing to press button:", button_timing(DISCS)
# print "Timing with added disc:", button_timing(DISCS + [[11, 0]])
print "Timing to press button:", chinese_remainder_theorem(DISCS)
print "Timing with added disc:", chinese_remainder_theorem(DISCS + [[11, 0]])
