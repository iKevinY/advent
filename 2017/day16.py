import fileinput
from collections import deque


def perform_dance(progs, moves):
    for m in moves:
        if m[0] == 's':
            progs.rotate(int(m[1:]))

        else:
            a, b = m[1:].split('/')

            if m[0] == 'x':
                a = int(a)
                b = int(b)
            else:
                # deque.index() only supported in Python 3.5+
                progs_lst = list(progs)
                a = progs_lst.index(a)
                b = progs_lst.index(b)

            progs[a], progs[b] = progs[b], progs[a]


MOVES = fileinput.input()[0].strip().split(',')
PROGS = [chr(x) for x in range(ord('a'), ord('p') + 1)]

# Part 1
progs = deque(PROGS)
perform_dance(progs, MOVES)
print "Order of programs after first dance:", ''.join(progs)

# Part 2
progs = deque(PROGS)
order = ''.join(progs)
past_orders = []
cycle_len = 0

while order not in past_orders:
    past_orders.append(order)
    perform_dance(progs, MOVES)
    order = ''.join(progs)
    cycle_len += 1

# Now we know the length of the cycle, so just compute the order
# after the billionth dance using modular arithmetic.
idx = 1000000000 % cycle_len
print "Order of programs after one billion dances:", past_orders[idx]
