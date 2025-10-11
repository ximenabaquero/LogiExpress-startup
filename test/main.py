import os
import requests
import osmnx as ox

"""
Interfaz CLI para el sistema de rutas de Bogotá.
"""

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

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
google_maps_api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
headers = {
    "Content-Type": "application/json",
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline",
    "X-Goog-Api-Key": GOOGLE_API_KEY,
}

def compute_route_duration_seconds(origin_lat, origin_lng, dest_lat, dest_lng,
                                   routing_preference="TRAFFIC_AWARE",
                                   departure_time=None,  # ej: "2025-10-04T11:00:00-05:00"
                                   traffic_model=None):  # "BEST_GUESS"|"OPTIMISTIC"|"PESSIMISTIC"
    body = {
        "origin": {
            "location": {"latLng": {"latitude": origin_lat, "longitude": origin_lng}}
        },
        "destination": {
            "location": {"latLng": {"latitude": dest_lat, "longitude": dest_lng}}
        },
        "travelMode": "DRIVE",
        "routingPreference": routing_preference,
        "computeAlternativeRoutes": True,
        "routeModifiers": {"avoidTolls": False, "avoidHighways": False, "avoidFerries": False},
        "languageCode": "en-US",
        "units": "METRIC",
    }

    # Opcionales (para predecir tráfico futuro y/o modelo de tráfico)
    if departure_time:
        body["departureTime"] = departure_time
    if traffic_model:
        body["trafficModel"] = traffic_model
        # Nota: para usar trafficModel, Google recomienda TRAFFIC_AWARE_OPTIMAL
        if routing_preference != "TRAFFIC_AWARE_OPTIMAL":
            body["routingPreference"] = "TRAFFIC_AWARE_OPTIMAL"

    r = requests.post(google_maps_api_url, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    data = r.json()

    # Extraer duración y distancia de la 1ª ruta
    route = (data.get("routes") or [None])[0]
    if not route:
        return None, None, data  # Sin ruta (devuelve payload crudo para inspección)

    # duration viene como string tipo "163s" → pásalo a segundos
    dur_str = route.get("duration", "0s")
    dur_seconds = float(dur_str[:-1]) if dur_str.endswith("s") else None
    distance_m = route.get("distanceMeters", None)

    return dur_seconds, distance_m, data

dur_s, dist_m, raw = compute_route_duration_seconds(
    origin_lat=4.70159, origin_lng=-74.14690,
    dest_lat=4.66778, dest_lng=-74.09056,
    routing_preference="TRAFFIC_AWARE_OPTIMAL"
)




print("Duración (s):", dur_s)
print("Duración (min):", dur_s/60)
print("Distancia (m):", dist_m)
print("Raw:", raw)