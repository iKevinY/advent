import fileinput

password = fileinput.input()[0].strip()

def is_valid(p):
    if any(x in p for x in ['i', 'o', 'l']):
        return False

    straight = False
    pairs = set()

    for i in range(len(p) - 2):
        if ord(p[i]) == ord(p[i+1]) - 1 == ord(p[i+2]) - 2:
            straight = True
        if p[i] == p[i+1]:
            pairs.add(p[i])

    if p[-1] == p[-2]:
        pairs.add(p[-1])

    return straight and (len(pairs) >= 2)

def next_pass(p):
    # Recursion is fantastic.
    if p == 'z':
        return 'a'
    elif p[-1] == 'z':
        return next_pass(p[:-1]) + 'a'
    else:
        return p[:-1] + chr(ord(p[-1]) + 1)


print "Santa's current password is %s" % password

for _ in range(2):
    while True:
        password = next_pass(password)
        if is_valid(password):
            print "His next password should be %s" % password
            break
