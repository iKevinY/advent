import fileinput
from string import ascii_lowercase

data = ''.join([line for line in fileinput.input()])
groups = [g.split('\n') for g in data.split('\n\n')]

part_1 = 0
part_2 = 0

for group in groups:
    anyone = set()
    everyone = set(ascii_lowercase)

    for person in group:
        anyone |= set(person)
        everyone &= set(person)

    part_1 += len(anyone)
    part_2 += len(everyone)

print part_1
print part_2
