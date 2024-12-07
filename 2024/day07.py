import fileinput
import itertools

from utils import parse_nums


def solve(target, operands, part_2=False):
    ops = ['+', '*']
    if part_2:
        ops.append('||')

    for operators in itertools.product(ops, repeat=(len(operands))):
        ans = operands[0]
        for operand, operator in zip(operands[1:], operators):
            if operator == '+':
                ans += operand
            elif operator == '*':
                ans *= operand
            else:
                ans = int('{}{}'.format(ans, operand))

        if int(ans) == target:
            return target

    return 0

part_1 = 0
part_2 = 0

for line in fileinput.input():
    target, *operands = parse_nums(line)
    part_1 += solve(target, operands)
    part_2 += solve(target, operands, part_2=True)

print("Part 1:", part_1)
print("Part 2:", part_2)
