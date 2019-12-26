"""
Credit to /u/mcpower_ for explaining the number theory involved in Part 2:
https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
"""

import fileinput


def solve_part_1(actions):
    CARDS = 10007
    POS = 2019

    for action, n in actions:
        if action == 'deal':
            if n is None:
                POS = (CARDS - 1) - POS
            else:
                POS = (n * POS) % CARDS
        else:
            if POS >= n:
                POS -= n
            else:
                POS = (CARDS - (n - POS))

    return POS


def solve_part_2(actions):
    CARDS = 119315717514047
    SHUFFLES = 101741582076661

    def modinv(n, p):
        """Returns the inverse of n mod p, assuming p is prime."""
        return pow(n, p - 2, p)

    def get_card(offset, increment, i):
        """Returns the ith card in the sequence given its offset and increment."""
        return (offset + i * increment) % CARDS

    def get_sequence(iterations, increment_mul, offset_diff):
        """Returns the final increment and offset after the given number of iterations."""
        increment = pow(increment_mul, iterations, CARDS)
        offset = (offset_diff * (1 - increment) * modinv(1 - increment_mul, CARDS)) % CARDS
        return increment, offset

    # `increment` is the difference between two adajcent numbers
    increment = 1

    # `offset` is the first number in the sequence
    offset = 0

    for action, n in actions:
        if action == 'deal':
            # deal into new stack
            if n is None:
                # The sequence gets reversed...
                increment = (increment * -1) % CARDS

                # ...and shifted one to the left
                offset = (offset + increment) % CARDS

            # deal with increment n
            else:
                increment = (increment * modinv(n, CARDS)) % CARDS

        # cut n
        else:
            offset = (offset + (n * increment)) % CARDS


    inc, off = get_sequence(SHUFFLES, increment, offset)
    return get_card(off, inc, 2020)


actions = []

for line in fileinput.input():
    line = line.strip()
    inst = line.split()
    verb = inst[0]
    if verb == 'cut':
        actions.append(('cut', int(inst[1])))

    else:
        if inst[1] == 'into':
            actions.append(('deal', None))
        else:
            actions.append(('deal', int(inst[-1])))


print "Position of card 2019:", solve_part_1(actions)
print "Card ending up in position 2020:", solve_part_2(actions)
