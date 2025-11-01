"""
Demostración del sistema de rutas integrado con Google Maps.
"""

from graph import create_bogota_graph
from algorithms import dijkstra, reconstruct_path

try:
    from google_maps import GoogleMapsAPI, update_graph_with_real_data
    GOOGLE_MAPS_AVAILABLE = True
except ImportError:
    GOOGLE_MAPS_AVAILABLE = False


def demo_basic_functionality():
    """Demuestra funcionalidad básica del sistema."""
    print("="*70)
    print("🚀 DEMOSTRACIÓN - SISTEMA BÁSICO DE RUTAS")
    print("="*70)
    
    # Crear grafo
    graph = create_bogota_graph()
    
    # Casos de prueba requeridos
    test_cases = [
        ('A', 'D', 32),  # Aeropuerto → Museo del Oro
        ('B', 'E', 27),  # Terminal → Monserrate
    ]
    
    print("\n📋 Verificando casos de prueba requeridos:")
    print("-" * 50)
    
    for origin, destination, expected in test_cases:
        distances, predecessors = dijkstra(graph, origin)
        actual = distances[destination]
        path = reconstruct_path(predecessors, origin, destination)
        
        status = "✅" if actual == expected else "❌"
        print(f"{status} {origin}→{destination}: Esperado={expected}min, Actual={actual}min")
        print(f"   Ruta: {' → '.join(path)}")
    
    print("\n" + "="*70)


def demo_google_maps_integration():
    """Demuestra integración con Google Maps."""
    if not GOOGLE_MAPS_AVAILABLE:
        print("\n⚠️  Google Maps no disponible. Instala dependencias:")
        print("   pip install -r requirements.txt")
        return
    
    print("\n" + "="*70)
    print("🗺️  DEMOSTRACIÓN - INTEGRACIÓN GOOGLE MAPS")
    print("="*70)
    
    try:
        # Crear instancia de Google Maps API
        maps_api = GoogleMapsAPI()
        
        # Mostrar información de ubicaciones
        print("\n📍 UBICACIONES DE BOGOTÁ:")
        print("-" * 50)
        
        graph = create_bogota_graph()
        locations_shown = 0
        
        for node in sorted(graph.get_nodes()):
            info = maps_api.get_location_info(node)
            if info:
                print(f"{node}: {info['name']}")
                print(f"   📌 {info['address']}")
                print(f"   🌐 {info['coordinates']}")
                print()
                locations_shown += 1
                
                if locations_shown >= 3:  # Limitar salida para demo
                    break
        
        print(f"... y {len(graph.get_nodes()) - locations_shown} ubicaciones más")
        
        # Demostrar consulta de distancias reales
        print("\n🔍 CONSULTAS DE DISTANCIA REAL:")
        print("-" * 50)
        
        sample_routes = [('A', 'D'), ('B', 'E')]
        
        for origin, destination in sample_routes:
            print(f"\n🛣️  Ruta {origin} → {destination}:")
            
            # Datos del grafo original
            distances, predecessors = dijkstra(graph, origin)
            original_time = distances[destination]
            path = reconstruct_path(predecessors, origin, destination)
            
            print(f"   📊 Tiempo estimado (grafo): {original_time} minutos")
            print(f"   🗺️  Ruta: {' → '.join(path)}")
            
            # Datos reales de Google Maps
            real_distance, real_duration = maps_api.get_real_distance_duration(origin, destination)
            
            if real_distance and real_duration:
                print(f"   🌐 Datos reales Google Maps:")
                print(f"      ⏱️  Tiempo: {real_duration:.0f} minutos")
                print(f"      📏 Distancia: {real_distance:.1f} km")
                
                # Generar URL para visualización
                url = maps_api.generate_route_url(path)
                if url:
                    print(f"      🔗 Ver en Maps: {url[:60]}...")
            else:
                print("   ⚠️  No se pudieron obtener datos reales")
        
        # Opción para abrir en navegador
        print(f"\n🖥️  VISUALIZACIÓN EN NAVEGADOR:")
        print("-" * 50)
        
        choice = input("¿Abrir una ruta de ejemplo en Google Maps? (s/N): ").lower().strip()
        
        if choice == 's':
            # Usar la primera ruta como ejemplo
            origin, destination = sample_routes[0]
            distances, predecessors = dijkstra(graph, origin)
            path = reconstruct_path(predecessors, origin, destination)
            
            print(f"🗺️  Abriendo ruta {origin}→{destination} en Google Maps...")
            maps_api.open_route_in_browser(path)
        
    except Exception as e:
        print(f"❌ Error en demostración Google Maps: {e}")
    
    print("\n" + "="*70)


