import fileinput

score = 0
depth = 0
garb_chars = 0

in_garbage = False
skip = False

for c in fileinput.input()[0].strip():
    if skip:
        skip = False

    elif c == '!':
        skip = True

    elif in_garbage:
        if c == '>':
            in_garbage = False
        else:
            garb_chars += 1

    else:
        if c == '{':
            depth += 1
        elif c == '}':
            score += depth
            depth -= 1
        elif c == '<':
            in_garbage = True

print "Total score for all groups:", score
print "Non-canceled garbage characters:", garb_chars
