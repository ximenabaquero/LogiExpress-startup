import heapq

def dijkstra(graph, source, target, weight_type="distance"):
    """
    Algoritmo de Dijkstra para encontrar el camino más corto según distancia o tiempo.

    Args:
        graph (dict): lista de adyacencia con la forma {nodo: [(vecino, peso), ...]}
        source (int): ID del nodo de inicio
        target (int): ID del nodo de destino
        weight_type (str): "distance" o "time" (solo para claridad en los logs)

    Returns:
        tuple: (path como lista de IDs de nodos, total_cost)
    """

    # Se inicializan todas las distancias en infinito excepto el origen
    cost = {node: float("inf") for node in graph}
    cost[source] = 0
    previous = {}
    visited = set()

    # Cola de prioridad (min-heap)
    queue = [(0, source)]

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Parada temprana si el objetivo es alcanzado
        if current_node == target:
            break

        # Explorar vecinos
        for neighbor, weight in graph.get(current_node, []):
            new_cost = current_cost + weight
            if new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(queue, (new_cost, neighbor))

    # Reconstruir el camino mas corto
    path = []
    node = target
    while node in previous:
        path.insert(0, node)
        node = previous[node]
    path.insert(0, source)

    # Retorna el camino y costo final de toda la trayectoria (distancia en metros o tiempo en segundos)
    print(f"[INFO] Shortest path computed based on {weight_type}.")
    return path, cost[target]

