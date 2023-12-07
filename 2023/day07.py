import fileinput
from collections import Counter


def rank(hand, part_2=False):
    # Special-case JJJJJ; other hands Js just become the most common card.
    if part_2 and hand != 'JJJJJ':
        no_jokers = Counter(c for c in hand if c != 'J').most_common()
        hand = hand.replace('J', no_jokers[0][0])

    cmn = Counter(hand).most_common()

    # Five of a Kind
    if cmn[0][1] == 5:
        return 6

    # Four of a Kind
    elif cmn[0][1] == 4:
        return 5

    # Full House / Three of a Kind (based on second-most common card)
    elif cmn[0][1] == 3:
        return 2 + cmn[1][1]

    # Two Pair / One Pair (based on second-most common card)
    elif cmn[0][1] == 2:
        return cmn[1][1]

    return 0


def tiebreak(hand, part_2=False):
    return tuple(card_score(c, part_2) for c in hand)


def card_score(card, part_2=False):
    if part_2:
        return 'J23456789TQKA'.index(card)
    else:
        return '23456789TJQKA'.index(card)


# Parse problem input.
hands = []
for line in fileinput.input():
    hand, bid = line.split()
    hands.append((hand, int(bid)))


# Solve part 1.
part_1 = 0
for i, (hand, bid) in enumerate(sorted(hands, key=lambda h: (rank(h[0]), tiebreak(h[0]))), start=1):
    part_1 += i * bid

print("Part 1:", part_1)


# Solve part 2.
part_2 = 0
for i, (hand, bid) in enumerate(sorted(hands, key=lambda h: (rank(h[0], part_2=True), tiebreak(h[0], part_2=True))), start=1):
    part_2 += i * bid

print("Part 2:", part_2)
