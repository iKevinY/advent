import fileinput
import copy
from utils import parse_nums

INPUT = ''.join(fileinput.input())
board, moves = INPUT.split('\n\n')

board = board.splitlines()
bottom = board[-1]
num_of_stacks = max(int(x) for x in bottom.split())
STACKS = [[] for _ in range(num_of_stacks)]

for line in board[::-1]:
    for i, crate in enumerate(line[1::4]):
        if crate.isupper():
            STACKS[i].append(crate)

MOVES = [parse_nums(line) for line in moves.splitlines()]


def simulate(part_2=False):
    stacks = copy.deepcopy(STACKS)
    for amt, frm, to in MOVES:
        frm -= 1
        to -= 1

        crates_to_move = []
        for _ in range(amt):
            crate = stacks[frm].pop()
            crates_to_move.append(crate)

        if not part_2:
            crates_to_move.reverse()

        stacks[to].extend(crates_to_move)

    return ''.join(s[-1] for s in stacks)

print("Part 1:", simulate())
print("Part 2:", simulate(part_2=True))
