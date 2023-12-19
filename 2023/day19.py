import copy
import fileinput
from utils import mul


# Parse problem input.
RULES = {}
WORKFLOWS = []
for line in fileinput.input():
    line = line.strip()

    if line.startswith('{'):
        WORKFLOWS.append([x for x in line[1:-1].split(',')])
    elif line.endswith('}'):
        name, rest = line.split('{')
        rules = []
        for r in rest[:-1].split(','):
            if all(x.isalpha() for x in r):
                rules.append(r)
            else:
                a, b, cond = r[0], r[1], r[2:]
                cond, out = cond.split(':')
                rules.append((a, b, int(cond), out))

        RULES[name] = rules

# Solve part 1.
part_1 = 0
for wf in WORKFLOWS:
    regs = {}
    for state in wf:
        reg, val = state.split('=')
        regs[reg] = int(val)

    curr = 'in'
    while curr not in ('A', 'R'):
        for rule in RULES[curr]:
            if type(rule) == str:
                curr = rule
                break

            reg, cond, val, next_rule = rule
            if cond == '<':
                if regs[reg] < val:
                    curr = next_rule
                    break
            elif cond == '>':
                if regs[reg] > val:
                    curr = next_rule
                    break

    if curr == 'A':
        part_1 += sum(regs.values())

print("Part 1:", part_1)


# Solve part 2.
INITIAL_HYPERCUBE = {k: [1, 4000] for k in 'xmas'}
horizon = [('in', INITIAL_HYPERCUBE)]

ACCEPTED = []

while horizon:
    curr, intervals = horizon.pop()

    if curr == 'A':
        ACCEPTED.append(intervals)
        continue
    elif curr == 'R':
        continue

    for rule in RULES[curr]:
        if type(rule) == str:
            horizon.append((rule, intervals))
            break

        reg, cond, val, next_rule = rule
        if cond == '<':
            if intervals[reg][0] >= val:
                continue

            curr_bound = intervals[reg][1]
            new_intervals = copy.deepcopy(intervals)
            new_intervals[reg][1] = min(val - 1, curr_bound)
            horizon.append((next_rule, copy.deepcopy(new_intervals)))

            # Propagate the inverse state to the next case in the rule.
            curr_bound = intervals[reg][0]
            inverse_intervals = copy.deepcopy(intervals)
            inverse_intervals[reg][0] = max(val, curr_bound)
            intervals = inverse_intervals

        elif cond == '>':
            if intervals[reg][1] <= val:
                continue

            curr_bound = intervals[reg][0]
            new_intervals = copy.deepcopy(intervals)
            new_intervals[reg][0] = max(val + 1, curr_bound)
            horizon.append((next_rule, copy.deepcopy(new_intervals)))

            # Propagate the inverse state to the next case in the rule.
            curr_bound = intervals[reg][1]
            inverse_intervals = copy.deepcopy(intervals)
            inverse_intervals[reg][1] = min(val, curr_bound)
            intervals = inverse_intervals

print("Part 2:", sum(mul(b - a + 1 for a, b in interval.values()) for interval in ACCEPTED))
