import math
import operator
from functools import total_ordering


LETTERS = [x for x in 'abcdefghijklmnopqrstuvwxyz']
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


def mul(lst):
    """Like sum(), but for multiplication."""
    return reduce(operator.mul, lst, 1)


def factors(n):
    """Returns the factors of n."""
    return sorted(
        x for tup in (
            [i, n//i] for i in range(1, int(n**0.5) + 1)
            if n % i == 0)
        for x in tup)


def primes(n):
    """Returns the sorted list of primes in the range [2, n]"""
    limit = n + 1
    not_prime = set()
    primes = []

    for i in range(2, limit):
        if i in not_prime:
            continue

        for f in range(i*2, limit, i):
            not_prime.add(f)

        primes.append(i)

    return primes


@total_ordering
class Point:
    """Simple 2-dimensional point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.manhattan < other.manhattan

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
