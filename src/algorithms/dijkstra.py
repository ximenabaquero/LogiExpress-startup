import heapq

def dijkstra(graph, source, target, weight_type="distance"):
    """
    Dijkstra algorithm to find the shortest path based on distance or time.

    Args:
        graph (dict): adjacency list like {node: [(neighbor, weight), ...]}
        source (int): start node ID
        target (int): end node ID
        weight_type (str): "distance" or "time" (for logging clarity)

    Returns:
        tuple: (path as list of node IDs, total_cost)
    """

    # Initialize all distances to infinity except source
    cost = {node: float("inf") for node in graph}
    cost[source] = 0
    previous = {}
    visited = set()

    # Priority queue (min-heap)
    queue = [(0, source)]

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Early stop if target is reached
        if current_node == target:
            break

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            new_cost = current_cost + weight
            if new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(queue, (new_cost, neighbor))

    # Reconstruct shortest path
    path = []
    node = target
    while node in previous:
        path.insert(0, node)
        node = previous[node]
    path.insert(0, source)

    # Return path and final cost (distance in meters or time in seconds)
    print(f"[INFO] Shortest path computed based on {weight_type}.")
    return path, cost[target]

