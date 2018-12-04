import fileinput
from collections import Counter, defaultdict

from utils import parse_line


# Read problem input
EVENTS = []
for line in fileinput.input():
    data = parse_line(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)', line)
    EVENTS.append(data)

EVENTS.sort()

# Process events
SHIFTS = Counter()
GUARDS = defaultdict(Counter)
curr_id = None
sleep = None

for year, month, date, hour, minute, action in EVENTS:
    if 'begins' in action:
        curr_id = int(action.split()[1][1:])

    elif 'asleep' in action:
        sleep = hour, minute

    elif 'wakes' in action:
        h, m = sleep
        SHIFTS[curr_id] += ((hour - h) % 24) * 60 + (minute - m)
        sleep = None

        for x in range(h * 60 + m, hour * 60 + minute):
            GUARDS[curr_id][x % 60] += 1

# Compute Part 1 answer
guard_id = SHIFTS.most_common(1)[0][0]
minute = GUARDS[guard_id].most_common(1)[0][0]
print "Strategy 1 checksum:", guard_id * minute

# Compute Part 2 answer
max_cnt = 0
max_min = 0
max_id = 0

for guard_id, minutes in GUARDS.items():
    minute, count = minutes.most_common(1)[0]
    if count > max_cnt:
        max_cnt = count
        max_min = minute
        max_id = guard_id

print "Strategy 2 checksum:", max_id * max_min
