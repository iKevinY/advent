import fileinput
from string import maketrans
from itertools import permutations


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

SEGMENTS_MAP = {v: str(k) for k, v in DIGIT_MAP.items()}

VALID_SEGMENTS = set(v for v in DIGIT_MAP.values())

ALL_SEGMENTS = 'abcdefg'

part_1 = 0
part_2 = 0

for y, line in enumerate(fileinput.input()):
    input, output = line.strip().split(' | ')

    # Solve part 1
    for word in output.split():
        if len(word) in UNIQUES.values():
            part_1 += 1

    # Solve part 2
    for perm in permutations('abcdefg', 7):
        table = maketrans(ALL_SEGMENTS, perm)

        for word in input.split():
            new_word = word.translate(table)
            new_word = ''.join(sorted(new_word))

            if new_word not in VALID_SEGMENTS:
                break
        else:
            ans = ''
            for word in output.split():
                new_word = word.translate(table)
                new_word = ''.join(sorted(new_word))
                ans += SEGMENTS_MAP[new_word]

            part_2 += int(ans)


print "Part 1:", part_1
print "Part 2:", part_2

