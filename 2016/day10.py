import re
import fileinput
from collections import defaultdict
from utils import parse_line, mul


BOTS = defaultdict(list)
OUTPUTS = defaultdict(list)

inst = [line.strip() for line in fileinput.input()]

while inst:
    temp = []

    for line in inst:
        if 'value' in line:
            val, bot = [int(x) for x in re.findall(r'(\d+)', line)]
            BOTS[bot].append(val)

        else:
            bot, low_t, low, high_t, high = parse_line(r'bot (\d+) .+ (\w+) (\d+) .+ (\w+) (\d+)', line)

            if bot not in BOTS or len(BOTS[bot]) != 2:
                temp.append(line)
                continue

            if 17 in BOTS[bot] and 61 in BOTS[bot]:
                print "Bot #%i compares 17 and 61." % bot

            l, h = sorted(BOTS[bot][:2])
            BOTS[bot] = []

            if low_t == 'bot':
                BOTS[low].append(l)
            else:
                OUTPUTS[low].append(l)

            if high_t == 'bot':
                BOTS[high].append(h)
            else:
                OUTPUTS[high].append(h)

    inst = temp
    temp = []

product = mul(OUTPUTS[i][0] for i in range(3))
print "Product of values in outputs 0-2 is %i." % product
