import fileinput

SNAFU_DIGITS = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
REVERSE_DIGITS = {v: k for k, v in SNAFU_DIGITS.items()}


def decimal_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def snafu_to_decimal(s):
    n = 0
    for i, c in enumerate(reversed(s)):
        n += SNAFU_DIGITS[c] * (5 ** i)
    return n


def decimal_to_snafu(n):
    quinary_digits = decimal_to_base(n, 5)
    snafu_digits = []

    # Iterate in reverse order through the base-5 digits; if a number larger
    # than 2 is found, add 1 to the next "place" and take the remainder.
    for i, n in enumerate(reversed(quinary_digits)):
        if n >= 3:
            quinary_digits[-(i+2)] += 1
            n -= 5
        snafu_digits = [REVERSE_DIGITS[n]] + snafu_digits

    return ''.join(snafu_digits)


# Read problem input and solve problem.
total = sum(snafu_to_decimal(line.strip()) for line in fileinput.input())
print("Part 1:", decimal_to_snafu(total))
