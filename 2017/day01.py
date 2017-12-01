import fileinput

digits = [int(x) for x in fileinput.input()[0].strip()]
dlen = len(digits)
half = dlen // 2

fst_total = 0
snd_total = 0

for i in range(len(digits)):
    if digits[i] == digits[(i + 1) % dlen]:
        fst_total += digits[i]

    if digits[i] == digits[(i + half) % dlen]:
        snd_total += digits[i]

print "Solution to first captcha:", fst_total
print "Solution to second captcha:", snd_total
