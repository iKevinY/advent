import fileinput
from collections import Counter, defaultdict

from utils import parse_nums


# Read problem input
EVENTS = sorted(parse_nums(line, negatives=False) for line in fileinput.input())

# Process events
SHIFTS = Counter()
GUARDS = defaultdict(Counter)
curr_id = None
sleep_min = None

for record in EVENTS:
    if len(record) == 6:  # shift begins
        curr_id = int(record[-1])

    elif sleep_min is None:  # falls asleep
        sleep_min = record[-1]

    else:  # wakes up
        minute = record[-1]
        SHIFTS[curr_id] += minute - sleep_min
        for m in range(sleep_min, minute):
            GUARDS[curr_id][m] += 1

        sleep_min = None

# Compute Part 1 answer
guard_id = SHIFTS.most_common(1)[0][0]
minute = GUARDS[guard_id].most_common(1)[0][0]
print "Strategy 1 checksum:", guard_id * minute

# Compute Part 2 answer
guard_id, (minute, _) = max(((i, c.most_common(1)[0]) for i, c in GUARDS.items()), key=lambda x: x[1][1])
print "Strategy 2 checksum:", guard_id * minute
