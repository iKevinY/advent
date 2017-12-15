import fileinput

SEEDS = [int(l.split()[-1]) for l in fileinput.input()]

FACTOR_A = 16807
FACTOR_B = 48271
MODULO = 2**31 - 1

# Part 1
gen_a, gen_b = SEEDS
count = 0

for i in range(40000000):
    gen_a = (gen_a * FACTOR_A) % MODULO
    gen_b = (gen_b * FACTOR_B) % MODULO

    if (gen_a & 0xffff) == (gen_b & 0xffff):
        count += 1

print "Judge's first count:", count


# Part 2
gen_a, gen_b = SEEDS
count = 0

for i in range(5000000):
    gen_a = (gen_a * FACTOR_A) % MODULO
    while gen_a % 4 != 0:
        gen_a = (gen_a * FACTOR_A) % MODULO

    gen_b = (gen_b * FACTOR_B) % MODULO
    while gen_b % 8 != 0:
        gen_b = (gen_b * FACTOR_B) % MODULO

    if (gen_a & 0xffff) == (gen_b & 0xffff):
        count += 1

print "Judge's second count:", count
