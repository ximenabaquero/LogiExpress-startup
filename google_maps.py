"""
Módulo para integración con Google Maps API.
Proporciona funcionalidades para calcular rutas reales y generar mapas.
"""

import requests
import json
import webbrowser
import urllib.parse
from config import GOOGLE_MAPS_CONFIG, BOGOTA_LOCATIONS, MAP_CONFIG


class GoogleMapsAPI:
    """Clase para manejar las operaciones con Google Maps API."""
    
    def __init__(self, api_key=None):
        """
        Inicializa la conexión con Google Maps API.
        
        Args:
            api_key: Clave de API de Google Maps
        """
        self.api_key = api_key or GOOGLE_MAPS_CONFIG['API_KEY']
        self.base_url = GOOGLE_MAPS_CONFIG['BASE_URL']
        
    def get_real_distance_duration(self, origin_node, destination_node):
        """
        Obtiene distancia y duración real entre dos ubicaciones usando Google Maps.
        
        Args:
            origin_node: Nodo origen (A, B, C, etc.)
            destination_node: Nodo destino (A, B, C, etc.)
            
        Returns:
            tuple: (distancia_km, duracion_minutos) o (None, None) si hay error
        """
        if self.api_key == 'TU_API_KEY_AQUI':
            print("WARNING: API Key no configurada. Usando datos simulados.")
            return self._get_simulated_data(origin_node, destination_node)
            
        origin = BOGOTA_LOCATIONS[origin_node]['coordinates']
        destination = BOGOTA_LOCATIONS[destination_node]['coordinates']
        
        url = f"{self.base_url}/distancematrix/json"
        params = {
            'origins': f"{origin[0]},{origin[1]}",
            'destinations': f"{destination[0]},{destination[1]}",
            'mode': 'driving',
            'language': GOOGLE_MAPS_CONFIG['LANGUAGE'],
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                element = data['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    distance_km = element['distance']['value'] / 1000  # Convertir a km
                    duration_min = element['duration']['value'] / 60   # Convertir a minutos
                    return distance_km, duration_min
                    
        except Exception as e:
            print(f"Error al consultar Google Maps API: {e}")
            
        return None, None
    
    def _get_simulated_data(self, origin_node, destination_node):
        """
        Datos simulados cuando no hay API key configurada.
        
        Args:
            origin_node: Nodo origen
            destination_node: Nodo destino
            
        Returns:
            tuple: (distancia_km, duracion_minutos)
        """
        # Datos simulados basados en distancias aproximadas en Bogotá
        simulated_data = {
            ('A', 'B'): (15.2, 25),
            ('A', 'C'): (18.5, 30),
            ('A', 'D'): (22.1, 35),
            ('B', 'C'): (8.3, 15),
            ('B', 'D'): (12.7, 22),
            ('B', 'E'): (15.4, 28),
            ('C', 'D'): (6.2, 12),
            ('C', 'F'): (9.8, 18),
            ('D', 'E'): (3.1, 8),
            ('D', 'F'): (4.5, 10),
            ('E', 'F'): (2.8, 6),
            ('E', 'G'): (5.2, 12),
            ('F', 'G'): (3.7, 8),
        }
        
        key = (origin_node, destination_node)
        if key in simulated_data:
            return simulated_data[key]
        
        # Si no está en la tabla, calcular basado en coordenadas
        return self._calculate_approximate_distance(origin_node, destination_node)
    
    def _calculate_approximate_distance(self, origin_node, destination_node):
        """
        Calcula distancia aproximada usando coordenadas.
        
        Args:
            origin_node: Nodo origen
            destination_node: Nodo destino
            
        Returns:
            tuple: (distancia_km, duracion_minutos)
        """
        import math
        
        origin = BOGOTA_LOCATIONS[origin_node]['coordinates']
        destination = BOGOTA_LOCATIONS[destination_node]['coordinates']
        
        # Fórmula de Haversine para distancia aproximada
        lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
        lat2, lon2 = math.radians(destination[0]), math.radians(destination[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radio de la Tierra en km
        r = 6371
        distance_km = c * r
        
        # Estimar duración (velocidad promedio 25 km/h en Bogotá)
        duration_min = (distance_km / 25) * 60
        
        return round(distance_km, 1), round(duration_min, 0)
    
    def generate_route_url(self, path_nodes):
        """
        Genera URL de Google Maps para visualizar la ruta.
        
        Args:
            path_nodes: Lista de nodos que forman la ruta
            
        Returns:
            str: URL para abrir en Google Maps
        """
        if len(path_nodes) < 2:
            return None
            
        # Punto de origen
        origin = BOGOTA_LOCATIONS[path_nodes[0]]['coordinates']
        origin_str = f"{origin[0]},{origin[1]}"
        
        # Punto de destino
        destination = BOGOTA_LOCATIONS[path_nodes[-1]]['coordinates']
        destination_str = f"{destination[0]},{destination[1]}"
        
        # Puntos intermedios (waypoints)
        waypoints = []
        if len(path_nodes) > 2:
            for node in path_nodes[1:-1]:
                coord = BOGOTA_LOCATIONS[node]['coordinates']
                waypoints.append(f"{coord[0]},{coord[1]}")
        
        # Construir URL
        base_url = "https://www.google.com/maps/dir/"
        
        params = {
            'api': 1,
            'origin': origin_str,
            'destination': destination_str,
            'travelmode': 'driving'
        }
        
        if waypoints:
            params['waypoints'] = '|'.join(waypoints)
        
        url = base_url + '?' + urllib.parse.urlencode(params)
        return url
    
    def open_route_in_browser(self, path_nodes):
        """
        Abre la ruta en Google Maps en el navegador.
        
        Args:
            path_nodes: Lista de nodos que forman la ruta
        """
        url = self.generate_route_url(path_nodes)
        if url:
            print(f"🗺️  Abriendo ruta en Google Maps...")
            webbrowser.open(url)
            print(f"🔗 URL: {url}")
        else:
            print("❌ No se pudo generar la URL de la ruta")
    
    def get_location_info(self, node):
        """
        Obtiene información de una ubicación.
        
        Args:
            node: Identificador del nodo
            
        Returns:
            dict: Información de la ubicación
        """
        return BOGOTA_LOCATIONS.get(node, {})
    
    def print_location_details(self, node):
        """
        Imprime detalles de una ubicación.
        
        Args:
            node: Identificador del nodo
        """
        info = self.get_location_info(node)
        if info:
            print(f"📍 {node}: {info['name']}")
            print(f"   📌 {info['address']}")
            print(f"   🌐 {info['coordinates'][0]}, {info['coordinates'][1]}")


def update_graph_with_real_data(graph, maps_api):
    """
    Actualiza el grafo con datos reales de Google Maps.
    
    Args:
        graph: Objeto Graph a actualizar
        maps_api: Instancia de GoogleMapsAPI
    """
    print("🔄 Actualizando grafo con datos reales de Google Maps...")
    
    nodes = graph.get_nodes()
    updated_edges = []
    
    for origin in nodes:
        for destination in nodes:
            if origin != destination:
                distance_km, duration_min = maps_api.get_real_distance_duration(origin, destination)
                if distance_km and duration_min:
                    updated_edges.append((origin, destination, int(duration_min)))
    
    # Crear nuevo grafo con datos actualizados
    from graph import Graph
    new_graph = Graph()
    
    # Agregar nodos
    for node in nodes:
        new_graph.add_node(node)
    
    # Agregar aristas con datos reales
    for origin, destination, duration in updated_edges:
        new_graph.add_edge(origin, destination, duration)
    
    print(f"✅ Grafo actualizado con {len(updated_edges)} conexiones reales")
    return new_graph