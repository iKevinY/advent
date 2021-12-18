import fileinput
from itertools import permutations


class Snail:
    def __init__(self, val, depth):
        self.val = val
        self.depth = depth

    def __repr__(self):
        return 'S({} @ {})'.format(self.val, self.depth)


def process_snailnum(s):
    """Turns a written snailfish number into a List[Snail]."""
    depth = -1
    snails = []

    for c in s:
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif '0' <= c <= '9':
            snails.append(Snail(int(c), depth))

    return snails


def reduce_num(snails):
    """
    Reduces a snailfish number by iteratively going through
    it until no more explosions or splits can be performed.
    """

    while True:
        did_explode = did_split = False
        i = 0

        while i < len(snails):
            s = snails[i]

            # Prefer explode
            if s.depth >= 4:
                # print "ex",
                l = snails[i]
                n = snails[i+1]

                # Process left explosion
                leftmost = False
                if i == 0:
                    snails[i] = Snail(0, s.depth - 1)
                    leftmost = True
                else:
                    p = snails[i-1]
                    snails[i-1] = Snail(p.val + l.val, p.depth)

                # Process right explosion
                rightmost = False
                if i+1 == len(snails) - 1:
                    snails[i+1] = Snail(0, n.depth - 1)
                    rightmost = True
                else:
                    nn = snails[i+2]
                    snails[i+2] = Snail(n.val + nn.val, nn.depth)

                if leftmost:
                    del snails[1]
                elif rightmost:
                    del snails[-2]
                else:
                    del snails[i+1]
                    snails[i] = Snail(0, l.depth - 1)

                did_explode = True
                break

            i += 1

        if not did_explode:
            i = 0
            while i < len(snails):
                s = snails[i]
                if s.val >= 10:
                    a = s.val // 2
                    b = (s.val + 1) // 2
                    assert a + b == s.val

                    snails = snails[:i] + [Snail(a, s.depth + 1), Snail(b, s.depth + 1)] + snails[i+1:]

                    did_split = True
                    break

                i += 1

        if not did_explode and not did_split:
            break

    return snails


def add_snails(la, lb):
    """Adds two snailfish numbers together."""
    res = []

    for x in la:
        res.append(Snail(x.val, x.depth + 1))
    for x in lb:
        res.append(Snail(x.val, x.depth + 1))

    res = reduce_num(res)

    return res


def magnitude(snails):
    """Returns the magnitude of a snailnum (iterative)."""
    while True:
        max_depth = 0

        i = 0
        for i in range(len(snails)):
            s = snails[i]
            max_depth = max(max_depth, s.depth)

        # Nothing more to reduce
        if max_depth == 0:
            break

        # Else, search and expand the leftmost pair
        expanded = False
        for i in range(len(snails)):
            s = snails[i]
            if s.depth == max_depth:
                n = snails[i+1]
                assert s.depth == n.depth
                ns = Snail(s.val * 3 + n.val * 2, s.depth - 1)

                snails = snails[:i] + [ns] + snails[i+2:]

                expanded = True
                break

    return snails[0].val * 3 + snails[1].val * 2


# Parse problem input.
SNAILS = [process_snailnum(l.strip()) for l in fileinput.input()]

# Solve part 1.
part_1_snails = reduce_num(SNAILS[0])
for s in SNAILS[1:]:
    part_1_snails = add_snails(part_1_snails, s)
print "Part 1:", magnitude(part_1_snails)

# Solve part 2.
print "Part 2:", max(magnitude(add_snails(a, b)) for a, b in permutations(SNAILS, 2))
