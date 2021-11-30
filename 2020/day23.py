NUM_CUPS = 1000000
ITERS = 10000000

class Cup:
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "{} -> ({}) -> {}".format(self.prev.n, self.n, self.next.n)

labeling = [int(x) for x in raw_input()]
cup_ptrs = {}

for i in range(1, NUM_CUPS + 1):
    cup_ptrs[i] = Cup(i)

curr_cup = None
prev = None
for n in labeling:
    if curr_cup is None:
        curr_cup = cup_ptrs[n]
        prev = curr_cup
    else:
        cup_ptrs[n].prev = prev
        prev.next = cup_ptrs[n]
        prev = cup_ptrs[n]

for n in range(len(labeling) + 1, NUM_CUPS + 1):
    cup_ptrs[n].prev = prev
    prev.next = cup_ptrs[n]
    prev = cup_ptrs[n]

curr_cup.prev = prev
prev.next = curr_cup

for move in range(ITERS):
    curr = curr_cup.n

    # Pick up three cups
    a = curr_cup.next
    b = a.next
    c = b.next

    # Cup spacing adjusted
    a.prev.next = c.next
    c.next.prev = a.prev

    dval = curr - 1
    if dval == 0:
        dval = NUM_CUPS
    while dval == a.n or dval == b.n or dval == c.n:
        dval -= 1
        if dval == 0:
            dval = NUM_CUPS

    dest_cup = cup_ptrs[dval]
    tmp_cup = dest_cup.next

    dest_cup.next = a
    a.prev = dest_cup

    c.next = tmp_cup
    tmp_cup.prev = c

    # Move current cup to the next cup.
    curr_cup = curr_cup.next

print cup_ptrs[1].next.n * cup_ptrs[1].next.next.n
