import fileinput
from utils import resolve_mapping
from collections import Counter, defaultdict, deque, namedtuple  # NOQA

foods = []

for y, line in enumerate(fileinput.input()):
    line = line.strip()

    ingredients, allergens = line.split(' (')
    allergens = allergens.replace(')', '').replace(',', '').split(' ')[1:]

    foods.append((ingredients.split(' '), allergens))

ing_to_all = defaultdict(set)
all_to_ing = defaultdict(set)

for ingredients, allergens in foods:
    for i in ingredients:
        for a in allergens:
            ing_to_all[i].add(a)
            all_to_ing[a].add(i)

candidates = defaultdict(set)
resolved_ing = set()

for a in all_to_ing:
    poss = []
    for ingredients, allergens in foods:
        if a in allergens:
            poss.append(ingredients)

    if poss:
        resolve = set(poss[0])
        for p in poss[1:]:
            resolve &= set(p)

        for r in resolve:
            candidates[a].add(r)
            resolved_ing.add(r)
    else:
        print "empty poss", a

good = set(ing_to_all) - resolved_ing
print len(good)

tot = 0
for ingredients, allergens in foods:
    for i in ingredients:
        if i in good:
            tot += 1


print tot

resolved = resolve_mapping(candidates)

l = []
for r in sorted(resolved):
    l.append(resolved[r])

print ','.join(l)
