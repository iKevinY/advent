import fileinput
import heapq

from utils import Point, DIRS, N, S, E, W


def minimize_heat_loss(graph, start, goal=None, part_2=False):
    def gen_neighbours(node, hist):
        for d in DIRS:
            n = node + d
            if n not in graph:
                continue

            if hist:
                # No U-turns allowed.
                if hist[-1] == -d:
                    continue

                if part_2:
                    # Early ultra crucible turn.
                    if len(hist) < 4 and d != hist[-1]:
                        continue

                    # Early ultra crucible turn.
                    if len(set(hist[-4:])) != 1 and d != hist[-1]:
                        continue

                    # Wobbly ultra crucible.
                    if len(hist) == 10 and all(x == d for x in hist):
                        continue
                else:
                    # Unstable regular crucible.
                    if len(hist) >= 3 and all(x == d for x in hist[-3:]):
                        continue

            yield n, graph[n], d

    horizon = [(0, start, ())]
    seen = set()
    buf_len = 10 if part_2 else 4

    while horizon:
        depth, curr, hist = heapq.heappop(horizon)

        if (curr, hist) in seen:
            continue

        seen.add((curr, hist))

        # Check if at the bottom-right, and that our last 4 moves
        # were in the same direction if we're solving part 2.
        if curr == goal and (not part_2 or len(set(hist[-4:])) == 1):
            return depth

        for neighbour, weight, nd in gen_neighbours(curr, hist):
            new_cost = weight + depth
            new_hist = hist + (nd,)
            heapq.heappush(horizon, (new_cost, neighbour, new_hist[-buf_len:]))


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
