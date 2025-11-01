"""
Interfaz CLI mejorada para el sistema de rutas de Bogotá con Google Maps.
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

try:
    from google_maps import GoogleMapsAPI, update_graph_with_real_data
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False


def print_enhanced_menu():
    """Imprime el menú principal mejorado."""
    print("\n" + "="*70)
    print("🗺️  SISTEMA DE RUTAS DE BOGOTÁ - LOGIEXPRESS (CON GOOGLE MAPS)")
    print("="*70)
    print("1. Ruta más corta origen → destino")
    print("2. Todas las rutas desde un origen")
    print("3. Matriz de todos los pares de distancias")
    print("4. Ver ubicaciones y detalles")
    if GOOGLE_MAPS_AVAILABLE:
        print("5. 🌐 Actualizar con datos reales de Google Maps")
        print("6. 🗺️  Ver ruta en Google Maps")
        print("7. Configurar API de Google Maps")
        print("8. Salir")
    else:
        print("5. 📦 Instalar Google Maps (requiere dependencias)")
        print("6. Salir")
    print("="*70)


def configure_google_maps():
    """Permite configurar la API key de Google Maps."""
    if not GOOGLE_MAPS_AVAILABLE:
        print("❌ Google Maps no disponible. Instala dependencias primero.")
        return
    
    print("\n" + "="*60)
    print("🔧 CONFIGURACIÓN DE GOOGLE MAPS API")
    print("="*60)
    print("Para usar funciones reales de Google Maps necesitas:")
    print("1. Una API Key de Google Cloud Platform")
    print("2. Habilitar APIs: Maps JavaScript API, Directions API, Distance Matrix API")
    print()
    print("Obtén tu API key en: https://console.cloud.google.com/")
    print()
    
    api_key = input("Ingresa tu API key (o Enter para usar datos simulados): ").strip()
    
    if api_key:
        # Actualizar archivo de configuración
        try:
            with open('config.py', 'r') as f:
                content = f.read()
            
            content = content.replace(
                "'API_KEY': 'TU_API_KEY_AQUI'",
                f"'API_KEY': '{api_key}'"
            )
            
            with open('config.py', 'w') as f:
                f.write(content)
            
            print("✅ API key configurada correctamente")
            
            # Probar la conexión
            maps_api = GoogleMapsAPI(api_key)
            distance, duration = maps_api.get_real_distance_duration('A', 'D')
            
            if distance and duration:
                print(f"✅ Conexión exitosa. Ejemplo: A→D = {duration:.0f} min, {distance:.1f} km")
            else:
                print("⚠️  API key configurada, pero verifica que esté habilitada para Distance Matrix API")
                
        except Exception as e:
            print(f"❌ Error al configurar: {e}")
    else:
        print("ℹ️  Usando datos simulados")


def interactive_google_maps_route():
    """Interfaz interactiva para ver rutas en Google Maps."""
    if not GOOGLE_MAPS_AVAILABLE:
        print("❌ Google Maps no disponible.")
        return
    
    print("\n" + "="*60)
    print("🗺️  VER RUTA EN GOOGLE MAPS")
    print("="*60)
    
    # Crear grafo
    graph = create_bogota_graph()
    
    # Obtener origen y destino
    print("\nUbicaciones disponibles:")
    print_location_legend()
    
    origin = get_valid_node("Ingresa nodo origen: ", graph)
    if origin is None:
        return
        
    destination = get_valid_node("Ingresa nodo destino: ", graph)
    if destination is None:
        return
    
    # Calcular ruta más corta
    distances, predecessors = dijkstra(graph, origin)
    
    if destination not in distances or distances[destination] == float('inf'):
        print(f"❌ No hay ruta disponible de {origin} a {destination}")
        return
    
    # Reconstruir ruta
    path = reconstruct_path(predecessors, origin, destination)
    
    print(f"\n🛣️  Ruta más corta: {' → '.join(path)}")
    print(f"⏱️  Tiempo estimado: {distances[destination]} minutos")
    
    # Mostrar en Google Maps
    try:
        maps_api = GoogleMapsAPI()
        
        print("\n📍 Detalles de la ruta:")
        for node in path:
            info = maps_api.get_location_info(node)
            print(f"  {node}: {info.get('name', 'Desconocido')}")
        
        print("\n🗺️  Abriendo ruta en Google Maps...")
        maps_api.open_route_in_browser(path)
        
    except Exception as e:
        print(f"❌ Error al abrir Google Maps: {e}")


def update_with_real_data():
    """Actualiza el grafo con datos reales de Google Maps."""
    if not GOOGLE_MAPS_AVAILABLE:
        print("❌ Google Maps no disponible.")
        return
    
    print("\n" + "="*60)
    print("🔄 ACTUALIZAR CON DATOS REALES")
    print("="*60)
    
    try:
        # Crear grafo original
        original_graph = create_bogota_graph()
        
        # Crear instancia de Google Maps
        maps_api = GoogleMapsAPI()
        
        # Actualizar con datos reales
        updated_graph = update_graph_with_real_data(original_graph, maps_api)
        
        print("\n📊 Comparación de datos:")
        print("-" * 50)
        
        # Mostrar algunas comparaciones
        test_routes = [('A', 'D'), ('B', 'E'), ('C', 'F')]
        
        for origin, destination in test_routes:
            # Datos originales
            orig_distances, _ = dijkstra(original_graph, origin)
            orig_time = orig_distances.get(destination, 'N/A')
            
            # Datos actualizados
            new_distances, _ = dijkstra(updated_graph, origin)
            new_time = new_distances.get(destination, 'N/A')
            
            print(f"{origin}→{destination}: Original={orig_time}min, Real≈{new_time}min")
        
        print("\n✅ Datos actualizados con Google Maps")
        return updated_graph
        
    except Exception as e:
        print(f"❌ Error al actualizar: {e}")
        return None


def get_valid_node(prompt, graph):
    """
    Solicita un nodo válido al usuario.
    
    Args:
        prompt: Mensaje para mostrar al usuario
        graph: Grafo para validar nodos
        
    Returns:
        Nodo válido o None si se cancela
    """
    while True:
        node = input(prompt).upper().strip()
        if node == '':
            return None
        if node in graph.get_nodes():
            return node
        print(f"❌ Nodo '{node}' no válido. Usa: {', '.join(graph.get_nodes())}")


def main():
    """Función principal del programa mejorado."""
    print("🚀 Iniciando LogiExpress con integración Google Maps...")
    
    if not GOOGLE_MAPS_AVAILABLE:
        print("\n⚠️  NOTA: Para funcionalidades completas de Google Maps:")
        print("   pip install -r requirements.txt")
    
    # Crear grafo inicial
    graph = create_bogota_graph()
    current_graph = graph  # Mantener referencia al grafo actual
    
    while True:
        print_enhanced_menu()
        
        try:
            max_options = 8 if GOOGLE_MAPS_AVAILABLE else 6
            choice = input(f"\nSelecciona una opción (1-{max_options}): ").strip()
            
            if choice == '1':
                # Ruta más corta
                print("\nUbicaciones disponibles:")
                print_location_legend()
                
                origin = get_valid_node("Ingresa nodo origen: ", current_graph)
                if origin is None:
                    continue
                    
                destination = get_valid_node("Ingresa nodo destino: ", current_graph)
                if destination is None:
                    continue
                
                distances, predecessors = dijkstra(current_graph, origin)
                
                if destination not in distances or distances[destination] == float('inf'):
                    print(f"❌ No hay ruta disponible de {origin} a {destination}")
                    continue
                
                path = reconstruct_path(predecessors, origin, destination)
                visualize_path(path, distances, current_graph, show_in_maps=GOOGLE_MAPS_AVAILABLE)
                
            elif choice == '2':
                # Todas las rutas desde origen
                print("\nUbicaciones disponibles:")
                print_location_legend()
                
                origin = get_valid_node("Ingresa nodo origen: ", current_graph)
                if origin is None:
                    continue
                
                distances, predecessors = dijkstra(current_graph, origin)
                print_all_routes_from_source(origin, distances, predecessors, current_graph, GOOGLE_MAPS_AVAILABLE)
                
            elif choice == '3':
                # Matriz de todos los pares
                distances_matrix = floyd_warshall(current_graph)
                print_all_pairs_matrix(distances_matrix, current_graph)
                
            elif choice == '4':
                # Ver ubicaciones
                print_location_legend()
                if GOOGLE_MAPS_AVAILABLE:
                    try:
                        maps_api = GoogleMapsAPI()
                        print("\n📍 DETALLES COMPLETOS:")
                        print("-" * 60)
                        for node in current_graph.get_nodes():
                            maps_api.print_location_details(node)
                            print()
                    except Exception as e:
                        print(f"⚠️  Error al obtener detalles: {e}")
                
            elif choice == '5':
                if GOOGLE_MAPS_AVAILABLE:
                    # Actualizar con datos reales
                    updated_graph = update_with_real_data()
                    if updated_graph:
                        use_updated = input("\n¿Usar datos actualizados? (s/N): ").lower().strip()
                        if use_updated == 's':
                            current_graph = updated_graph
                            print("✅ Ahora usando datos reales de Google Maps")
                else:
                    print("\n📦 Para instalar Google Maps:")
                    print("1. pip install -r requirements.txt")
                    print("2. Reinicia el programa")
                
            elif choice == '6':
                if GOOGLE_MAPS_AVAILABLE:
                    # Ver ruta en Google Maps
                    interactive_google_maps_route()
                else:
                    print("👋 ¡Hasta luego!")
                    break
                    
            elif choice == '7' and GOOGLE_MAPS_AVAILABLE:
                # Configurar Google Maps
                configure_google_maps()
                
            elif choice == '8' and GOOGLE_MAPS_AVAILABLE:
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()