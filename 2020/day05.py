import fileinput
from collections import Counter


seen = set()
max_seat_id = 0
min_row = 1000
max_row = 0

for line in fileinput.input():
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(line[7:10].replace('L', '0').replace('R', '1'), 2)

    min_row = min(row, min_row)
    max_row = max(row, max_row)
    max_seat_id = max(row * 8 + col, max_seat_id)
    seen.add((row, col))

print "Highest seat ID:", max_seat_id

for row in range(min_row + 1, max_row - 1):
    for col in range(8):
        if (row, col) not in seen:
            print "Your seat ID:", row * 8 + col
