import re
import fileinput
from collections import Counter

from utils import parse_line


formulas = {}
from_ore = set()

for i, line in enumerate(fileinput.input()):
    inp, out = line.split(' => ')
    re_form = r'(\d+) (.+)'

    inputs = [parse_line(re_form, i) for i in inp.split(', ')]
    out = parse_line(re_form, out)
    formulas[out[1]] = (out[0], inputs)

    if inputs[0][1] == 'ORE':
        from_ore.add(out[1])


def create_fuel(n):
    excesses = Counter()

    def needed(n, type):
        ret = Counter()

        if type in from_ore:
            ret[type] += n
            return ret

        nn, inputs = formulas[type]

        ratio = ((n - 1) // nn) + 1

        for m, t in inputs:
            ret[t] += m * ratio

        excess = ratio * nn - n
        excesses[type] += excess

        return ret


    resolve = Counter()
    resolve['FUEL'] = n

    while True:
        new_resolve = Counter()
        for type, amt in resolve.items():
            new_resolve += needed(amt, type)

        if resolve == new_resolve:
            break

        for k, v in new_resolve.items():
            if k in excesses:
                new_resolve[k] -= excesses[k]
                excesses[k] = 0

        resolve = new_resolve

    ore = 0

    for type, required in resolve.items():
        formula = formulas[type]
        created = formula[0]
        ore_needed = formula[1][0][0]
        done = 0

        ratio = ((required - 1) // created) + 1
        ore += ratio * ore_needed

        excesses[type] += (required - ratio)

    return ore


one_fuel = create_fuel(1)
print "Ore to create 1 FUEL:", one_fuel

trillion = 1000000000000
worst_case = trillion // one_fuel
lo, hi = worst_case, worst_case * 2

while lo < hi:
    mid = (lo + hi + 1) // 2
    ore = create_fuel(mid)

    if ore > trillion:
        hi = mid - 1
    else:
        lo = mid

print "Maximum FUEL with 1 trillion ORE:", lo
