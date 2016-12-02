import fileinput
import hashlib

secret_key = fileinput.input()[0].strip()
i = 1

hash1 = None
hash2 = None

print "Searching for hashes..."

while True:
    s = secret_key + str(i)
    h = hashlib.md5(s).hexdigest()

    if h[:5] == "00000":
        hash1 = (s, h) if hash1 == None else hash1

    if h[:6] == "000000":
        hash2 = (s, h) if hash2 == None else hash2

    if hash1 and hash2:
        break
    else:
        i += 1

print "Hashed %s to %s" % hash1
print "Hashed %s to %s" % hash2
