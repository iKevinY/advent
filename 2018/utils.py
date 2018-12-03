import re
import math
import hashlib
import operator
from functools import total_ordering


LETTERS = [x for x in 'abcdefghijklmnopqrstuvwxyz']
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


def parse_line(regex, line):
    ret = []
    for match in re.match(regex, line).groups():
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)

    return ret


def parse_nums(line):
    return [int(n) for n in re.findall(r'\d+', line)]


def new_table(val, width, height):
    return [[val for _ in range(width)] for _ in range(height)]


def transposed(matrix):
    """Returns the transpose of the given matrix."""
    return [list(r) for r in zip(*matrix)]


def rotated(matrix):
    """Returns the given matrix rotated 90 degrees clockwise."""
    return [list(r) for r in zip(*matrix[::-1])]


def mul(lst):
    """Like sum(), but for multiplication."""
    return reduce(operator.mul, lst, 1)  # NOQA


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def all_unique(lst):
    return len(lst) == len(set(lst))


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
            for j in xrange(i * i, n, i):  # NOQA
                _primes[j] = False


def primes(n):
    """Return a list of primes from [2, n)"""
    return list(_eratosthenes(n))


def md5(msg):
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()


def sha256(msg):
    s = hashlib.sha256()
    s.update(msg)
    return s.hexdigest()


def knot_hash(msg):
    lengths = [ord(x) for x in msg] + [17, 31, 73, 47, 23]
    sparse = range(0, 256)
    pos = 0
    skip = 0

    for _ in range(64):
        for l in lengths:
            for i in range(l // 2):
                x = (pos + i) % len(sparse)
                y = (pos + l - i - 1) % len(sparse)
                sparse[x], sparse[y] = sparse[y], sparse[x]

            pos = pos + l + skip % len(sparse)
            skip += 1

    hash_val = 0

    for i in range(16):
        res = 0
        for j in range(0, 16):
            res ^= sparse[(i * 16) + j]

        hash_val += res << ((16 - i - 1) * 8)

    return '%032x' % hash_val


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

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def neighbours_4(self):
        return [self + p for p in DIRS_4]

    def neighbours_8(self):
        return [self + p for p in DIRS_8]


DIRS_4 = DIRS = [
    Point(0, 1),   # north
    Point(1, 0),   # east
    Point(0, -1),  # south
    Point(-1, 0),  # west
]

DIRS_8 = [
    Point(0, 1),    # N
    Point(1, 1),    # NE
    Point(1, 0),    # E
    Point(1, -1),   # SE
    Point(0, -1),   # S
    Point(-1, -1),  # SW
    Point(-1, 0),   # W
    Point(-1, 1),   # NW
]
