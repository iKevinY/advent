import fileinput
from collections import Counter, defaultdict, deque, namedtuple  # NOQA

# Read problem input.
data = ''.join([line for line in fileinput.input()])
groups = [g.split('\n') for g in data.split('\n\n')]


POLYMER = groups[0][0]
MAPPING = {}

for line in groups[1]:
    a, b = line.split(' -> ')
    MAPPING[a] = b


# COUNTS maps bigrams to their counts in the underlying polymer.
COUNTS = Counter()


for i in range(len(POLYMER)-1):
    COUNTS[POLYMER[i:i+2]] += 1


for iteration in range(1, 40 + 1):
    new_counts = Counter()

    for bigram, num in COUNTS.items():
        insertion = MAPPING[bigram]

        new_counts[bigram[0] + insertion] += num
        new_counts[insertion + bigram[1]] += num

    COUNTS = new_counts

    if iteration in (10, 40):
        # Compute counts of individual letters from bigram counts.
        letter_counts = Counter()

        for bigram, num in COUNTS.items():
            letter_counts[bigram[0]] += num
            letter_counts[bigram[1]] += num

        frequencies = zip(*letter_counts.most_common())[1]
        most = (frequencies[0] + 1) // 2
        least = (frequencies[-1] + 1) // 2
        print "Part 1:" if iteration == 10 else "Part 2:", most - least
