import fileinput
from collections import defaultdict


def HASH(code):
    val = 0
    for c in code:
        val += ord(c)
        val *= 17
        val %= 256
    return val


# Parse problem input.
STEPS = next(fileinput.input()).strip().split(',')

# Solve part 1.
print("Part 1:", sum(HASH(step) for step in STEPS))

# Solve part 2.
BOXES = defaultdict(list)

for step in STEPS:
    if step[-1] == '-':
        label = step[:-1]
        box = HASH(label)
        BOXES[box] = [lens for lens in BOXES[box] if lens[0] != label]

    else:
        focal = int(step[-1])
        label = step[:-2]
        box = HASH(label)

        for i, (other_label, other_focal) in enumerate(BOXES[box]):
            if other_label == label:
                BOXES[box][i] = (label, focal)
                break
        else:
            BOXES[box].append((label, focal))

lenses = {}
for box_num, box in BOXES.items():
    for slot_num, (label, focal) in enumerate(box, start=1):
        lenses[label] = (box_num + 1) * slot_num * focal

print("Part 2:", sum(lenses.values()))
