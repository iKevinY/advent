import fileinput
import heapq

from utils import Point, DIRS


def minimize_heat_loss(graph, start, goal=None, part_2=False):
    def gen_neighbours(node, last_dir, last_count):
        for d in DIRS:
            n = node + d
            if n not in graph:
                continue

            if last_dir is not None:
                # No U-turns allowed.
                if last_dir == -d:
                    continue

                if part_2:
                    # Early ultra crucible turn.
                    if last_count < 4 and d != last_dir:
                        continue

                    # Wobbly ultra crucible.
                    if last_count == 10 and d == last_dir:
                        continue
                else:
                    # Unstable regular crucible.
                    if last_count == 3 and last_dir == d:
                        continue

            yield n, graph[n], d

    horizon = [(0, start, None, 0)]
    seen = set()

    while horizon:
        depth, curr, last_dir, last_count = heapq.heappop(horizon)

        if (curr, last_dir, last_count) in seen:
            continue

        seen.add((curr, last_dir, last_count))

        # Check if at the bottom-right, and that our last 4 moves
        # were in the same direction if we're solving part 2.
        if curr == goal and (not part_2 or last_count >= 4):
            return depth

        for neighbour, weight, nd in gen_neighbours(curr, last_dir, last_count):
            new_cost = weight + depth
            new_count = 1 if nd != last_dir else last_count + 1
            heapq.heappush(horizon, (new_cost, neighbour, nd, new_count))


# Read problem input.
graph = {}
for y, line in enumerate(fileinput.input()):
    for x, c in enumerate(line.strip()):
        graph[Point(x, y)] = int(c)

start = Point(0, 0)
end = Point(x, y)

# Solve problem.
print("Part 1:", minimize_heat_loss(graph, start, end, part_2=False))
print("Part 2:", minimize_heat_loss(graph, start, end, part_2=True))
