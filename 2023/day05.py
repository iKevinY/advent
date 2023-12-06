import fileinput
import itertools


def seed_to_location(mappings, seed):
    curr = seed
    for mapping in mappings:
        for dest, src, rng in mapping:
            if src <= curr <= src + rng:
                curr += (dest - src)
                break

    return curr

def location_to_seed(mappings, location):
    curr = location
    for mapping in reversed(mappings):
        for dest, src, rng in mapping:
            if dest <= curr < dest + rng:
                curr -= (dest - src)
                break

    return curr


def seed_in_start_range(cand, seed_starts, seed_ranges):
    for start, rng in zip(seed_starts, seed_ranges):
        if start <= cand < start + rng:
            return True

    return False


# Parse problem input.
file = ''.join(fileinput.input())[:-1]
seeds, *raw_mappings = file.split('\n\n')
seeds = [int(x) for x in seeds.split()[1:]]

mappings = []
for m in raw_mappings:
    nums = m.split('\n')[1:]
    mapping = [[int(x) for x in line.split()] for line in nums]
    mappings.append(mapping)


# Solve Part 1.
print("Part 1:", min(seed_to_location(mappings, seed) for seed in seeds))

# Solve Part 2.
seed_starts = seeds[::2]
seed_ranges = seeds[1::2]

for location in itertools.count(start=1):
    seed = location_to_seed(mappings, location)
    if seed_in_start_range(seed, seed_starts, seed_ranges):
        break

print("Part 2:", location)

