import fileinput

TARGET = 19690720
NOUN_1 = 12
VERB_1 = 2

TAPE = [int(x) for x in fileinput.input()[0].split(',')]

for noun in range(100):
    for verb in range(100):
        tape = TAPE[:]
        pc = 0
        tape[1] = noun
        tape[2] = verb

        while pc < len(tape):
            opcode = tape[pc]
            if opcode == 1:
                tape[tape[pc + 3]] = tape[tape[pc + 1]] + tape[tape[pc + 2]]
                pc += 4
            elif opcode == 2:
                tape[tape[pc + 3]] = tape[tape[pc + 1]] * tape[tape[pc + 2]]
                pc += 4
            elif opcode == 99:
                result = tape[0]
                if result == TARGET:
                    print "100 * noun + verb =", 100 * noun + verb
                elif noun == NOUN_1 and verb == VERB_1:
                    print "Value in position 0 for Part 1:", result

                break
