import re
import fileinput

marker_re = re.compile(r'(\d+)x(\d+)')


def decompressed_len(data, improved=False):
    if not re.findall(marker_re, data):
        return len(data)

    length = 0

    take, repeat = (int(x) for x in re.findall(marker_re, data)[0])

    # Find start and end indices of first marker
    start = data.index('(')
    end = data.index(')')

    length += start

    data = data[end+1:]
    to_repeat = data[:take]

    if '(' in to_repeat and improved:
        length += decompressed_len(to_repeat, improved) * repeat
    else:
        length += take * repeat

    return length + decompressed_len(data[take:], improved)


payload = fileinput.input()[0].strip()

print "Length of original format:", decompressed_len(payload)
print "Length of improved format:", decompressed_len(payload, improved=True)
