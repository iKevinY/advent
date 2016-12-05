import fileinput
from hashlib import md5

door_id = fileinput.input()[0].strip()

print "Using door ID: %s" % door_id

pass_1 = ''
pass_2 = [None for _ in range(8)]

i = 0

while len(pass_1) < 8 or None in pass_2:
    digest = md5(door_id + str(i)).hexdigest()

    if digest.startswith('00000'):
        print "Hash found! %s (%08i)" % (digest, i)

        if len(pass_1) < 8:
            pass_1 += digest[5]

        pos = int(digest[5], 16)
        char = digest[6]

        if pos < 8 and pass_2[pos] is None:
            pass_2[pos] = char

    i += 1

print "Password 1 is: %s" % pass_1
print "Password 2 is: %s" % ''.join(pass_2)
