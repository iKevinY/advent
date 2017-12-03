import fileinput
from itertools import count

from utils import Point, DIRS

target = int(fileinput.input()[0])
pos = Point(0, 0)
seen = {pos: 1}
facing = 1

answer_1 = None
answer_2 = None

for i in count(start=2):
    pos = pos + DIRS[facing]

    value = sum(seen.get(p, 0) for p in pos.neighbours_8())
    seen[pos] = value

    if i == target and not answer_1:
        answer_1 = pos.manhattan

    if value > target and not answer_2:
        answer_2 = value

    # Check if we should move straight or turn left next
    if (pos + DIRS[(facing - 1) % 4] not in seen):
        facing = (facing - 1) % 4

    if (answer_1 is not None) and (answer_2 is not None):
        break

print "Step to access port:", answer_1
print "First value larger than puzzle input:", answer_2
