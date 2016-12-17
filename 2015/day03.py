import fileinput

DIRS = {
    "^": (0, 1),
    ">": (1, 0),
    "v": (0, -1),
    "<": (-1, 0),
}

def visit_houses(path):
    house = (0, 0)
    for c in path:
        yield house
        house = tuple(map(sum, zip(house, DIRS[c])))

path = fileinput.input()[0].strip()

year_1_houses = set(visit_houses(path))
year_2_houses = set(visit_houses(path[::2])) | set(visit_houses(path[1::2]))

print "Houses visited in year 1: %d" % len(year_1_houses)
print "Houses visited in year 2: %d" % len(year_2_houses)
