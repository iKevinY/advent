import fileinput
from utils import parse_line

MAX_IP = 2**32 - 1


def allowed_ips(blacklist, max_ip=MAX_IP):
    """Generator over all allowed IPs given a blacklist."""
    i = 0

    for start, end in sorted(blacklist):
        if i < start:
            for n in range(i, start):
                yield n

        if i <= end:
            i = end + 1

    if i <= max_ip:
        for n in range(i, max_ip + 1):
            yield n


if __name__ == '__main__':
    blacklist = []

    for line in fileinput.input():
        start, end = parse_line(r'(\d+)-(\d+)', line)
        blacklist.append((start, end))

    whitelist = list(allowed_ips(blacklist))

    print "Lowest-valued whitelisted IP:", whitelist[0]
    print "Number of allowed addresses:", len(whitelist)
