import re
import fileinput
from itertools import combinations


def complete(state):
    return all(f == 3 for f in state)


def valid(state):
    gens = set(state[::2])
    for i, floor in enumerate(state):
        # Element is a chip if it has an odd index
        if i % 2 == 1:
            # Its matching generator is on the same floor, so it's fine
            if state[i-1] == floor:
                continue

            # There is another generator on the floor
            if floor in gens:
                return False

    return True



def solve(state, start_floor=0):
    if start_floor == 3 and complete(state):
        return 0

    horizon = [(start_floor, state)]
    steps = 0
    seen = set()

    while horizon:
        new_horizon = []

        for floor, state in horizon:
            can_move = [i for i, f in enumerate(state) if f == floor]
            moves = []

            if floor < 3:
                moves.extend([(2, floor + 1), (1, floor + 1)])

            if floor > 0:
                moves.extend([(1, floor - 1), (2, floor - 1)])

            moved_two_up = False
            moved_one_down = False

            for n, new_floor in moves:
                # Don't move one item up if you can move two,
                # and don't move two items down if can move one
                if n == 1 and new_floor > floor and moved_two_up:
                    continue
                elif n == 2 and new_floor < floor and moved_one_down:
                    continue

                for move in combinations(can_move, n):
                    next_state = tuple(new_floor if i in move else f for i, f in enumerate(state))

                    if complete(next_state):
                        return steps + 1

                    if valid(next_state) and (new_floor, next_state) not in seen:
                        pair = (new_floor, next_state)
                        new_horizon.append(pair)
                        seen.add(pair)

                        if n == 2 and new_floor > floor:
                            moved_two_up = True
                        if n == 1 and new_floor < floor:
                            moved_one_down = True

        horizon = new_horizon
        steps += 1


generators = {}
microchips = {}

for i, line in enumerate(fileinput.input()):
    for gen in re.findall(r'(\w+) generator', line):
        generators[gen] = i
    for chip in re.findall(r'(\w+)-compatible microchip', line):
        microchips[chip] = i


STATE = []

for key in generators:
    STATE.append(generators[key])
    STATE.append(microchips[key])

STATE = tuple(STATE)

print "Minimum number of steps:", solve(STATE)

STATE = tuple(list(STATE) + [0, 0, 0, 0])
print "With four new objects:", solve(STATE)
