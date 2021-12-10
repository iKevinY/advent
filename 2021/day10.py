import fileinput

RIGHT_TO_LEFT = {
    '}': '{',
    ']': '[',
    ')': '(',
    '>': '<',
}

LEFT_TO_RIGHT = {v: k for k, v in RIGHT_TO_LEFT.items()}

ILLEGAL_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

PART_2_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

part_1 = 0
part_2_scores = []

for line in fileinput.input():
    stk = []
    is_incomplete = True

    for c in line.strip():
        if c in RIGHT_TO_LEFT.values():
            stk.append(c)
        else:
            p = stk.pop()
            if RIGHT_TO_LEFT[c] != p:
                is_incomplete = False
                part_1 += ILLEGAL_POINTS[c]

    if is_incomplete:
        score = 0
        for s in stk[::-1]:
            score *= 5
            score += PART_2_POINTS[LEFT_TO_RIGHT[s]]

        part_2_scores.append(score)

print "Part 1:", part_1
print "Part 2:", sorted(part_2_scores)[len(part_2_scores)//2]
