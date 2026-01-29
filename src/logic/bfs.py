from collections import deque

def bfs(graph, start, goal):
    """
    Perform Breadth-First Search (BFS) on the Graph from start to goal.
    :param graph: Graph object representing the Board.
    :param start: Starting node (tuple).
    :param goal: Goal node (tuple).
    :return: List of nodes representing the path from start to goal, or empty list if no path found.
    """
    queue = deque([start])
    visited = set()
    parent = {start: None}
    visited.add(start)
    while queue: # While there are nodes to explore
        current = queue.popleft()

        if current == goal: # If we reached the goal
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return reversed path

        for neighbor in graph.edges.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return []  # No path found