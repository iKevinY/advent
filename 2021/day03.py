import fileinput
from collections import Counter


report = [line.strip() for line in fileinput.input()]


# Part 1
gamma = ''
epsilon = ''
for i in range(len(report[0])):
    c = Counter(r[i] for r in report)
    gamma += c.most_common()[0][0]
    epsilon += c.most_common()[1][0]

gamma = int(gamma, 2)
epsilon = int(epsilon, 2)

print "Part 1:", gamma * epsilon


# Part 2
def part_2(report, idx, oxygen=True):
    # Figure out what the most/least common bit is.
    c = Counter(r[idx] for r in report)
    keep = '1' if oxygen else '0'
    comm = c.most_common()

    if comm[0][1] != comm[1][1]:
        if oxygen:
            keep = comm[0][0]
        else:
            keep = comm[1][0]

    valid = [r for r in report if r[idx] == keep]

    if len(valid) == 1:
        return valid[0]

    return part_2(valid, idx + 1, oxygen=oxygen)


o2 = int(part_2(report, 0, oxygen=True), 2)
co2 = int(part_2(report, 0, oxygen=False), 2)

print "Part 2:", o2 * co2
