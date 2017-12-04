import fileinput

fst_valids = 0
snd_valids = 0

for line in fileinput.input():
    passphrase = [x for x in line.split()]
    anagrams = [''.join(sorted(p)) for p in passphrase]

    if len(set(passphrase)) == len(passphrase):
        fst_valids += 1

    if len(set(anagrams)) == len(anagrams):
        snd_valids += 1

print "Valid passphrases under first policy:", fst_valids
print "Valid passphrases under second policy:", snd_valids
