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


def parse_address(address):
    runs = re.findall(r'(\w+)', address.strip())
    return runs[::2], runs[1::2]


def supports_tls(address):
    sequences, hypernets = parse_address(address)

    if any(is_abba(s) for s in sequences):
        if not any(is_abba(h) for h in hypernets):
            return True

    return False


def supports_ssl(address):
    sequences, hypernets = parse_address(address)

    for seq in sequences:
        for a, b in find_abas(seq):
            bab = b + a + b

            if any(bab in h for h in hypernets):
                return True

    return False


ADDRESSES = [line.strip() for line in fileinput.input()]
print "Number of TLS IPs: %i" % sum(supports_tls(a) for a in ADDRESSES)
print "Number of SSL IPs: %i" % sum(supports_ssl(a) for a in ADDRESSES)
