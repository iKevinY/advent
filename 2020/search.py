def bfs(start, graph):
    from collections import deque

    max_depth = 0
    depths = {}
    horizon = deque([(start, 0)])  # node, depth
    seen = {start: None}

    # TODO
    def is_goal(node):
        return graph.get(node) == 'G'

    def gen_neighbours(node):
        for n in node.neighbours_4():
            if graph.get(n, ' ') != ' ':
                yield n


    while horizon:
        node, depth = horizon.popleft()  # pop() for DFS
        depths[node] = depth

        if depth > max_depth:
            max_depth = depth
            print "BFS @ {}; depth={}, horizon={}, seen={}".format(node, depth, len(horizon), len(seen))

        for new in gen_neighbours(node):
            if new in seen:
                continue

            seen[new] = node
            horizon.append((new, depth + 1))

            if is_goal(new):
                print "FOUND GOAL", new, depth + 1
                path = []
                curr = new
                while curr is not None:
                    path.append(curr)
                    curr = seen[curr]
                for p in reversed(path):
                    print p
                    pass
                print "FOUND GOAL", new, depth + 1
                return depth + 1

    print "FLOOD FILL COMPLETE, max_depth={}, seen={}".format(max_depth, len(seen))
    return depths

start = Point(0, 0)
bfs(start, board)
