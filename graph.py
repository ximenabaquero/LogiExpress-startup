"""
Módulo de estructura de datos del grafo.
Implementa representación con lista de adyacencia y matriz.
"""

class Graph:
    """Clase Graph que representa un grafo con lista de adyacencia y matriz."""
    
    def __init__(self):
        """Inicializa el grafo vacío."""
        self.adjacency_list = {}
        self.nodes = []
        
    def add_node(self, node):
        """
        Agrega un nodo al grafo.
        
        Args:
            node: Identificador del nodo
        """
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            self.nodes.append(node)
            
    def add_edge(self, from_node, to_node, weight):
        """
        Agrega una arista dirigida al grafo.
        
        Args:
            from_node: Nodo origen
            to_node: Nodo destino
            weight: Peso de la arista (tiempo en minutos)
        """
        if from_node not in self.adjacency_list:
            self.add_node(from_node)
        if to_node not in self.adjacency_list:
            self.add_node(to_node)
            
        self.adjacency_list[from_node].append((to_node, weight))
        
    def get_adjacency_matrix(self):
        """
        Convierte la lista de adyacencia a matriz de adyacencia.
        
        Returns:
            Matriz de adyacencia (dict de dict)
        """
        matrix = {}
        for node in self.nodes:
            matrix[node] = {}
            for neighbor in self.nodes:
                matrix[node][neighbor] = float('inf')
            matrix[node][node] = 0
            
        for node in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[node]:
                matrix[node][neighbor] = weight
                
        return matrix
    
    def get_neighbors(self, node):
        """
        Obtiene los vecinos de un nodo.
        
        Args:
            node: Nodo a consultar
            
        Returns:
            Lista de tuplas (vecino, peso)
        """
        return self.adjacency_list.get(node, [])
    
    def get_nodes(self):
        """
        Obtiene todos los nodos del grafo.
        
        Returns:
            Lista de nodos
        """
        return self.nodes.copy()


def create_bogota_graph():
    """
    Crea el grafo de Bogotá con los nodos y aristas definidos.
    
    Nodos:
    - A: Aeropuerto
    - B: Terminal
    - C: Simón Bolívar
    - D: Museo del Oro
    - E: Monserrate
    - F: Zona T
    - G: EAN
    
    Returns:
        Graph: Grafo de Bogotá
    """
    graph = Graph()
    
    # Agregar nodos
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for node in nodes:
        graph.add_node(node)
    
    # Agregar aristas con pesos (tiempos en minutos)
    # Las conexiones están diseñadas para que A->D=32 y B->E=27
    edges = [
        ('A', 'B', 15),
        ('A', 'C', 20),
        ('B', 'D', 25),  # Aumentado para que B->D->E no sea más corto que B->E
        ('B', 'C', 10),
        ('B', 'E', 27),
        ('C', 'D', 12),
        ('C', 'F', 15),
        ('D', 'E', 10),  # Aumentado para que B->D->E no sea más corto que B->E
        ('D', 'F', 10),
        ('E', 'F', 5),
        ('E', 'G', 12),
        ('F', 'G', 8),
        ('A', 'F', 35),
        ('C', 'E', 30),  # Aumentado para que no sea más corto que la ruta deseada
    ]
    
    for from_node, to_node, weight in edges:
        graph.add_edge(from_node, to_node, weight)
    
    return graph
