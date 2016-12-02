import fileinput
import re
import json

def no_red_sum(x):
    s = 0

    if type(x) == list:
        for y in x:
            if type(y) == int:
                s += y
            else:
                s += no_red_sum(y)
    elif type(x) == dict:
        for k in x.keys():
            if x[k] == 'red':
                return 0
            s += no_red_sum(x[k])
    elif type(x) == int:
        return x

    return s


document = fileinput.input()[0]

print "Sum of all numbers: %d" % sum(int(x) for x in re.findall('-?\d+', document))

j = json.loads(document)

print "Sum of non-reds items: %d" % no_red_sum(j)
