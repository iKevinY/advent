import sys
import fileinput
from hashlib import md5
from collections import defaultdict

from utils import memoize


@memoize
def salty_md5(salt, i):
    return md5(salt + str(i)).hexdigest()


@memoize
def stretched_md5(salt, i):
    h = salty_md5(salt, i)
    for _ in range(2016):
        h = md5(h).hexdigest()

    return h


def first_triple(s):
    for i in range(len(s) - 2):
        a, b, c = s[i:i+3]
        if a == b == c:
            return a


def all_quintuplets(s):
    for i in range(len(s) - 4):
        a, b, c, d, e = s[i:i+5]
        if a == b == c == d == e:
            yield a


def find_pad_key_64(salt, hash_fn):
    valid_keys = 0
    quintuplets = defaultdict(set)
    i = 0

    while True:
        digest = hash_fn(salt, i)

        for quint in all_quintuplets(digest):
            quintuplets[i].add(quint)

        if i >= 1000:
            n = i - 1000
            triple = first_triple(hash_fn(salt, n))
            for j in range(n + 1, n + 1001):
                if triple in quintuplets[j]:
                    valid_keys += 1
                    sys.stdout.write('.')
                    sys.stdout.flush()

                    if valid_keys >= 64:
                        return n

                    break

        i += 1


if __name__ == "__main__":
    SALT = fileinput.input()[0].strip()

    print "Index of 64th one-time pad key", find_pad_key_64(SALT, salty_md5)
    print "Index of key-stretched pad key", find_pad_key_64(SALT, stretched_md5)
