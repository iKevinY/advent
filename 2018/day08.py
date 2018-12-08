import fileinput


def parse_node(nodes, i=0, part_2=False):
    value = 0
    start = i
    num_children, num_meta = nodes[i:i+2]
    child_vals = []

    i += 2

    for _ in range(num_children):
        j, val = parse_node(nodes, i, part_2)
        child_vals.append(val)
        if not part_2:
            value += val
        i += j

    for j in range(num_meta):
        if part_2 and num_children > 0:
            try:
                value += child_vals[nodes[i] - 1]
            except IndexError:
                pass
        else:
            value += nodes[i]

        i += 1

    return i - start, value


nodes = [int(x) for x in fileinput.input()[0].split()]

print "Sum of metadata entries:", parse_node(nodes)[1]
print "Value of the root node:", parse_node(nodes, part_2=True)[1]
