#!/usr/bin/env python
"""
Script de demostración del Sistema de Rutas de Bogotá.
Ejecuta pruebas y muestra todas las funcionalidades del sistema.
"""

from graph import create_bogota_graph
from algorithms import dijkstra, floyd_warshall, reconstruct_path, reconstruct_path_floyd_warshall
from visualization import visualize_path, print_all_routes_from_source, print_all_pairs_matrix, print_location_legend


def print_separator():
    """Imprime un separador visual."""
    print("\n" + "="*70 + "\n")


def demo_shortest_path():
    """Demostración de ruta más corta."""
    print("DEMOSTRACIÓN 1: RUTAS MÁS CORTAS ESPECÍFICAS")
    print_separator()
    
    graph = create_bogota_graph()
    
    # Test A -> D (debe ser 32)
    print(">>> Test requerido: A → D")
    distances_a, predecessors_a = dijkstra(graph, 'A')
    path_a_d = reconstruct_path(predecessors_a, 'A', 'D')
    print(f"Origen: A (Aeropuerto)")
    print(f"Destino: D (Museo del Oro)")
    visualize_path(path_a_d, distances_a, graph)
    
    print_separator()
    
    # Test B -> E (debe ser 27)
    print(">>> Test requerido: B → E")
    distances_b, predecessors_b = dijkstra(graph, 'B')
    path_b_e = reconstruct_path(predecessors_b, 'B', 'E')
    print(f"Origen: B (Terminal)")
    print(f"Destino: E (Monserrate)")
    visualize_path(path_b_e, distances_b, graph)
    
    print_separator()
    
    # Ejemplo adicional
    print(">>> Ejemplo adicional: C → G")
    distances_c, predecessors_c = dijkstra(graph, 'C')
    path_c_g = reconstruct_path(predecessors_c, 'C', 'G')
    print(f"Origen: C (Simón Bolívar)")
    print(f"Destino: G (EAN)")
    visualize_path(path_c_g, distances_c, graph)


def demo_all_routes():
    """Demostración de todas las rutas desde un origen."""
    print_separator()
    print("DEMOSTRACIÓN 2: TODAS LAS RUTAS DESDE UN ORIGEN")
    print_separator()
    
    graph = create_bogota_graph()
    
    # Desde el Aeropuerto
    print(">>> Desde A (Aeropuerto)")
    distances, predecessors = dijkstra(graph, 'A')
    print_all_routes_from_source('A', distances, predecessors, graph)
    
    # Desde el Terminal
    print(">>> Desde B (Terminal)")
    distances, predecessors = dijkstra(graph, 'B')
    print_all_routes_from_source('B', distances, predecessors, graph)


def demo_floyd_warshall():
    """Demostración de Floyd-Warshall."""
    print_separator()
    print("DEMOSTRACIÓN 3: MATRIZ DE TODAS LAS DISTANCIAS (FLOYD-WARSHALL)")
    print_separator()
    
    graph = create_bogota_graph()
    distances, next_node = floyd_warshall(graph)
    
    print_all_pairs_matrix(distances, graph.get_nodes())
    
    # Verificar casos de prueba con Floyd-Warshall
    print("Verificación de casos de prueba con Floyd-Warshall:")
    print(f"A → D: {distances['A']['D']} minutos (esperado: 32) ✓" if distances['A']['D'] == 32 else f"A → D: {distances['A']['D']} minutos (esperado: 32) ✗")
    print(f"B → E: {distances['B']['E']} minutos (esperado: 27) ✓" if distances['B']['E'] == 27 else f"B → E: {distances['B']['E']} minutos (esperado: 27) ✗")
    print()


def demo_algorithms_comparison():
    """Compara Dijkstra y Floyd-Warshall."""
    print_separator()
    print("DEMOSTRACIÓN 4: COMPARACIÓN DE ALGORITMOS")
    print_separator()
    
    graph = create_bogota_graph()
    
    print("Comparando Dijkstra vs Floyd-Warshall para A → D:")
    
    # Dijkstra
    distances_dijkstra, predecessors = dijkstra(graph, 'A')
    path_dijkstra = reconstruct_path(predecessors, 'A', 'D')
    
    # Floyd-Warshall
    distances_fw, next_node = floyd_warshall(graph)
    path_fw = reconstruct_path_floyd_warshall(next_node, 'A', 'D')
    
    print(f"\nDijkstra:")
    print(f"  Distancia: {distances_dijkstra['D']} minutos")
    print(f"  Ruta: {' → '.join(path_dijkstra)}")
    
    print(f"\nFloyd-Warshall:")
    print(f"  Distancia: {distances_fw['A']['D']} minutos")
    print(f"  Ruta: {' → '.join(path_fw)}")
    
    print(f"\n¿Resultados iguales? {'✓ SÍ' if distances_dijkstra['D'] == distances_fw['A']['D'] and path_dijkstra == path_fw else '✗ NO'}")


def demo_graph_structure():
    """Muestra la estructura del grafo."""
    print_separator()
    print("DEMOSTRACIÓN 5: ESTRUCTURA DEL GRAFO")
    print_separator()
    
    graph = create_bogota_graph()
    
    print_location_legend()
    
    print("\nLISTA DE ADYACENCIA:")
    print("-" * 60)
    for node in sorted(graph.get_nodes()):
        neighbors = graph.get_neighbors(node)
        print(f"{node}: ", end="")
        if neighbors:
            neighbor_str = ", ".join([f"{n} ({w} min)" for n, w in neighbors])
            print(neighbor_str)
        else:
            print("(sin conexiones salientes)")
    
    print("\nESTADÍSTICAS DEL GRAFO:")
    print("-" * 60)
    print(f"Número de nodos: {len(graph.get_nodes())}")
    total_edges = sum(len(graph.get_neighbors(node)) for node in graph.get_nodes())
    print(f"Número de aristas: {total_edges}")
    print(f"Tipo de grafo: Dirigido con pesos")
    print()


def main():
    """Función principal de demostración."""
    print("\n" + "="*70)
    print("SISTEMA DE RUTAS DE BOGOTÁ - LogiExpress")
    print("Demostración Completa del Sistema")
    print("="*70)
    
    # Ejecutar todas las demostraciones
    demo_shortest_path()
    demo_all_routes()
    demo_floyd_warshall()
    demo_algorithms_comparison()
    demo_graph_structure()
    
    print_separator()
    print("FIN DE LA DEMOSTRACIÓN")
    print("Para usar el sistema interactivamente, ejecute: python main.py")
    print_separator()


if __name__ == "__main__":
    main()
