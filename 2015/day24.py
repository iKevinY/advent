import fileinput
import itertools

PACKAGES = []

for line in fileinput.input():
    PACKAGES.append(int(line))

PACKAGES.reverse()

def quantum_package(packages, target_weight):
    for n in range(1, len(PACKAGES) - 2):
        found = False
        for p in itertools.combinations(PACKAGES, n):
            if sum(p) == target_weight:
                # print p
                yield p
                found = True

        if found:
            return

def prod(it):
    p = 1
    for i in it:
        p *= i
    return p

print "3-compartment package QE:", min(prod(c) for c in quantum_package(PACKAGES, sum(PACKAGES) / 3))
print "4-compartment package QE:", min(prod(c) for c in quantum_package(PACKAGES, sum(PACKAGES) / 4))
