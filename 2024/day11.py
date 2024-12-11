import fileinput
from collections import Counter


stones = Counter(int(n) for n in fileinput.input()[0].split())

for blink in range(1, 76):
    new_stones = Counter()
    for stone, count in stones.items():
        stone_str = str(stone)

        if stone == 0:
            new_stones[1] += count
        elif len(stone_str) % 2 == 0:
            mid = len(stone_str) // 2
            left, right = stone_str[:mid], stone_str[mid:]
            new_stones[int(left)] += count
            new_stones[int(right)] += count
        else:
            new_stones[stone * 2024] += count

    stones = new_stones

    if blink == 25:
        print("Part 1:", sum(stones.values()))
    elif blink == 75:
        print("Part 2:", sum(stones.values()))
