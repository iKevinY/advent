import fileinput


class Node:
    def __init__(self, i, val):
        self.i = i
        self.val = val
        self.back = None
        self.next = None


# Parse problem input.
INPUT = [int(x) for x in fileinput.input()]


def construct_problem(problem_input, decryption_key=1):
    numbers = []
    first = None
    last = None
    zero = None
    for i, num in enumerate(problem_input):
        node = Node(i, num * decryption_key)

        if num == 0:
            zero = node

        if first is None:
            first = node
        else:
            node.back = last

        if last is not None:
            last.next = node

        last = node
        numbers.append(node)

    last.next = first
    first.back = last

    return numbers, zero


def move_number(node, mod):
    n = node.val % mod
    if n == 0:
        return

    # Keep track of old parent/child.
    parent = node.back
    child = node.next

    # Find the next location.
    curr = node
    for _ in range(n):
        curr = curr.next

    # Point new parent/child to node and vice versa.
    desc = curr.next

    desc.back = node
    curr.next = node
    node.back = curr
    node.next = desc

    # Put the old parent/child together.
    parent.next = child
    child.back = parent


def mix(numbers):
    for n in numbers:
        move_number(n, len(numbers) - 1)


def get_grove_coordinates(curr):
    vals = []
    for i in range(3):
        for _ in range(1000):
            curr = curr.next

        vals.append(curr.val)

    return sum(vals)


# Solve part 1.
numbers, zero = construct_problem(INPUT)
mix(numbers)
print("Part 1:", get_grove_coordinates(zero))

# Solve part 2.
numbers, zero = construct_problem(INPUT, decryption_key=811589153)
for _ in range(10): mix(numbers)
print("Part 2:", get_grove_coordinates(zero))

