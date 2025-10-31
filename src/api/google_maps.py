import requests
import unicodedata

def google_key_sanity_check(google_api_key: str) -> bool:
    # ping muy barato: geocode “Bogotá, Colombia”
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": "Bogotá, Colombia", "key": google_api_key}
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        return data.get("status") == "OK"
    except Exception:
        return False

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

def _normalize_address(addr: str) -> str:
    # Comentarios en español, variables en inglés
    # Normaliza caracteres y expande abreviaturas comunes en Colombia
    s = unicodedata.normalize("NFKC", addr).strip()
    s = s.replace("Dg.", "Diagonal ").replace("Diag.", "Diagonal ")
    s = s.replace("Cl.", "Calle ").replace("Cra.", "Carrera ")
    s = s.replace("#", " # ").replace("  ", " ")
    return s

def get_coordinates_from_address(
        google_api_key: str,
        address: str,
        *,
        city_hint: str | None = "Bogotá, Colombia",
        bounds: tuple[tuple[float, float], tuple[float, float]] | None = None,
        region: str = "co",
        language: str = "es",
):
    """
    Geocodifica con Google. Devuelve (lat, lng) en float o (None, None) si no hay resultados.
    Acepta:
      - city_hint: texto agregado para sesgar la búsqueda (si no está ya en address)
      - bounds: ((sw_lat, sw_lng), (ne_lat, ne_lng)) para sesgo adicional
      - region, language: preferencia regional/idioma
    """
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    addr = _normalize_address(address)
    if city_hint and city_hint.lower() not in addr.lower():
        addr = f"{addr}, {city_hint}"

    params = {
        "address": addr,
        "key": google_api_key,
        "language": language,
        "region": region,
        "components": "country:CO",  # restringe a Colombia
    }
    if bounds:
        (sw_lat, sw_lng), (ne_lat, ne_lng) = bounds
        params["bounds"] = f"{sw_lat},{sw_lng}|{ne_lat},{ne_lng}"

    r = requests.get(endpoint, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()

    status = data.get("status", "UNKNOWN")
    if status != "OK" or not data.get("results"):
        print(f"[WARN] Google Geocoding status={status} results=0 addr='{addr}'")
        return None, None

    loc = data["results"][0]["geometry"]["location"]
    lat, lng = float(loc["lat"]), float(loc["lng"])
    print(f"[INFO] Geocoded: '{addr}' -> lat={lat}, lng={lng}")
    return lat, lng
