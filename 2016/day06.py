import fileinput
from collections import Counter

messages = [line.strip() for line in fileinput.input()]
columns = []

for i in range(len(messages[0])):
    columns.append(Counter(msg[i] for msg in messages).most_common())

print "Error-corrected message: %s" % ''.join(c[0][0] for c in columns)
print "Santa's original message: %s" % ''.join(c[-1][0] for c in columns)
