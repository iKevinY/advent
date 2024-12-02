import fileinput

def is_safe(levels):
    increasing = all((a < b) for a, b in zip(levels, levels[1:]))
    decreasing = all((a > b) for a, b in zip(levels, levels[1:]))
    good_deltas = all((abs(a - b) <= 3) for a, b in zip(levels, levels[1:]))

    return (increasing or decreasing) and good_deltas

def gen_part_2(levels):
    yield levels
    for i in range(len(levels)):
        yield levels[:i] + levels[i+1:]


reports = []

for line in fileinput.input():
    reports.append([int(n) for n in line.split()])

print("Part 1:", sum(is_safe(r) for r in reports))
print("Part 2:", sum(any(is_safe(r) for r in gen_part_2(report)) for report in reports))
