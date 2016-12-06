import fileinput
from collections import Counter

messages = [line.strip() for line in fileinput.input()]
message_1 = ''.join(Counter(c).most_common()[0][0] for c in zip(*messages))
message_2 = ''.join(Counter(c).most_common()[-1][0] for c in zip(*messages))

print "Error-corrected message: %s" % message_1
print "Santa's original message: %s" % message_2
