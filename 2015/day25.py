import fileinput
import re

# ROW, COL = (int(x) for x in re.findall(r'\d+', fileinput.input()[0]))
ROW, COL = 3010, 3019


def next_code(c):
    return (c * 252533) % 33554393

def code_no(row, col):
    # s = 1
    # for x in range(row + col - 1):
    #     s += x

    # return s + col - 1

    return (((row + col - 1) * (row + col - 2)) / 2) + col

code = 20151125

# for x in range(code_no(ROW, COL) - 1):
#     code = next_code(code)


print (code * pow(252533, code_no(ROW, COL) - 1, 33554393)) % 33554393
