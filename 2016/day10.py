import re
import fileinput
from collections import defaultdict
from utils import parse_line

BOTS = defaultdict(list)
OUTPUTS = defaultdict(list)
INSTRUCTIONS = [line.strip() for line in fileinput.input()]

while INSTRUCTIONS:
    temp = []

    for line in INSTRUCTIONS:
        if 'value' in line:
            val, bot = [int(x) for x in re.findall(r'(\d+)', line)]
            BOTS[bot].append(val)

        else:
            bot, low_t, low, high_t, high = parse_line(r'bot (\d+) .+ (\w+) (\d+) .+ (\w+) (\d+)', line)

            if bot not in BOTS or len(BOTS[bot]) < 2:
                temp.append(line)
                continue

            if 17 in BOTS[bot] and 61 in BOTS[bot]:
                print "Bot #%i compares values 17 and 61." % bot

            l, h = sorted(BOTS[bot][:2])
            BOTS[bot] = []

            (BOTS if low_t == 'bot' else OUTPUTS)[low].append(l)
            (BOTS if high_t == 'bot' else OUTPUTS)[high].append(h)

    INSTRUCTIONS = temp
    temp = []

a, b, c = (OUTPUTS[i][0] for i in range(3))
print "Product of values in outputs 0-2 is %i." % (a * b * c)
