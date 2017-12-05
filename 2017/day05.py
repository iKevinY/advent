import fileinput

INSTR = []

for line in fileinput.input():
    INSTR.append(int(line))

# Part 1
instr = INSTR[:]
steps = 0
i = 0

while 0 <= i < len(instr):
    jump_to = instr[i] + i
    instr[i] += 1
    i = jump_to
    steps += 1

print "Steps to reach exit (part 1):", steps

# Part 2
instr = INSTR[:]
steps = 0
i = 0

while 0 <= i < len(instr):
    jump_to = instr[i] + i
    instr[i] += (-1 if instr[i] >= 3 else 1)
    i = jump_to
    steps += 1

print "Steps to reach exit (part 2):", steps
