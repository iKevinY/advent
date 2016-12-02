import fileinput
import re

connections = {}

# Set up dictionary of connections
for line in fileinput.input():
    rule, wire = re.search(r'(.*) -> (.*)', line).groups()
    value = None

    if len(rule.split()) == 1:
        value = (rule,)
    elif 'NOT' in rule:
        value = ('NOT', rule.split()[1])
    else:
        value = (rule.split()[1], rule.split()[0], rule.split()[2])

    connections[wire] = value

connections2 = connections.copy()

def follow(wire, c):
    rule = c[wire]
    val = None

    # Base case
    if len(rule) == 1:
        if rule[0].isdigit():
            return int(rule[0])
        else:
            return follow(rule[0], c)

    elif len(rule) == 2:
        return ~follow(rule[1], c)

    else:
        if rule[0] == 'AND':
            val = (int(rule[1]) if rule[1].isdigit() else follow(rule[1], c)) & (int(rule[2]) if rule[2].isdigit() else follow(rule[2], c))
        elif rule[0] == 'OR':
            val = (int(rule[1]) if rule[1].isdigit() else follow(rule[1], c)) | (int(rule[2]) if rule[2].isdigit() else follow(rule[2], c))
        elif rule[0] == 'LSHIFT':
            val = follow(rule[1], c) << int(rule[2])
        elif rule[0] == 'RSHIFT':
            val = follow(rule[1], c) >> int(rule[2])

        if type(val) is int:
            c[wire] = (str(val),)

        return val

s = follow('a', connections)

print "Signal to wire a: %d" % s

connections2['b'] = (str(s), )

print "After overriding b to %s, signal to a is %d" % (s, follow('a', connections2))
