"""
Módulo de algoritmos de rutas más cortas.
Implementa Dijkstra (SSSP) y Floyd-Warshall (APSP).
"""

import heapq


def dijkstra(graph, start):
    """
    Implementa el algoritmo de Dijkstra para encontrar las rutas más cortas
    desde un nodo origen a todos los demás nodos.
    
    Args:
        graph: Objeto Graph
        start: Nodo origen
        
    Returns:
        Tupla (distances, predecessors) donde:
        - distances: dict con distancias mínimas desde start
        - predecessors: dict con nodos predecesores para reconstruir rutas
    """
    distances = {node: float('inf') for node in graph.get_nodes()}
    predecessors = {node: None for node in graph.get_nodes()}
    distances[start] = 0
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Si la distancia en la cola es mayor que la registrada, ignorar
        if current_distance > distances[current_node]:
            continue
        
        # Revisar vecinos
        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, predecessors


def reconstruct_path(predecessors, start, end):
    """
    Reconstruye la ruta desde start hasta end usando los predecesores.
    
    Args:
        predecessors: dict de predecesores de Dijkstra
        start: Nodo origen
        end: Nodo destino
        
    Returns:
        Lista de nodos en la ruta, o None si no hay ruta
    """
    if predecessors[end] is None and start != end:
        return None
    
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    return path if path[0] == start else None


def floyd_warshall(graph):
    """
    Implementa el algoritmo de Floyd-Warshall para encontrar todas las rutas
    más cortas entre todos los pares de nodos.
    
    Args:
        graph: Objeto Graph
        
    Returns:
        Tupla (distances, next_node) donde:
        - distances: matriz de distancias mínimas entre todos los pares
        - next_node: matriz para reconstruir rutas
    """
    nodes = graph.get_nodes()
    
    # Inicializar matrices de distancia y siguiente nodo
    distances = graph.get_adjacency_matrix()
    next_node = {}
    
    for i in nodes:
        next_node[i] = {}
        for j in nodes:
            if i == j:
                next_node[i][j] = None
            elif distances[i][j] != float('inf'):
                next_node[i][j] = j
            else:
                next_node[i][j] = None
    
    # Algoritmo Floyd-Warshall
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return distances, next_node


def reconstruct_path_floyd_warshall(next_node, start, end):
    """
    Reconstruye la ruta desde start hasta end usando la matriz next_node
    de Floyd-Warshall.
    
    Args:
        next_node: Matriz de siguiente nodo de Floyd-Warshall
        start: Nodo origen
        end: Nodo destino
        
    Returns:
        Lista de nodos en la ruta, o None si no hay ruta
    """
    if next_node[start][end] is None:
        return None
    
    path = [start]
    current = start
    
    while current != end:
        current = next_node[current][end]
        if current is None:
            return None
        path.append(current)
    
    return path
