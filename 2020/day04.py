import fileinput
from collections import OrderedDict

def validate_hgt(hgt):
    if hgt.endswith('cm'):
        return 150 <= int(hgt[:-2]) <= 193
    elif hgt.endswith('in'):
        return 59 <= int(hgt[:-2]) <= 76

    return False

VALIDATION_FNS = {
    'byr': lambda v: 1920 <= int(v) <= 2002,
    'iyr': lambda v: 2010 <= int(v) <= 2020,
    'eyr': lambda v: 2020 <= int(v) <= 2030,
    'hgt': validate_hgt,
    'hcl': lambda v: len(v) == 7 and v[0] == '#' and all(c in 'abcdef1234567890' for c in v[1:]),
    'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': lambda v: len(v) == 9 and all(c in '1234567890' for c in v),
}

# Parse problem input
passports = []
port = OrderedDict()

for line in fileinput.input():
    line = line.strip()
    if not line:
        passports.append(port)
        port = OrderedDict()
    else:
        parts = [x.split(':') for x in line.split()]
        for a, b in parts:
            port[a] = b

passports.append(port)

part_1 = 0
part_2 = 0

for p in passports:
    if all(k in p for k in VALIDATION_FNS):
        part_1 += 1

        if all(VALIDATION_FNS.get(k, lambda x: True)(v) for k, v in p.items()):
            part_2 += 1

print part_1
print part_2

