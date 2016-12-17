import fileinput

PRESENTS = int(fileinput.input()[0].strip())

def factors(n):
    return set(x for tup in ([i, n//i]
                for i in range(1, int(n**0.5)+1) if n % i == 0) for x in tup)

house = 1

while True:
    if sum(factors(house)) * 10 >= PRESENTS:
        print "Lowest house number #1:", house
        break
    house += 1

house = 1

while True:
    if sum(x for x in factors(house) if (x * 50 >= house)) * 11 >= PRESENTS:
        print "Lowest house number #2:", house
        break
    house += 1
