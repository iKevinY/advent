import fileinput

string = fileinput.input()[0].strip()

def look_and_say(s):
    occurences = 0
    number = s[0]
    ret = ''

    for n in s:
        if number == n:
            occurences += 1
        else:
            ret += str(occurences) + number
            number = n
            occurences = 1

    return ret + str(occurences) + number

for _ in range(40):
    string = look_and_say(string)

print "Length after 40 iterations: %d" % len(string)

for _ in range(10):
    string = look_and_say(string)

print "Length after 50 iterations: %d" % len(string)
