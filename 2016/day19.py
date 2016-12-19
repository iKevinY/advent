import fileinput


class LinkedElf:
    def __init__(self, num):
        self.num = num
        self.next = None


def adjacent_elves(num_elves):
    head = LinkedElf(1)
    curr = head

    for i in range(2, num_elves + 1):
        curr.next = LinkedElf(i)
        curr = curr.next

    curr.next = head
    curr = head

    while curr is not curr.next:
        curr.next = curr.next.next
        curr = curr.next

    return curr.num


def circular_elves(num_elves):
    seen = set()
    victim = num_elves // 2

    # Start with a double jump if number of elves is odd
    double = (num_elves % 2) == 1

    while True:
        seen.add(victim)

        if len(seen) == num_elves:
            return victim + 1

        for _ in range(2 if double else 1):
            victim = (victim + 1) % num_elves
            while victim in seen:
                victim = (victim + 1) % num_elves

        double = not double


if __name__ == '__main__':
    num_elves = int(fileinput.input()[0])
    print "Winning Elf in part 1:", adjacent_elves(num_elves)
    print "Winning Elf in part 2:", circular_elves(num_elves)
