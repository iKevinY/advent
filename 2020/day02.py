import fileinput
from utils import parse_line

part_1 = 0
part_2 = 0

for line in fileinput.input():
    start, end, letter, pwd = parse_line(r'(\d+)-(\d+) (\w+): (\w+)', line)

    if start <= pwd.count(letter) <= end:
        part_1 += 1

    if (pwd[start-1] == letter) ^ (pwd[end-1] == letter):
        part_2 += 1

print "Part 1:", part_1
print "Part 2:", part_2
