import fileinput
from collections import deque


def adjacent_elves(num_elves):
    elves = deque(range(1, num_elves + 1))

    while len(elves) > 1:
        elves.rotate(-1)
        elves.popleft()

    return elves[0]


def circular_elves(num_elves):
    left = deque(range(1, (num_elves // 2) + 1))
    right = deque(range((num_elves // 2) + 1, num_elves + 1))

    while len(left) + len(right) > 1:
        # Remove the middle Elf in the circle
        right.popleft()

        # Move an Elf from between deques
        right.append(left.popleft())

        # Rebalance the deques if uneven
        if len(right) - len(left) == 2:
            left.append(right.popleft())

    return right[0]


if __name__ == '__main__':
    num_elves = int(fileinput.input()[0])
    print "Winning Elf in part 1:", adjacent_elves(num_elves)
    print "Winning Elf in part 2:", circular_elves(num_elves)
