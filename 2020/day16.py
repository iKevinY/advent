import fileinput
from collections import defaultdict
from utils import parse_nums, mul, transposed, resolve_mapping

fields = {}
tickets = []

for line in fileinput.input():
    nums = parse_nums(line)
    if nums:
        if len(nums) == 4:
            fields[line.split(':')[0]] = [abs(x) for x in nums]
        else:
            tickets.append(nums)

valid_tickets = []
part_1 = 0

for ticket in tickets[1:]:
    for n in ticket:
        for a, b, c, d in fields.values():
            if a <= n <= b or c <= n <= d:
                break

        else:
            part_1 += n
            break
    else:
        valid_tickets.append(ticket)

print "Part 1:", part_1

poss = defaultdict(set)

for i, col in enumerate(transposed(valid_tickets)):
    for field, (a, b, c, d) in fields.items():
        if all(a <= n <= b or c <= n <= d for n in col):
            poss[field].add(i)

resolved = resolve_mapping(poss)

departures = [resolved[field] for field in resolved if 'departure' in field]
print "Part 2:", mul(tickets[0][i] for i in departures)
