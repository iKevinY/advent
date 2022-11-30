import re
import math
import hashlib
import operator
import copy
from collections import Counter
from functools import total_ordering, reduce


LETTERS = [x for x in 'abcdefghijklmnopqrstuvwxyz']
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


def parse_line(regex, line):
    """Returns capture groups in regex for line. Int-ifies numbers."""
    ret = []
    for match in re.match(regex, line).groups():
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)

    return ret


def parse_nums(line, negatives=True):
    """Returns a list of numbers in `line`."""
    num_re = r'-?\d+' if negatives else r'\d+'
    return [int(n) for n in re.findall(num_re, line)]


def new_table(val, width, height):
    return [[val for _ in range(width)] for _ in range(height)]


def transposed(matrix):
    """Returns the transpose of the given matrix."""
    return [list(r) for r in zip(*matrix)]


def rotated(matrix):
    """Returns the given matrix rotated 90 degrees clockwise."""
    return [list(r) for r in zip(*matrix[::-1])]

def firsts(matrix):
    """Like matrix[0], but for the first column."""
    return rotated(matrix)[0]

def lasts(matrix):
    """Like matrix[-1], but for the last column."""
    return rotated(matrix)[-1]


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


def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


def egcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g == 1:
        return x % n
    else:
        raise ValueError("%d is not invertible mod %d" % (a, n))

def crt(rems, mods):
    ''' Solve a system of modular equivalences via the Chinese Remainder Theorem.
    Does not require pairwise coprime moduli. '''

    # copy inputs
    orems, omods = rems, mods
    rems = list(rems)
    mods = list(mods)

    newrems = []
    newmods = []

    for i in range(len(mods)):
        for j in range(i+1, len(mods)):
            g = gcd(mods[i], mods[j])
            if g == 1:
                continue
            if rems[i] % g != rems[j] % g:
                raise ValueError("inconsistent remainders at positions %d and %d (mod %d)" % (i, j, g))
            mods[j] //= g

            while 1:
                # transfer any remaining gcds to mods[j]
                g = gcd(mods[i], mods[j])
                if g == 1:
                    break
                mods[i] //= g
                mods[j] *= g

        if mods[i] == 1:
            continue

        newrems.append(rems[i] % mods[i])
        newmods.append(mods[i])

    rems, mods = newrems, newmods

    # standard CRT
    s = 0
    n = 1
    for k in mods:
        n *= k

    for i in range(len(mods)):
        ni = n // mods[i]
        s += rems[i] * modinv(ni, mods[i]) * ni
    return s % n, n


def min_max_xy(points):
    if len(points) == 0:
        return None, None, None, None
    if type(points[0]) == tuple:
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
    else:
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)

    return min_x, max_x, min_y, max_y


def print_grid(grid, f=None, quiet=False):
    """
    Outputs `grid` to stdout. This works whether `grid` is a 2D array,
    or a sparse matrix (dictionary) with keys either (x, y) or Point(x, y).

    This function also returns a tuple (a, b), where a is the serialized
    representation of the grid, in case what gets printed out to stdout
    needs to be consumed afterwards, and b is a Counter over the values
    in `grid`.

    f: a function to transform the values of grid to something printable.
    quiet: don't output to stdout.
    """
    if f is None:
        f = lambda x: str(x)  # NOQA

    counts = Counter()
    serialized = []

    if type(grid) is dict:
        positions = list(grid.keys())
        min_x, max_x, min_y, max_y = min_max_xy(positions)
        if type(positions[0]) is tuple:
            for y in range(min_y, max_y + 1):
                row = ''.join(f(grid.get((x, y), ' ')) for x in range(min_x, max_x + 1))
                if not quiet:
                    print(row)
                serialized.append(row)
                for c in row:
                    counts[c] += 1

        else:
            # (x, y) => point
            for y in range(min_y, max_y + 1):
                row = ''.join(f(grid.get(Point(x, y), ' ')) for x in range(min_x, max_x + 1))
                if not quiet:
                    print(row)
                serialized.append(row)
                for c in row:
                    counts[c] += 1
    else:
        min_x = 0
        min_y = 0
        for y in range(len(grid)):
            row = ''.join(f(grid[y][x]) for x in range(len(grid[0])))
            if not quiet:
                print(row)
            serialized.append(row)
            for x, c in enumerate(row):
                counts[c] += 1
                max_x = x
            max_y = y

    if not quiet:
        print("height={} ({} -> {})".format(max_y - min_y + 1, min_y, max_y))
        print("width={} ({} -> {})".format(max_x - min_x + 1, min_x, max_x))
        print("Statistics:")
        for item, num in counts.most_common():
            print("{}: {}".format(item, num))

    return serialized, counts

def resolve_mapping(candidates):
    """
    Given a dictionary `candidates` mapping keys to candidate values, returns
    a dictionary where each `key` maps to a unique `value`. Hangs if intractable.

    Example:

    candidates = {
        'a': [0, 1, 2],
        'b': [0, 1],
        'c': [0],
    }

    resolve_mapping(candidates) -> {'c': 0, 'b': 1, 'a': 2}
    """
    resolved = {}

    # Ensure the mapping is key -> set(values).
    candidates_map = {}
    for k, v in candidates.items():
        candidates_map[k] = set(v)

    while len(resolved) < len(candidates_map):
        for candidate in candidates_map:
            if len(candidates_map[candidate]) == 1 and candidate not in resolved:
                r = candidates_map[candidate].pop()
                for c in candidates_map:
                    candidates_map[c].discard(r)

                resolved[candidate] = r
                break

    return resolved


def memoize(f):
    """Simple dictionary-based memoization decorator"""
    cache = {}

    def _mem_fn(*args):
        hargs = (','.join(str(x) for x in args))
        if hargs not in cache:
            cache[hargs] = f(*args)
        return cache[hargs]

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


HEX_DIRS = {
    'N': (1, -1, 0),
    'NE': (1, 0, -1),
    'SE': (0, 1, -1),
    'S': (-1, 1, 0),
    'SW': (-1, 0, 1),
    'NW': (0, -1, 1),
}


def hex_distance(x, y, z):
    """Returns a given hex point's distance from the origin."""
    return (abs(x) + abs(y) + abs(z)) // 2


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
        return self.length < other.length

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dist_manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def angle(self, to=None):
        if to is None:
            return math.atan2(self.y, self.x)
        return math.atan2(self.y - to.y, self.x - to.x)

    def rotate(self, turns):
        """Returns the rotation of the Point around (0, 0) `turn` times clockwise."""
        turns = turns % 4

        if turns == 1:
            return Point(self.y, -self.x)
        elif turns == 2:
            return Point(-self.x, -self.y)
        elif turns == 3:
            return Point(-self.y, self.x)
        else:
            return self

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def neighbours_4(self):
        return [self + p for p in DIRS_4]

    def neighbors_4(self):
        return self.neighbours_4()

    def neighbours(self):
        return self.neighbours_4()

    def neighbors(self):
        return self.neighbours()

    def neighbours_8(self):
        return [self + p for p in DIRS_8]

    def neighbors_8(self):
        return self.neighbours_8()


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
