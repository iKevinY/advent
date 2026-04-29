import fileinput


def is_fresh(ingredient, intervals):
    for a, b in intervals:
        if a <= ingredient <= b:
            return True

    return False


def is_overlap(a, b, c, d):
    """Returns the (min, max) if (a, b) and (c, d) overlap, else None."""
    if a <= c <= d <= b:
        return a, b
    elif c <= a <= b <= d:
        return c, d
    elif c <= b <= d and a <= c <= b:
        return a, d

    return None, None


def merge_intervals(intervals):
    def _merge_one_pass(intervals):
        new_intervals = []

        for y in range(len(intervals)):
            for x in range(len(intervals)):
                if x == y:
                    continue

                a, b = intervals[x]
                c, d = intervals[y]
                m, n = is_overlap(a, b, c, d)

                if m is not None and n is not None:
                    new_intervals = [interval for i, interval in enumerate(intervals) if i != x and i != y]
                    new_intervals.append((m, n))
                    return new_intervals

        return intervals

    while True:
        new_intervals = _merge_one_pass(intervals)
        if len(new_intervals) == len(intervals):
            return intervals
        intervals = new_intervals


# Read problem input.
INTERVALS = []
INGREDIENTS = []
for line in fileinput.input():
    line = line.strip()
    if '-' in line:
        a, b = line.split('-')
        INTERVALS.append((int(a), int(b)))
    elif line:
        INGREDIENTS.append(int(line))

# Solve problem.
INTERVALS = merge_intervals(INTERVALS)
print("Part 1:", sum(is_fresh(ingredient, INTERVALS) for ingredient in INGREDIENTS))
print("Part 2:", sum(b - a + 1 for a, b in INTERVALS))
