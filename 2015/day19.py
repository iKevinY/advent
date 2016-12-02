import fileinput
import itertools
import re
import sys

REPLACEMENTS = []
ELECTRONS = []
MOLECULE = ""
MOL_LEN = len(MOLECULE)

for line in fileinput.input():
    if "=>" in line:
        m = re.findall(r'\w+', line)
        if m[0] == "e":
            ELECTRONS.append(m[1])
        else:
            REPLACEMENTS.append(m)
    else:
        MOLECULE = line.strip()

print "Elements:", len(re.findall(r'[A-Z]', MOLECULE))
print "Rn/Ar:", len(re.findall(r'Rn', MOLECULE)), "* 2"
print "Y:", len(re.findall(r'Y', MOLECULE))

# molecule = MOLECULE

# reps = {m[1][::-1]: m[0][::-1]
#         for m in REPLACEMENTS}

# def rep(x):
#     return reps[x.group()]

# count = 0
# while molecule != 'e':
#     molecule = re.sub('|'.join(reps.keys()), rep, molecule, 1)
#     count += 1

# print(count)

sys.exit()


outs = set()

def molefy(mole):
    for old, new in REPLACEMENTS:
        for pos in (m.start() for m in re.finditer(old, mole)):
            new_string = mole[:pos] + new + mole[pos+len(old):]
            yield new_string

def delete(mole):
    for old, new in REPLACEMENTS:
        for pos in (m.start() for m in re.finditer(new, mole)):
            new_string = mole[:pos] + old + mole[pos+len(new):]
            yield new_string

def replace(old, new, s):
    for pos in (m.start() for m in re.finditer(new, s)):
        yield "{}{}{}".format(s[:pos], old, s[pos+len(new):])


LOWEST = 100000

def submol(m, i=1,):
    if m in ELECTRONS:
        LOWEST = min(LOWEST, i)

    for r in REPLACEMENTS:
        if r[1] in m:
            for x in replace(r[0], r[1], m):
                submol(x, i+1)


submol(MOLECULE)
print LOWEST

sys.exit()

iterations = 1
mols = set()
mols.add(MOLECULE)
new_mols = set()
# seen = set()

while True:
    iterations += 1
    for m in mols:
        for r in REPLACEMENTS:
            if r[1] in m:
                for x in replace(r[0], r[1], m):
                    if x in ELECTRONS:
                        print iterations
                        sys.exit()

                # if x not in seen:
                    new_mols.add(x)
                    # seen.add(x)

    if len(new_mols) == 0:
        sys.exit("BLALALLA")

    mols = new_mols
    new_mols = set()



# print len(outs)
