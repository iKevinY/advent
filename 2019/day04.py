import fileinput

password_range = fileinput.input()[0]
start, end = (int(x) for x in password_range.split('-'))

def increasing(n):
    s = [int(c) for c in str(n)]
    if s[0] <= s[1] <= s[2] <= s[3] <= s[4] <= s[5]:
        return True

def part_1_valid(n):
    if not increasing(n):
        return False

    s = [int(c) for c in str(n)]
    if s[0] == s[1] or s[1] == s[2] or s[2] == s[3] or s[3] == s[4] or s[4] == s[5]:
        return True

    return False

def part_2_valid(n):
    if not increasing(n):
        return False

    s = [int(c) for c in str(n)]
    if ((s[0] == s[1] and s[1] != s[2]) or
        (s[1] == s[2] and s[1] != s[0] and s[1] != s[3]) or
        (s[2] == s[3] and s[2] != s[1] and s[2] != s[4]) or
        (s[3] == s[4] and s[3] != s[2] and s[3] != s[5]) or
        (s[4] == s[5] and s[4] != s[3])):
        return True

    return False

print "Part 1 passwords:", sum(part_1_valid(n) for n in range(start, end + 1))
print "Part 2 passwords:", sum(part_2_valid(n) for n in range(start, end + 1))
