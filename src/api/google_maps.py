import requests

def compute_route_duration_seconds(google_maps_api_url, google_api_key, origin_lat, origin_lng, dest_lat, dest_lng,
                                   routing_preference="TRAFFIC_AWARE",
                                   departure_time=None,
                                   traffic_model=None):

    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline",
        "X-Goog-Api-Key": google_api_key,
    }

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

def get_coordinates_from_address(google_api_key, address: str):
    """
    Gets latitude and longitude from a given address or place name using Google Maps Geocoding API.
    """
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": google_api_key}

    response = requests.get(endpoint, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not data["results"]:
        print(f"[WARN] No results found for: {address}")
        return None, None

    location = data["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]
    print(f"[INFO] {address} -> lat={lat}, lng={lng}")
    return lat, lng