import fileinput
from collections import Counter


part_1 = 0
part_2_cards = Counter()

for line in fileinput.input():
    card, rest = line.split(': ')
    card_id = int(card[5:])

    winning, your = rest.split(' | ')
    winning = set(int(n) for n in winning.split())
    your = [int(n) for n in your.split()]

    # Add the "original" scratchcard as one of the copies.
    part_2_cards[card_id] += 1

    matches = 0
    for n in your:
        if n in winning:
            matches += 1

    if matches > 0:
        part_1 += 2 ** (matches - 1)

    for copy_id in range(card_id + 1, card_id + matches + 1):
        part_2_cards[copy_id] += part_2_cards[card_id]

print("Part 1:", part_1)
print("Part 2:", sum(part_2_cards.values()))

