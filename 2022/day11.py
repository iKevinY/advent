import os, copy, fileinput
from collections import Counter, deque
from utils import parse_nums, mul


def simulate(monkeys, num_turns, part_2=False):
    monkeys = copy.deepcopy(monkeys)
    mod = mul(m[2] for m in monkeys)
    counts = Counter()

    for turn in range(num_turns):
        for i, (items, operation, div, true, false) in enumerate(monkeys):
            for _ in range(len(items)):
                counts[i] += 1
                item = monkeys[i][0].popleft()
                op, val = operation.split()[-2:]
                if val == 'old':
                    val = item
                else:
                    val = int(val)

                if op == "*":
                    item *= val
                elif op == "+":
                    item += val

                if part_2:
                    item %= mod
                else:
                    item //= 3

                next_monkey = true if item % div == 0 else false
                monkeys[next_monkey][0].append(item)

    inspections = list(sorted(counts.values(), reverse=True))
    return inspections[0] * inspections[1]



# Parse input.
INPUT = "".join(fileinput.input())

MONKEYS = []
for monkey in INPUT.split(os.linesep * 2):
    m = monkey.splitlines()
    items = deque(parse_nums(m[1]))
    operation = m[2].split(': ')[1]
    div = parse_nums(m[3])[0]
    true = parse_nums(m[4])[0]
    false = parse_nums(m[5])[0]
    MONKEYS.append([items, operation, div, true, false])

# Solve problem.
print("Part 1:", simulate(MONKEYS, 20))
print("Part 2:", simulate(MONKEYS, 10000, part_2=True))
