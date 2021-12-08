import fileinput
from collections import Counter

lanternfish = [int(x) for x in fileinput.input()[0].split(',')]

state = Counter()

for n in lanternfish:
    state[n] += 1

for i in range(1, 256 + 1):
    next_state = Counter()
    for age, count in state.items():
        if age == 0:
            next_state[6] += count
            next_state[8] += count
        else:
            next_state[age - 1] += count

    state = next_state

    if i == 80:
        print "Part 1:", sum(state.values())

print "Part 2:", sum(state.values())

