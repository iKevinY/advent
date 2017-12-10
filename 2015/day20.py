import fileinput

PRESENTS = int(fileinput.input()[0].strip())
CACHE = {}


def factors(n):
    if n in CACHE:
        return CACHE[n]

    CACHE[n] = set()

    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            CACHE[n] |= set([i, n//i])

    return CACHE[n]


house = 1
while sum(factors(house)) * 10 < PRESENTS:
    house += 1

print "Lowest house number #1:", house

house = 1
while sum(x for x in factors(house) if (x * 50 >= house)) * 11 < PRESENTS:
    house += 1

print "Lowest house number #2:", house
