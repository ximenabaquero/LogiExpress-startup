"""
Demostración final del sistema LogiExpress con Google Maps.
"""

from graph import create_bogota_graph
from algorithms import dijkstra, reconstruct_path
from google_maps import GoogleMapsAPI


def main():
    print("=" * 70)
    print("LOGIEXPRESS - SISTEMA DE RUTAS DE BOGOTA CON GOOGLE MAPS")
    print("=" * 70)
    
    # Crear grafo
    graph = create_bogota_graph()
    maps_api = GoogleMapsAPI()
    
    print("\n1. UBICACIONES DISPONIBLES:")
    print("-" * 40)
    for node in sorted(graph.get_nodes()):
        info = maps_api.get_location_info(node)
        print(f"   {node}: {info['name']}")
    
    print("\n2. CASOS DE PRUEBA REQUERIDOS:")
    print("-" * 40)
    
    # Caso 1: A -> D = 32 minutos
    distances, predecessors = dijkstra(graph, 'A')
    path_ad = reconstruct_path(predecessors, 'A', 'D')
    print(f"   A->D: {distances['D']} minutos (ruta: {' -> '.join(path_ad)})")
    
    # Caso 2: B -> E = 27 minutos  
    distances, predecessors = dijkstra(graph, 'B')
    path_be = reconstruct_path(predecessors, 'B', 'E')
    print(f"   B->E: {distances['E']} minutos (ruta: {' -> '.join(path_be)})")
    
    print("\n3. INTEGRACION GOOGLE MAPS:")
    print("-" * 40)
    
    # Mostrar datos reales vs simulados
    print("   Comparacion de tiempos (simulados vs reales):")
    test_routes = [('A', 'D'), ('B', 'E'), ('C', 'F')]
    
    for origin, dest in test_routes:
        distances, _ = dijkstra(graph, origin)
        graph_time = distances[dest]
        real_dist, real_time = maps_api.get_real_distance_duration(origin, dest)
        print(f"     {origin}->{dest}: Grafo={graph_time}min, Real≈{real_time}min, {real_dist}km")
    
    print("\n4. URLS DE GOOGLE MAPS:")
    print("-" * 40)
    
    # Generar URLs para rutas principales
    routes_to_show = [
        ('A', 'D', path_ad),
        ('B', 'E', path_be)
    ]
    
    for origin, dest, path in routes_to_show:
        url = maps_api.generate_route_url(path)
        print(f"   {origin}->{dest}: {url}")
    
    print("\n5. COMO USAR EL SISTEMA:")
    print("-" * 40)
    print("   - Basico: python main.py")
    print("   - Con Google Maps: python main_google_maps.py")
    print("   - Configurar API key en config.py para datos reales")
    
    print("\n" + "=" * 70)
    print("SISTEMA LISTO PARA USAR!")
    print("=" * 70)


if __name__ == "__main__":
    main()