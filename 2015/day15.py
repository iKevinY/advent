import fileinput
import itertools
import re

def mul(vals):
    ret = 1
    for x in vals:
        ret *= x
    return ret

ingredients = [[int(n) for n in re.findall(r'\w+ (-?\d+)', line)] for line in fileinput.input()]

cookies = []

for combo in itertools.combinations_with_replacement(ingredients, 100):  # 100 teaspoons of ingredients
    cookies.append([max(0, sum(c)) for c in tuple(zip(*combo))])

print "Best cookie total: %d" % max(mul(c[:-1]) for c in cookies)
print "Best 500 calories: %d" % max(mul(c[:-1]) for c in cookies if c[-1] == 500)
