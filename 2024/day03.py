import re
import fileinput


MUL_RE = r"mul\((\d+),(\d+)\)"
DONT_DO_RE = r"don\'t\(\).*?(do\(\)|$)"  # match a `do()` or end of string


def count_muls(program):
    return sum(int(x) * int(y) for x, y in re.findall(MUL_RE, program))


program = ''.join(line.strip() for line in fileinput.input())
print("Part 1:", count_muls(program))
print("Part 2:", count_muls(re.sub(DONT_DO_RE, '', program)))

