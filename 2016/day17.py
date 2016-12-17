import fileinput
from hashlib import md5
from itertools import compress


DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}


def open_doors(digest):
    """Returns a 4-tuple of booleans representing whether doors UDLR are open."""
    return [x in 'bcdef' for x in digest[:4]]


def pathfind(salt):
    horizon = [(0, 0, '')]

    while horizon:
        x, y, path = horizon.pop(0)
        digest = md5(salt + path).hexdigest()

        for door in compress('UDLR', open_doors(digest)):
            dx, dy = DIRS[door]
            nx, ny = x + dx, y + dy

            if (0 <= nx < 4) and (0 <= ny < 4):
                if nx == 3 and ny == 3:
                    yield path + door
                else:
                    horizon.append((nx, ny, path + door))


if __name__ == '__main__':
    salt = fileinput.input()[0].strip()
    paths = sorted(pathfind(salt), key=len)
    print 'Shortest path:', paths[0]
    print 'Longest path length:', len(paths[-1])
