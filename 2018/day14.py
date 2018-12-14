import fileinput
from itertools import count


def slice_to_str(slice):
    return ''.join(str(n) for n in slice)


INPUT = int(fileinput.input()[0])
input_str = str(INPUT)
input_len = len(input_str)

recipes = [3, 7]
recipes_len = 2
elf_1 = 0
elf_2 = 1

part_1 = None
part_2 = None

while part_1 is None or part_2 is None:
    score = recipes[elf_1] + recipes[elf_2]
    if score >= 10:
        recipes.append(score // 10)
        recipes.append(score % 10)
        recipes_len += 2
    else:
        recipes.append(score)
        recipes_len += 1

    elf_1 = (elf_1 + recipes[elf_1] + 1) % recipes_len
    elf_2 = (elf_2 + recipes[elf_2] + 1) % recipes_len

    if part_1 is None and recipes_len > INPUT + 10:
        part_1 = slice_to_str(recipes[INPUT:INPUT+10])

    if part_2 is None:
        if score >= 10 and slice_to_str(recipes[-1-input_len:-1]) == input_str:
            part_2 = recipes_len - input_len - 1

        if slice_to_str(recipes[-input_len:]) == input_str:
            part_2 = recipes_len - input_len

print "Scores of recipes after puzzle input:", part_1
print "Number of recipes before puzzle input:", part_2
