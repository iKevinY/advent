import fileinput
import re

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


def replace(old, new, s):
    for pos in (m.start() for m in re.finditer(old, s)):
        yield "{}{}{}".format(s[:pos], new, s[pos+len(old):])


single_replacements = set()

for old, new in REPLACEMENTS:
    if old in MOLECULE:
        for new_mol in replace(old, new, MOLECULE):
            single_replacements.add(new_mol)

print "Distinct molecules after one replacement:", len(single_replacements)


elements = len(re.findall(r'[A-Z]', MOLECULE))
radon = len(re.findall(r'Rn', MOLECULE))
yttrium = len(re.findall(r'Y', MOLECULE))

# print "Elements:", elements
# print "Rn/Ar:", radon, "* 2"
# print "Y:", yttrium
# print "|E| - (Rn + Ar) - 2*Y - 1 = n"

print "Fewest steps from e to medicine:", elements - (2 * radon) - (2 * yttrium) - 1
