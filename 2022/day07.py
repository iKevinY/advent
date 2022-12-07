import fileinput


class File:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.children = []
        self.parent = None

FS = File('/')
pwd = FS

for line in fileinput.input():
    if line.startswith('$'):
        parts = line.split()
        cmd = parts[1]
        if cmd == 'cd':
            directory = parts[2]
            if directory == '..':
                pwd = pwd.parent
            else:  # cd-ing into a new directory
                file = File(directory)
                file.parent = pwd
                pwd.children.append(file)
                pwd = file

    # The current line is telling us something about
    # either a file and its size, or a new directory.
    else:
        size, name = line.split()

        # Only care if we are looking at a file.
        if size != 'dir':
            file = File(name, int(size))
            pwd.children.append(file)


SIZES = {}

def dir_size(file):
    """Return the size of the given file."""
    if not file.children:
        return file.size

    total_size = 0
    for child in file.children:
        total_size += dir_size(child)

    SIZES[file] = total_size
    return total_size

# Perform DFS to seed `SIZES`.
USED = dir_size(FS)

# Part 1
print("Part 1:", sum(s for s in SIZES.values() if s < 100000))

# Part 2
AVAILABLE = 70000000
NEED = 30000000
UNUSED = AVAILABLE - USED

for size in sorted(SIZES.values()):
    if UNUSED + size >= NEED:
        print("Part 2:", size)
        break

