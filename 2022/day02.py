import fileinput

wins = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X',
}

losses = {
    'B': 'X',
    'C': 'Y',
    'A': 'Z',
}

draw = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z',
}

score = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

INPUT = [line.strip() for line in fileinput.input()]

part_1 = 0
for line in INPUT:
    op, us = line.split(' ')

    part_1 += score[us]
    if wins[op] == us:
        part_1 += 6
    elif losses[op] == us:
        part_1 += 0
    else:
        part_1 += 3

print("Part 1:", part_1)

part_2 = 0
for line in INPUT:
    op, outcome = line.split(' ')
    if outcome == 'X':
        us = losses[op]
        part_2 += score[us]
    elif outcome == 'Y':
        us = draw[op]
        part_2 += score[us] + 3
    else:
        us = wins[op]
        part_2 += score[us] + 6

print("Part 2:", part_2)

