import re
import math
import operator
from functools import total_ordering


LETTERS = [x for x in 'abcdefghijklmnopqrstuvwxyz']
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


def parse_line(line, regex):
    return re.match(regex, line).groups()


def mul(lst):
    """Like sum(), but for multiplication."""
    return reduce(operator.mul, lst, 1)  # NOQA


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def factors(n):
    """Returns the factors of n."""
    return sorted(
        x for tup in (
            [i, n // i] for i in range(1, int(n ** 0.5) + 1)
            if n % i == 0)
        for x in tup)


def memoize(f):
    """Simple dictionary-based memoization decorator"""
    cache = {}

    def _mem_fn(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    _mem_fn.cache = cache
    return _mem_fn


def _eratosthenes(n):
    """http://stackoverflow.com/a/3941967/239076"""
    # Initialize list of primes
    _primes = [True] * n

    # Set 0 and 1 to non-prime
    _primes[0] = _primes[1] = False

    for i, is_prime in enumerate(_primes):
        if is_prime:
            yield i

            # Mark factors as non-prime
            for n in xrange(i * i, n, i):  # NOQA
                _primes[n] = False


def primes(n):
    """Return a list of primes from [2, n)"""
    return list(_eratosthenes(n))


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
