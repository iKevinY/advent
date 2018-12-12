import fileinput


INITIAL = None
RULES = {}
GENS = 200  # 200 generations is safe for the automata to converge
TARGET_GEN = 50000000000

for i, line in enumerate(fileinput.input()):
    if i == 0:
        INITIAL = line.split()[-1]
    elif i >= 2:
        a, _, b = line.split()
        RULES[a] = b


state = ['.'] * GENS + list(INITIAL) + ['.'] * GENS
pot_sums = []

for it in range(GENS):
    amt = sum(i - GENS for i, p in enumerate(state) if p == '#')
    pot_sums.append(amt)

    next_state = ['.'] * len(state)
    for i in range(len(state) - 2):
        next_state[i + 2] = RULES.get(''.join(state[i:i+5]), '.')

    state = next_state

print "Sum of plants after 20 generations:", pot_sums[20]

growth_per_gen = pot_sums[-1] - pot_sums[-2]
remaining_gens = TARGET_GEN - GENS + 1
print "Sum after 50000000000 generations:", growth_per_gen * remaining_gens + pot_sums[-1]
