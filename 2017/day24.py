import fileinput
from collections import defaultdict, deque


def bridge_bfs(i, port):
    def bridge_strength(ports):
        """Returns the strength of a bridge given its ports."""
        return sum(ports) * 2 - ports[0] - ports[-1]

    # (port_index, port_list, seen_indices)
    horizon = deque([(i, [port], set([i]))])

    strongest = 0

    while horizon:
        longest = 0

        for _ in range(len(horizon)):
            i, ports, seen = horizon.popleft()
            seen.add(i)

            bridge = BRIDGES[i]
            port = bridge[0] if bridge[1] == ports[-1] else bridge[1]

            next_ports = ports + [port]
            strength = bridge_strength(next_ports)

            # See if we can incorporate any `X/X` components
            strength += sum(2 * p for p in BRIDGE_EXTRAS if p in next_ports)

            strongest = max(strongest, strength)
            longest = max(longest, strength)

            for p in BRIDGE_PORTS[port]:
                if p not in seen:
                    horizon.append((p, list(next_ports), set(seen)))

    return strongest, longest


BRIDGES = []
BRIDGE_PORTS = defaultdict(list)
BRIDGE_EXTRAS = []  # tracks components of type `X/X`

for line in fileinput.input():
    x, y = (int(x) for x in line.split('/'))

    if x != y:
        i = len(BRIDGES)
        BRIDGES.append((x, y))
        BRIDGE_PORTS[x].append(i)
        BRIDGE_PORTS[y].append(i)
    else:
        BRIDGE_EXTRAS.append(x)

for i in BRIDGE_PORTS[0]:
    strongest, longest = bridge_bfs(i, 0)
    print "Strength of strongest bridge:", strongest
    print "Strength of longest bridge:", longest
