import fileinput
from utils import mul


HEX_MAPPING = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

OPERATORS = {
    0: '+',
    1: '*',
    2: 'min',
    3: 'max',
    5: '>',
    6: '<',
    7: '=='
}


def parse_packets(bits, num_subpackets=None, bit_length=None, depth=0, quiet=False):
    """
    Given a bitstring `bits`, parses `num_subpackets` subpackets, and returns ([packets], bit_length, version).

    If the argument `num_subpackets` is given, this dictates the number of packets
    to parse from `bits` before returning.

    If the argument `bit_length` is given, this dictates how many bits to process
    before returning however many packets the parser got through.

    If `quiet` is False, the parser will print the operator and values processed,
    with various nesting levels based on `depth` (incremented per recursive call).
    """

    i = 0        # current pointer into `bits`
    subs = []    # list of subpackets currently parsed
    version = 0  # the version so far (?)

    try:
        while True:
            # Standard Packet Header

            # Read 3-bit version
            version += int(bits[i:i+3], 2)
            i += 3

            # Read 3-bit type ID
            ttype = int(bits[i:i+3], 2)
            i += 3

            # Packets with type ID 4 represent a literal value.
            if ttype == 4:
                lit = ''

                # Read groups of 5 bits until the final group
                # (prefixed 0) is seen. Then stop reading.
                while True:
                    group = bits[i:i+5]
                    i += 5
                    lit += group[1:]
                    if group[0] == '0':
                        break

                try:
                    lit = int(lit, 2)
                    subs.append(lit)
                except Exception:
                    print "bad literal, moving on"

            # Otherwise, process an operator.
            else:
                # Operator packet mode is based on its 1-bit length type ID.
                len_type_id = bits[i]
                i += 1

                # Specifies the bit length of contained subpackets.
                if len_type_id == '0':
                    sub_len = int(bits[i:i+15], 2)
                    i += 15
                    subpackets, new_i, new_version = parse_packets(bits[i:i+sub_len], bit_length=sub_len, depth=depth + 1, quiet=quiet)

                    i += new_i
                    version += new_version

                # Specifies total number of subpackets.
                elif len_type_id == '1':
                    sub_packets = int(bits[i:i+11], 2)
                    i += 11
                    subpackets, new_i, new_version = parse_packets(bits[i:], num_subpackets=sub_packets, depth=depth+1, quiet=quiet)

                    i += new_i
                    version += new_version
                else:
                    print "Unknown length type ID"

                # Process operators
                if not quiet:
                    print " " * depth, OPERATORS[ttype], subpackets

                if ttype == 0:
                    subs.append(sum(subpackets))
                elif ttype == 1:
                    subs.append(mul(subpackets))
                elif ttype == 2:
                    subs.append(min(subpackets))
                elif ttype == 3:
                    subs.append(max(subpackets))
                elif ttype == 5:
                    subs.append(1 if subpackets[0] > subpackets[1] else 0)
                elif ttype == 6:
                    subs.append(1 if subpackets[0] < subpackets[1] else 0)
                elif ttype == 7:
                    subs.append(1 if subpackets[0] == subpackets[1] else 0)

            # Check exit conditions for loop.
            if num_subpackets is not None and len(subs) == num_subpackets:
                # IMPORTANT: return i and not len(i); it is not an invariant
                # that we read the full `bits`, since there may have been
                # some trailing data that we ignore since it falls out of
                # the range of `num_subpackets` subpackets.
                return subs, i, version
            elif bit_length is not None and i > bit_length:
                return subs, len(bits), version
            elif i >= len(bits):
                return subs, len(bits), version

    except Exception as e:
        print "Unexpected parsing error:", e
        return subs, i, version


# Read problem input.
BITS = ''.join(HEX_MAPPING[byte] for byte in fileinput.input()[0].strip())

# Problem guarantees the input consists of precisely 1 outer packet.
packets, _, total_version = parse_packets(BITS, num_subpackets=1, quiet=True)

print "Part 1:", total_version
print "Part 2:", packets[0]
