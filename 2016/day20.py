import fileinput
from utils import parse_line

MAX_IP = 2**32 - 1


def allowed_ips(blacklist, max_ip=MAX_IP):
    """Generator over all allowed IPs given a blacklist."""
    i = 0

    while i <= max_ip:
        if not blacklist:
            for n in range(i, max_ip + 1):
                yield n

            return

        start, end = blacklist.pop(0)

        if i < start:
            for n in range(i, start):
                yield n

        if i <= end:
            i = end + 1


if __name__ == '__main__':
    blacklist = []

    for line in fileinput.input():
        start, end = parse_line(r'(\d+)-(\d+)', line)
        blacklist.append((start, end))

    blacklist.sort()

    whitelist = list(allowed_ips(blacklist))

    print "Lowest-valued whitelisted IP:", whitelist[0]
    print "Number of allowed addresses:", len(whitelist)
