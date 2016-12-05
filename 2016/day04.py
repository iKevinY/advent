import re
import fileinput
from collections import Counter

from utils import parse_line


def decrypt(c, n):
    if c == '-':
        return ' '

    return chr((((ord(c) - ord('a')) + n) % 26) + ord('a'))


total_sector_id = 0
north_pole_sector_id = None

for line in fileinput.input():
    name, sector, checksum = parse_line(line, r'(\S+)-(\d+)\[(\w{5})\]')
    sector = int(sector)

    real_name = ''.join(decrypt(c, sector) for c in name)

    if 'northpole' in real_name:
        north_pole_sector_id = sector

    occurences = Counter([x for x in name if x.isalpha()])
    commons = sorted(occurences.most_common(), key=lambda (x, y): (-y, x))

    if ''.join(zip(*commons)[0][:5]) == checksum:
        total_sector_id += sector


print "Sum of sector IDs of real rooms: %i" % total_sector_id
print "North Pole storage room sector: %i" % north_pole_sector_id
