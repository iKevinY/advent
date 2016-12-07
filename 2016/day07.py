import re
import fileinput


def is_abba(seq):
    for i in range(len(seq) - 3):
        a, b, c, d = seq[i:i+4]
        if a == d and b == c and a != b:
            return True

    return False


def find_abas(seq):
    for i in range(len(seq) - 2):
        a, b, c = seq[i:i+3]
        if a == c and a != b:
            yield a, b


tls_ips = 0
ssl_ips = 0

for line in fileinput.input():
    runs = re.findall(r'(\w+)', line.strip())

    sequences = runs[0::2]
    hypernets = runs[1::2]

    if any(is_abba(s) for s in sequences):
        if not any(is_abba(h) for h in hypernets):
            tls_ips += 1

    for seq in sequences:
        for a, b in find_abas(seq):
            bab = b + a + b

            if any(bab in h for h in hypernets):
                ssl_ips += 1
                break

print "Number of TLS IPs: %i" % tls_ips
print "Number of SSL IPs: %i" % ssl_ips
