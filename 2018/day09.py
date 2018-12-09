import fileinput
from utils import parse_nums


class Node:
    def __init__(self, val, n=None, p=None):
        self.val = val
        self.next = n
        self.prev = p


PLAYERS, MARBLES = parse_nums(fileinput.input()[0])
scores = [0] * PLAYERS
player = 0

curr = Node(0)
curr.next = curr
curr.prev = curr

for m in range(1, MARBLES * 100):
    if m % 23 == 0:
        scores[player] += m
        for _ in range(7):
            curr = curr.prev

        scores[player] += curr.val
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        curr = curr.prev.next
    else:
        curr = curr.next
        node = Node(m, p=curr, n=curr.next)
        curr.next.prev = node
        curr.next = node
        curr = node

    player = (player + 1) % PLAYERS

    if m == MARBLES:
        print "Winning elf's score:", max(scores)

print "Newer winning score:", max(scores)
