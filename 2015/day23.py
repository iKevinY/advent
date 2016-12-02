import fileinput
import re

INS = []

for line in fileinput.input():
    INS.append(line.strip())

pc = 0
ra = 1
rb = 0

while 0 <= pc < len(INS):
    ins = INS[pc]
    print '{0: <16}   a: {1}, b: {2}'.format(ins, ra, rb)

    if 'hlf' in ins:
        if 'a' in ins:
            ra /= 2
        else:
            rb /= 2

    elif 'tpl' in ins:
        if 'a' in ins:
            ra *= 3
        else:
            rb *= 3

    elif 'inc' in ins:
        if 'a' in ins:
            ra += 1
        else:
            rb += 1

    elif 'jmp' in ins:
        offset = int(re.findall('\d+', ins)[0]) * (-1 if '-' in ins else 1)
        pc += offset
        pc -= 1  # compensate for pc++ at end

    elif 'jie' in ins:
        offset = int(re.findall('\d+', ins)[0]) * (-1 if '-' in ins else 1)
        if 'a' in ins:
            if ra % 2 == 0:
                pc += offset
                pc -= 1
        else:
            if rb % 2 == 0:
                pc += offset
                pc -= 1

    elif 'jio' in ins:
        offset = int(re.findall('\d+', ins)[0]) * (-1 if '-' in ins else 1)
        if 'a' in ins:
            if ra == 1:
                pc += offset
                pc -= 1
        else:
            if rb == 1:
                pc += offset
                pc -= 1


    pc += 1

print "halt\n--"
print "Register A: %d" % ra
print "Register B: %d" % rb
