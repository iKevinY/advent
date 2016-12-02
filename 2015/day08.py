import fileinput
import ast
import re

chars = 0
lits = 0
encoded_chars = 0

for line in fileinput.input():
    line = line.strip()  # strip newline

    chars += len(line)
    lits += len(ast.literal_eval(line))
    encoded_chars += (len(re.escape(line)) + 2 )

print "chars - literals = %d" % (chars - lits)
print "encoded_chars - chars = %d" % (encoded_chars - chars)
