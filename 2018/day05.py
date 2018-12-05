import fileinput
from string import ascii_lowercase, ascii_uppercase


def reduce_polymer(poly, omit=None):
    if omit:
        poly = poly.replace(omit.upper(), '').replace(omit.lower(), '')
    else:
        poly = poly.replace('', '')

    while True:
        for (x, X) in zip(ascii_lowercase, ascii_uppercase):
            new = poly.replace(x + X, '').replace(X + x, '')
            if len(new) < len(poly):
                improved = True
                poly = new
                break
        else:
            return len(poly)


POLYMER = fileinput.input()[0].strip()


print "Units remaining after reaction:", reduce_polymer(POLYMER)
print "Best length after omitting one:", min(reduce_polymer(POLYMER, x) for x in ascii_lowercase)
