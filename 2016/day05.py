import fileinput
from hashlib import md5

door_id = fileinput.input()[0].strip()

print "Using door ID: %s" % door_id

old_password = ''
new_password = [None for _ in range(8)]

i = 0

while len(old_password) < 8 or None in new_password:
    digest = md5(door_id + str(i)).hexdigest()

    if digest.startswith('00000'):
        print "Hash found! %s (%i)" % (digest, i)

        if len(old_password) < 8:
            old_password += digest[5]

        pos = int(digest[5], 16)
        char = digest[6]

        if pos < 8 and new_password[pos] is None:
            new_password[pos] = char

    i += 1

print "First password is: %s" % old_password
print "Second password is: %s" % ''.join(new_password)
