import fileinput

INC = int(fileinput.input()[0])

# Part 1
spinlock = [0]
pos = 0

for i in range(1, 2017 + 1):
    pos = (pos + INC) % len(spinlock)
    spinlock.insert((pos + 1), i)
    pos += 1

val = spinlock[spinlock.index(2017) + 1]
print "Value after 2017 in small buffer:", val

# Part 2
snd_elem = None
lock_len = 1
pos = 0

for i in range(1, 50000000 + 1):
    pos = (pos + INC) % lock_len

    if pos == 0:
        snd_elem = i

    lock_len += 1
    pos += 1

print "Value after 0 in large buffer:", snd_elem
