import re
import fileinput

marker_re = re.compile(r'(\d+)x(\d+)')


def decompressed_len(data, improved=False):
    length = 0

    while re.findall(marker_re, data):
        take, repeat = (int(x) for x in re.findall(marker_re, data)[0])

        # Remove any text before the first marker
        length += data.index('(')

        # Strip the marker
        end = data.index(')')
        data = data[end+1:]

        to_repeat = data[:take]

        if '(' in to_repeat and improved:
            length += (decompressed_len(to_repeat, improved=True) * repeat)
        else:
            length += take * repeat

        data = data[take:]

    return length + len(data)


payload = fileinput.input()[0].strip()

print "Length of original format:", decompressed_len(payload)
print "Length of improved format:", decompressed_len(payload, improved=True)
