import fileinput
from utils import mul

DIRS = [
    (0, 1),
    (0, -1),
    (-1, 0),
    (1, 0),
]

# Parse problem input.
grid = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        grid[x, y] = int(c)

# Check what trees are visible.
visibles = set()
scenic_scores = {}

for tree in grid:
    scores = []
    for dx, dy in DIRS:
        x, y = tree
        score = 0
        while (x, y) in grid:
            nx = x + dx
            ny = y + dy

            # Are we at the edge yet?
            if (nx, ny) not in grid:
                visibles.add(tree)
                break
            elif grid[nx, ny] >= grid[tree]:
                score += 1
                break

            x = nx
            y = ny
            score += 1

        scores.append(score)

    scenic_scores[tree] = mul(scores)

print("Part 1:", len(visibles))
print("Part 2:", max(scenic_scores.values()))
