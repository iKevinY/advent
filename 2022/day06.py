import fileinput

stream = fileinput.input()[0].strip()

part_1 = None
part_2 = None
for i in range(len(stream)):
    window_1 = stream[i:i+4]
    window_2 = stream[i:i+14]
    if len(window_1) == len(set(window_1)) and not part_1:
        part_1 = i + 4
    if len(window_2) == len(set(window_2)) and not part_2:
        part_2 = i + 14
        break

print("Part 1:", part_1)
print("Part 2:", part_2)
