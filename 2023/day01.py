import fileinput

DIGITS = {str(i): i for i in range(1, 10)}

DIGIT_WORDS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def calibration(line, dictionary):
    start = None
    end = None
    for i, c in enumerate(line):
        for key, val in dictionary.items():
            if line[i:].startswith(key):
                if start is None:
                    start = val
                end = val

    return start * 10 + end


part_1 = 0
part_2 = 0

for line in fileinput.input():
    part_1 += calibration(line, DIGITS)
    part_2 += calibration(line, DIGITS | DIGIT_WORDS)

print("Part 1:", part_1)
print("Part 2:", part_2)

