import fileinput
import itertools
import functools
import multiprocessing


def mix(n, secret):
    return n ^ secret

def prune(secret):
    return secret % 16777216

@functools.lru_cache(None)
def advance(n):
    a = n * 64
    n = mix(n, a)
    n = prune(n)

    a = int(n / 32)
    n = mix(n, a)
    n = prune(n)

    a = n * 2048
    n = mix(n, a)
    n = prune(n)

    return n


def possible_windows():
    for a, b, c, d in itertools.product(list(range(-9, 10)), repeat=4):
        yield (a, b, c, d)


def gen_windows(n):
    """Returns the 2000th secret number and all sliding delta windows."""
    windows = {}
    deltas = []
    last = n
    for i in range(2000 - 1):
        n = advance(n)
        delta = (n % 10) - (last % 10)
        deltas.append(delta)
        last = n

        if len(deltas) >= 4:
            w = tuple(deltas[-4:])
            if w not in windows:
                windows[w] = n % 10

    return advance(n), windows


def bananas_for_window(window):
    bananas = 0
    for b in BUYERS:
        bananas += ALL_WINDOWS[b].get(window, 0)

    return bananas


# Read problem input and solve part 1.
part_1 = 0
BUYERS = []
ALL_WINDOWS = {}

for line in fileinput.input():
    buyer = int(line)
    BUYERS.append(buyer)
    secret_2000, windows = gen_windows(buyer)
    part_1 += secret_2000
    ALL_WINDOWS[buyer] = windows

# Solve part 2.
MULTITHREAD = True
NUM_THREADS = multiprocessing.cpu_count()

if MULTITHREAD:
    with multiprocessing.Pool(processes=NUM_THREADS) as pool:
        results = pool.map(bananas_for_window, possible_windows())

else:
    results = []
    for window in possible_windows():
        bananas = bananas_for_window(window)
        results.append(bananas)

print("Part 1:", part_1)
print("Part 2:", max(results))
