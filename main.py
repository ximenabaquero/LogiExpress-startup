"""
Interfaz CLI para el sistema de rutas de Bogotá.
"""

from graph import create_bogota_graph
from algorithms import dijkstra, floyd_warshall, reconstruct_path, reconstruct_path_floyd_warshall
from visualization import (
    visualize_path, 
    print_all_routes_from_source, 
    print_all_pairs_matrix,
    print_location_legend,
    get_location_name
)


def print_menu():
    """Imprime el menú principal."""
    print("\n" + "="*60)
    print("SISTEMA DE RUTAS DE BOGOTÁ - LOGIEXPRESS")
    print("="*60)
    print("1. Ruta más corta origen → destino")
    print("2. Todas las rutas desde un origen")
    print("3. Matriz de todos los pares de distancias")
    print("4. Ver ubicaciones")
    print("5. Salir")
    print("="*60)


def get_valid_node(prompt, graph):
    """
    Solicita al usuario un nodo válido.
    
    Args:
        prompt: Mensaje para mostrar
        graph: Objeto Graph
        
    Returns:
        Nodo válido seleccionado
    """
    valid_nodes = graph.get_nodes()
    while True:
        node = input(prompt).strip().upper()
        if node in valid_nodes:
            return node
        print(f"Nodo inválido. Seleccione uno de: {', '.join(sorted(valid_nodes))}")


def option_shortest_path(graph):
    """Opción 1: Encuentra la ruta más corta entre dos nodos."""
    print("\n--- RUTA MÁS CORTA ---")
    
    origin = get_valid_node("Ingrese el nodo origen (A-G): ", graph)
    destination = get_valid_node("Ingrese el nodo destino (A-G): ", graph)
    
    # Ejecutar Dijkstra
    distances, predecessors = dijkstra(graph, origin)
    
    # Reconstruir ruta
    path = reconstruct_path(predecessors, origin, destination)
    
    if path:
        print(f"\nOrigen: {origin} ({get_location_name(origin)})")
        print(f"Destino: {destination} ({get_location_name(destination)})")
        visualize_path(path, distances, graph)
    else:
        print(f"\nNo hay ruta disponible desde {origin} hasta {destination}")


def option_all_routes_from_source(graph):
    """Opción 2: Muestra todas las rutas desde un origen."""
    print("\n--- TODAS LAS RUTAS DESDE UN ORIGEN ---")
    
    origin = get_valid_node("Ingrese el nodo origen (A-G): ", graph)
    
    # Ejecutar Dijkstra
    distances, predecessors = dijkstra(graph, origin)
    
    print(f"\nOrigen: {origin} ({get_location_name(origin)})")
    print_all_routes_from_source(origin, distances, predecessors, graph)


def option_all_pairs_matrix(graph):
    """Opción 3: Muestra la matriz de distancias de todos los pares."""
    print("\n--- MATRIZ DE TODOS LOS PARES ---")
    
    # Ejecutar Floyd-Warshall
    distances, next_node = floyd_warshall(graph)
    
    print_all_pairs_matrix(distances, graph.get_nodes())


def main():
    """Función principal de la CLI."""
    # Crear el grafo de Bogotá
    graph = create_bogota_graph()
    
    print("\n¡Bienvenido al Sistema de Rutas de Bogotá!")
    print_location_legend()
    
    while True:
        print_menu()
        choice = input("\nSeleccione una opción (1-5): ").strip()
        
        if choice == '1':
            option_shortest_path(graph)
        elif choice == '2':
            option_all_routes_from_source(graph)
        elif choice == '3':
            option_all_pairs_matrix(graph)
        elif choice == '4':
            print_location_legend()
        elif choice == '5':
            print("\n¡Gracias por usar el Sistema de Rutas de Bogotá!")
            print("Hasta luego.\n")
            break
        else:
            print("\nOpción inválida. Por favor seleccione una opción válida.")
        
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