def demo_real_data_update():
    """Demuestra actualización con datos reales."""
    if not GOOGLE_MAPS_AVAILABLE:
        return
    
    print("\n" + "="*70)
    print("🔄 DEMOSTRACIÓN - ACTUALIZACIÓN CON DATOS REALES")
    print("="*70)
    
    try:
        # Crear grafo original
        original_graph = create_bogota_graph()
        
        print("\n📊 COMPARACIÓN DE DATOS:")
        print("-" * 50)
        print("Actualizando grafo con datos reales...")
        
        # Crear API y actualizar (solo algunas rutas para demo)
        maps_api = GoogleMapsAPI()
        
        # Comparar algunas rutas específicas
        test_routes = [('A', 'D'), ('B', 'E'), ('F', 'G')]
        
        print(f"\n{'Ruta':<8} {'Original':<12} {'Real (aprox)':<15} {'Diferencia':<12}")
        print("-" * 50)
        
        for origin, destination in test_routes:
            # Tiempo original
            orig_distances, _ = dijkstra(original_graph, origin)
            orig_time = orig_distances.get(destination, float('inf'))
            
            # Tiempo real
            _, real_time = maps_api.get_real_distance_duration(origin, destination)
            
            if real_time and orig_time != float('inf'):
                diff = abs(real_time - orig_time)
                print(f"{origin}→{destination}     {orig_time:<12.0f} {real_time:<15.0f} {diff:<12.0f}")
            else:
                print(f"{origin}→{destination}     {orig_time:<12} {'N/A':<15} {'N/A':<12}")
        
        print("\n💡 Nota: Los datos 'reales' son aproximados cuando no hay API key configurada")
        
    except Exception as e:
        print(f"❌ Error en actualización: {e}")
    
    print("\n" + "="*70)


def main():
    """Función principal de demostración."""
    print("🎯 DEMO COMPLETO - LOGIEXPRESS CON GOOGLE MAPS")
    print("="*70)
    
    # Demostración básica
    demo_basic_functionality()
    
    # Pausa
    input("\nPresiona Enter para continuar con la demostración Google Maps...")
    
    # Demostración Google Maps
    demo_google_maps_integration()
    
    # Pausa
    if GOOGLE_MAPS_AVAILABLE:
        input("\nPresiona Enter para continuar con actualización de datos...")
        demo_real_data_update()
    
    # Instrucciones finales
    print("\n" + "="*70)
    print("🎉 DEMOSTRACIÓN COMPLETADA")
    print("="*70)
    print("\n📚 PRÓXIMOS PASOS:")
    print("1. Ejecuta 'python main_google_maps.py' para la interfaz completa")
    print("2. Configura tu API key de Google Maps para datos reales")
    print("3. Instala dependencias: pip install -r requirements.txt")
    
    if not GOOGLE_MAPS_AVAILABLE:
        print("\n⚠️  Para funcionalidades completas de Google Maps:")
        print("   pip install requests urllib3")
    
    print("\n🔗 Enlaces útiles:")
    print("- Google Cloud Console: https://console.cloud.google.com/")
    print("- Documentación API: https://developers.google.com/maps/documentation")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()