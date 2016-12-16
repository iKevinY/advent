import fileinput


def generate_data(data, size):
    def dragon(a):
        b = ''.join('1' if c == '0' else '0' for c in a)
        return a + '0' + b[::-1]

    while len(data) < size:
        data = dragon(data)

    return data[:size]


def checksum(s):
    def checksum_iteration(s):
        tmp = []
        for a, b in zip(s[::2], s[1::2]):
            tmp.append('1' if a == b else '0')

        return ''.join(tmp)

    res = checksum_iteration(s)

    while len(res) % 2 == 0:
        res = checksum_iteration(res)

    return res


if __name__ == '__main__':
    data = fileinput.input()[0].strip()
    print 'Checksum #1:', checksum(generate_data(data, 272))
    print 'Checksum #2:', checksum(generate_data(data, 35651584))
