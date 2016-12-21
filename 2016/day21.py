import fileinput
from collections import deque

from utils import parse_line


def scramble(data, operations, unscramble=False):
    data = deque(data)

    if unscramble:
        operations.reverse()

    for line in operations:
        if line.startswith('swap position'):
            x, y = parse_line(r'swap position (\d+) with position (\d+)', line)
            data[x], data[y] = data[y], data[x]

        elif line.startswith('swap letter'):
            x, y = parse_line(r'swap letter (\w+) with letter (\w+)', line)
            data = deque(''.join(data).replace(x, '_').replace(y, x).replace('_', y))

        elif line.startswith('rotate based'):
            x = line.split()[-1]
            tmp = ''.join(data)

            if not unscramble:
                i = tmp.index(x)
                data.rotate(i + (2 if i >= 4 else 1))

            else:
                # Keep trying rotation candidates until one is valid
                curr = deque(data)

                while True:
                    curr.rotate(1)
                    post = ''.join(curr)
                    idx = post.index(x)

                    tmp = deque(data)
                    tmp.rotate(-(idx + (2 if idx >= 4 else 1)))
                    pre = ''.join(tmp)

                    if pre == post:
                        data = deque(pre)
                        break


        elif line.startswith('rotate'):
            lr, x = parse_line(r'rotate (\w+) (\d+) step', line)

            if (unscramble and lr == 'right') or (not unscramble and lr == 'left'):
                x = -x

            data.rotate(x)

        elif line.startswith('reverse'):
            x, y = parse_line(r'reverse positions (\d+) through (\d+)', line)

            tmp = ''.join(data)
            tmp = tmp[:x] + ''.join(reversed(tmp[x:y+1])) + tmp[y+1:]
            data = deque(tmp)

        elif line.startswith('move'):
            x, y = parse_line(r'move position (\d+) to position (\d+)', line)

            if unscramble:
                x, y = y, x

            tmp = ''.join(data)

            # Extract the character
            c = tmp[x]
            tmp = tmp[:x] + tmp[x+1:]

            # Reinsert it
            tmp = tmp[:y] + c + tmp[y:]

            data = deque(tmp)


    return ''.join(data)


if __name__ == '__main__':
    operations = [line.strip() for line in fileinput.input()]
    print 'Result of scrambling abcdefgh:', scramble('abcdefgh', operations, False)
    print 'Unscrambled version of fbgdceah:', scramble('fbgdceah', operations, unscramble=True)
