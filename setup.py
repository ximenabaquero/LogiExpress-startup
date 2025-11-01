"""
Script de instalación y configuración para LogiExpress con Google Maps.
"""

import subprocess
import sys
import os


def check_python_version():
    """Verifica la versión de Python."""
    if sys.version_info < (3, 6):
        print("❌ Se requiere Python 3.6 o superior")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True


def install_dependencies():
    """Instala las dependencias necesarias."""
    print("\n📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False


def test_installation():
    """Prueba la instalación."""
    print("\n🧪 Probando instalación...")
    
    try:
        # Probar importaciones básicas
        from graph import create_bogota_graph
        from algorithms import dijkstra
        print("✅ Módulos básicos funcionando")
        
        # Probar Google Maps
        try:
            from google_maps import GoogleMapsAPI
            print("✅ Módulo Google Maps disponible")
            
            # Probar funcionalidad básica
            maps_api = GoogleMapsAPI()
            info = maps_api.get_location_info('A')
            if info:
                print("✅ Configuración de ubicaciones correcta")
            
        except ImportError:
            print("⚠️  Módulo Google Maps no disponible (instala dependencias)")
        
        # Probar algoritmos
        graph = create_bogota_graph()
        distances, _ = dijkstra(graph, 'A')
        
        if distances['D'] == 32:
            print("✅ Algoritmos funcionando correctamente")
        else:
            print("⚠️  Verificar algoritmos - resultado inesperado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        return False


def setup_google_maps():
    """Configuración interactiva de Google Maps."""
    print("\n🗺️  CONFIGURACIÓN DE GOOGLE MAPS")
    print("=" * 50)
    
    print("Para usar funcionalidades completas de Google Maps necesitas:")
    print("1. Una cuenta de Google Cloud Platform")
    print("2. Un proyecto con billing habilitado")
    print("3. APIs habilitadas: Maps JavaScript, Directions, Distance Matrix")
    print()
    
    setup_now = input("¿Configurar Google Maps ahora? (s/N): ").lower().strip()
    
    if setup_now == 's':
        print("\n📋 PASOS PARA OBTENER API KEY:")
        print("1. Ve a: https://console.cloud.google.com/")
        print("2. Crea un proyecto o selecciona uno existente")
        print("3. Ve a 'APIs y servicios' > 'Credenciales'")
        print("4. Clic en 'Crear credenciales' > 'Clave de API'")
        print("5. Habilita las APIs necesarias")
        print()
        
        api_key = input("Pega tu API key aquí (o Enter para omitir): ").strip()
        
        if api_key:
            try:
                # Leer config actual
                with open('config.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Reemplazar API key
                content = content.replace(
                    "'API_KEY': 'TU_API_KEY_AQUI'",
                    f"'API_KEY': '{api_key}'"
                )
                
                # Guardar config actualizada
                with open('config.py', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ API key configurada")
                
                # Probar conexión
                try:
                    from google_maps import GoogleMapsAPI
                    maps_api = GoogleMapsAPI(api_key)
                    distance, duration = maps_api.get_real_distance_duration('A', 'D')
                    
                    if distance and duration:
                        print(f"✅ Conexión exitosa! Ejemplo: A→D = {duration:.0f}min")
                    else:
                        print("⚠️  API key configurada pero verifica permisos")
                        
                except Exception as e:
                    print(f"⚠️  Error al probar conexión: {e}")
                    
            except Exception as e:
                print(f"❌ Error al configurar: {e}")
                
        else:
            print("ℹ️  Configuración omitida - usando datos simulados")
    else:
        print("ℹ️  Configuración omitida - puedes hacerlo después")


def show_usage_instructions():
    """Muestra instrucciones de uso."""
    print("\n" + "=" * 60)
    print("🎉 INSTALACIÓN COMPLETADA")
    print("=" * 60)
    
    print("\n📚 CÓMO USAR LOGIEXPRESS:")
    print("\n1. Interfaz básica:")
    print("   python main.py")
    
    print("\n2. Interfaz con Google Maps:")
    print("   python main_google_maps.py")
    
    print("\n3. Demostraciones:")
    print("   python demo.py")
    print("   python demo_google_maps.py")
    
    print("\n4. Ejecutar tests:")
    print("   python test_graph.py")
    
    print("\n🗺️  FUNCIONALIDADES GOOGLE MAPS:")
    print("- Ver rutas en navegador web")
    print("- Calcular distancias y tiempos reales")
    print("- Información detallada de ubicaciones")
    print("- Actualización con datos en tiempo real")
    
    print("\n🔧 CONFIGURACIÓN ADICIONAL:")
    print("- Edita config.py para personalizar ubicaciones")
    print("- Agrega tu API key para datos reales")
    print("- Modifica main_google_maps.py para nuevas funciones")
    
    print("\n" + "=" * 60)


def main():
    """Función principal de instalación."""
    print("🚀 INSTALADOR LOGIEXPRESS - SISTEMA DE RUTAS BOGOTÁ")
    print("=" * 60)
    
    # Verificar Python
    if not check_python_version():
        return
    
    # Verificar archivos
    required_files = ['graph.py', 'algorithms.py', 'main.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return
    
    print("✅ Archivos del proyecto encontrados")
    
    # Instalar dependencias
    install_deps = input("\n¿Instalar dependencias de Google Maps? (S/n): ").lower().strip()
    
    if install_deps != 'n':
        if not install_dependencies():
            print("⚠️  Continuando sin dependencias de Google Maps")
    
    # Probar instalación
    if not test_installation():
        print("⚠️  Algunas funciones pueden no estar disponibles")
    
    # Configurar Google Maps
    setup_google_maps()
    
    # Mostrar instrucciones
    show_usage_instructions()
    
    print("\n🎯 ¡Listo para usar LogiExpress!")


if __name__ == "__main__":
    main()