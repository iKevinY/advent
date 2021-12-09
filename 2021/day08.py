import fileinput
from collections import Counter


UNIQUES = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}

DIGIT_MAP = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

REVERSE_MAP = {v: k for k, v in DIGIT_MAP.items()}

# a/c and d/g can both be diambiguated by 4,
# who has a unique segument count, and also
# contains c & d but not a & g.
SEGMENT_FREQ = {
    # 'a': 8,
    'b': 6,
    # 'c': 8,
    # 'd': 7,
    'e': 4,
    'f': 9,
    # 'g': 7,
}

REVERSE_FREQ = {v: k for k, v in SEGMENT_FREQ.items()}

part_1 = 0
part_2 = 0

for y, line in enumerate(fileinput.input()):
    input, output = line.strip().split(' | ')

    # Solve part 1
    for word in output.split():
        if len(word) in UNIQUES.values():
            part_1 += 1

    # Solve part 2
    for word in input.split():
        if len(word) == 4:
            four_segments = word

    frequencies = Counter(input.replace(' ', ''))

    print frequencies.most_common()
    # break

    mapping = {}
    for segment, count in frequencies.most_common():
        if count in REVERSE_FREQ:
            mapping[segment] = REVERSE_FREQ[count]
        elif count == 7:
            if segment in four_segments:
                mapping[segment] = 'd'
            else:
                mapping[segment] = 'g'
        elif count == 8:
            if segment in four_segments:
                mapping[segment] = 'c'
            else:
                mapping[segment] = 'a'

    code = ''
    for word in output.split():
        new_word = ''.join(sorted(mapping[l] for l in word))
        code += str(REVERSE_MAP[new_word])

    part_2 += int(code)


print "Part 1:", part_1
print "Part 2:", part_2

