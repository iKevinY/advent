import fileinput

MAPPINGS = {}

for line in fileinput.input():
    x, y = line.strip().split(' <-> ')
    MAPPINGS[x] = [pid for pid in y.split(', ')]

groups = {}
seen_ids = set()
group_0 = None

for pid in MAPPINGS.keys():
    if pid in seen_ids:
        continue

    connected = set()
    queue = MAPPINGS[pid][:]

    while queue:
        nid = queue.pop()
        connected.add(nid)

        if nid == '0':
            group_0 = pid

        for n in MAPPINGS[nid]:
            if n not in seen_ids:
                queue.append(n)
                seen_ids.add(n)

    groups[pid] = connected

print "Programs in group containing PID 0:", len(groups[group_0])
print "Total number of program groups:", len(groups)
