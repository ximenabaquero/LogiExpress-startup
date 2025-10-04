"""
Módulo de visualización de rutas y tablas.
Incluye integración con Google Maps para visualización real.
"""

try:
    from google_maps import GoogleMapsAPI
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False


def visualize_path(path, distances, graph, show_in_maps=False):
    """
    Visualiza una ruta con segmentos y tiempos.
    
    Args:
        path: Lista de nodos en la ruta
        distances: Distancias acumuladas desde el origen
        graph: Objeto Graph para obtener pesos de aristas
    """
    if not path:
        print("No hay ruta disponible")
        return
    
    print("\n" + "="*60)
    print("VISUALIZACIÓN DE RUTA")
    print("="*60)
    
    # Mostrar la ruta completa
    route_str = " → ".join(path)
    print(f"\nRuta: {route_str}")
    
    # Calcular distancia total
    total_distance = distances[path[-1]]
    print(f"Distancia total: {total_distance} minutos")
    
    # Tabla de segmentos
    print("\n" + "-"*60)
    print("TABLA DE SEGMENTOS")
    print("-"*60)
    print(f"{'Desde':<10} {'Hacia':<10} {'Tiempo':<15} {'Acumulado':<15}")
    print("-"*60)
    
    accumulated = 0
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        
        # Buscar el peso de la arista
        segment_time = 0
        for neighbor, weight in graph.get_neighbors(from_node):
            if neighbor == to_node:
                segment_time = weight
                break
        
        accumulated += segment_time
        print(f"{from_node:<10} {to_node:<10} {segment_time:<15} {accumulated:<15}")
    
    print("-"*60)
    
    # Opción para mostrar en Google Maps
    if show_in_maps and GOOGLE_MAPS_AVAILABLE:
        try:
            maps_api = GoogleMapsAPI()
            print("\n🗺️  Opciones de Google Maps:")
            print("1. Ver ruta en el navegador")
            print("2. Mostrar detalles de ubicaciones")
            
            choice = input("\nSelecciona una opción (1-2, Enter para omitir): ").strip()
            
            if choice == '1':
                maps_api.open_route_in_browser(path)
            elif choice == '2':
                print("\n📍 DETALLES DE UBICACIONES:")
                print("-" * 50)
                for node in path:
                    maps_api.print_location_details(node)
                    print()
        except Exception as e:
            print(f"⚠️  Error al conectar con Google Maps: {e}")
    elif show_in_maps and not GOOGLE_MAPS_AVAILABLE:
        print("\n⚠️  Google Maps no disponible. Instala dependencias: pip install -r requirements.txt")
    
    print()


def print_all_routes_from_source(start, distances, predecessors, graph, show_maps_option=False):
    """
    Imprime todas las rutas desde un origen.
    
    Args:
        start: Nodo origen
        distances: dict de distancias desde Dijkstra
        predecessors: dict de predecesores desde Dijkstra
        graph: Objeto Graph
    """
    from algorithms import reconstruct_path
    
    print("\n" + "="*60)
    print(f"TODAS LAS RUTAS DESDE {start}")
    print("="*60)
    print(f"{'Destino':<10} {'Distancia':<15} {'Ruta':<30}")
    print("-"*60)
    
    for node in sorted(graph.get_nodes()):
        if node == start:
            continue
        
        distance = distances[node]
        path = reconstruct_path(predecessors, start, node)
        
        if path and distance != float('inf'):
            route_str = " → ".join(path)
            print(f"{node:<10} {distance:<15} {route_str:<30}")
        else:
            print(f"{node:<10} {'∞':<15} {'No hay ruta':<30}")
    
    print("-"*60)
    print()


def print_all_pairs_matrix(distances, nodes):
    """
    Imprime la matriz de todas las distancias entre pares de nodos.
    
    Args:
        distances: Matriz de distancias de Floyd-Warshall
        nodes: Lista de nodos
    """
    print("\n" + "="*60)
    print("MATRIZ DE TODAS LAS DISTANCIAS (FLOYD-WARSHALL)")
    print("="*60)
    
    # Encabezado
    header = "   |"
    for node in sorted(nodes):
        header += f" {node:^6} |"
    print(header)
    print("-" * len(header))
    
    # Filas
    for from_node in sorted(nodes):
        row = f" {from_node} |"
        for to_node in sorted(nodes):
            dist = distances[from_node][to_node]
            if dist == float('inf'):
                row += f" {'∞':^6} |"
            else:
                row += f" {dist:^6} |"
        print(row)
    
    print("-" * len(header))
    print()


def get_location_name(node_id):
    """
    Obtiene el nombre descriptivo de un nodo.
    
    Args:
        node_id: Identificador del nodo (A-G)
        
    Returns:
        Nombre descriptivo del lugar
    """
    locations = {
        'A': 'Aeropuerto',
        'B': 'Terminal',
        'C': 'Simón Bolívar',
        'D': 'Museo del Oro',
        'E': 'Monserrate',
        'F': 'Zona T',
        'G': 'EAN'
    }
    return locations.get(node_id, node_id)


def print_location_legend():
    """Imprime la leyenda de ubicaciones."""
    print("\n" + "="*60)
    print("UBICACIONES EN BOGOTÁ")
    print("="*60)
    print("A: Aeropuerto")
    print("B: Terminal")
    print("C: Simón Bolívar")
    print("D: Museo del Oro")
    print("E: Monserrate")
    print("F: Zona T")
    print("G: EAN")
    print("="*60)
