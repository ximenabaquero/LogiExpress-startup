"""
Tests para el sistema de rutas de Bogotá.
Verifica los casos requeridos: A→D=32 y B→E=27.
"""

import unittest
from graph import create_bogota_graph
from algorithms import dijkstra, floyd_warshall, reconstruct_path, reconstruct_path_floyd_warshall


class TestBogotaGraph(unittest.TestCase):
    """Tests para el grafo de Bogotá."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.graph = create_bogota_graph()
    
    def test_graph_creation(self):
        """Verifica que el grafo se crea correctamente."""
        nodes = self.graph.get_nodes()
        self.assertEqual(len(nodes), 7)
        self.assertIn('A', nodes)
        self.assertIn('B', nodes)
        self.assertIn('C', nodes)
        self.assertIn('D', nodes)
        self.assertIn('E', nodes)
        self.assertIn('F', nodes)
        self.assertIn('G', nodes)
    
    def test_dijkstra_a_to_d(self):
        """Test requerido: A→D debe ser 32 minutos."""
        distances, predecessors = dijkstra(self.graph, 'A')
        self.assertEqual(distances['D'], 32)
        
        # Verificar la ruta
        path = reconstruct_path(predecessors, 'A', 'D')
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
    
    def test_dijkstra_b_to_e(self):
        """Test requerido: B→E debe ser 27 minutos."""
        distances, predecessors = dijkstra(self.graph, 'B')
        self.assertEqual(distances['E'], 27)
        
        # Verificar la ruta
        path = reconstruct_path(predecessors, 'B', 'E')
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'B')
        self.assertEqual(path[-1], 'E')
    
    def test_floyd_warshall_a_to_d(self):
        """Verifica A→D=32 con Floyd-Warshall."""
        distances, next_node = floyd_warshall(self.graph)
        self.assertEqual(distances['A']['D'], 32)
        
        # Verificar la ruta
        path = reconstruct_path_floyd_warshall(next_node, 'A', 'D')
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
    
    def test_floyd_warshall_b_to_e(self):
        """Verifica B→E=27 con Floyd-Warshall."""
        distances, next_node = floyd_warshall(self.graph)
        self.assertEqual(distances['B']['E'], 27)
        
        # Verificar la ruta
        path = reconstruct_path_floyd_warshall(next_node, 'B', 'E')
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'B')
        self.assertEqual(path[-1], 'E')
    
    def test_dijkstra_same_node(self):
        """Verifica que la distancia de un nodo a sí mismo es 0."""
        distances, _ = dijkstra(self.graph, 'A')
        self.assertEqual(distances['A'], 0)
    
    def test_adjacency_matrix(self):
        """Verifica que la matriz de adyacencia se genera correctamente."""
        matrix = self.graph.get_adjacency_matrix()
        
        # Verificar que la diagonal es 0
        for node in self.graph.get_nodes():
            self.assertEqual(matrix[node][node], 0)
        
        # Verificar algunas aristas conocidas
        self.assertEqual(matrix['A']['B'], 15)
        self.assertEqual(matrix['B']['D'], 25)
        self.assertEqual(matrix['C']['D'], 12)
    
    def test_path_reconstruction(self):
        """Verifica que se reconstruyen correctamente las rutas."""
        distances, predecessors = dijkstra(self.graph, 'A')
        path = reconstruct_path(predecessors, 'A', 'D')
        
        # La ruta debe existir y comenzar en A y terminar en D
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
        self.assertGreater(len(path), 1)
    
    def test_floyd_warshall_symmetric_paths(self):
        """Verifica que Floyd-Warshall calcula correctamente todas las rutas."""
        distances, _ = floyd_warshall(self.graph)
        
        # La diagonal debe ser 0
        for node in self.graph.get_nodes():
            self.assertEqual(distances[node][node], 0)
        
        # Verificar los casos requeridos
        self.assertEqual(distances['A']['D'], 32)
        self.assertEqual(distances['B']['E'], 27)


class TestAlgorithms(unittest.TestCase):
    """Tests adicionales para los algoritmos."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.graph = create_bogota_graph()
    
    def test_dijkstra_vs_floyd_warshall(self):
        """Verifica que Dijkstra y Floyd-Warshall dan los mismos resultados."""
        fw_distances, _ = floyd_warshall(self.graph)
        
        for node in self.graph.get_nodes():
            dijkstra_distances, _ = dijkstra(self.graph, node)
            
            for target in self.graph.get_nodes():
                self.assertEqual(
                    dijkstra_distances[target], 
                    fw_distances[node][target],
                    f"Diferencia en ruta {node}→{target}"
                )


def run_tests():
    """Ejecuta todos los tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBogotaGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithms))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
