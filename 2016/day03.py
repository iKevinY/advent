import fileinput
from utils import chunks


def possible_tri(tri):
    t = sorted(tri)
    return t[0] + t[1] > t[2]


triangles = []

for line in fileinput.input():
    triangles.append([int(x) for x in line.split()])

print "Possible triangles: %i" % sum(possible_tri(t) for t in triangles)


col_tris = []

for tris in chunks(triangles, 3):
    col_tris.extend(zip(*tris))

print "Column triangles: %i" % sum(possible_tri(t) for t in col_tris)
