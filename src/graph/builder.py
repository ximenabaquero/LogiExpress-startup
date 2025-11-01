from __future__ import annotations
from collections import defaultdict
from src.api.google_maps import compute_route_duration_seconds
import hashlib
from typing import Dict, Tuple, Optional
import time

def _is_oneway(edge_data: dict) -> bool:
    """
    Determina si la arista es unidireccional según atributos de OSM.
    Acepta variantes como True/'true'/'yes'/1.
    """
    val = edge_data.get("oneway", None)
    if isinstance(val, str):
        val = val.strip().lower()
        return val in ("true", "yes", "1")
    return bool(val)


def _deterministic_sample(u: int, v: int, ratio: float) -> bool:
    """
    Muestreo determinista por arista usando hash MD5 para reproducibilidad.
    Devuelve True si la arista debe muestrearse (consultar API).
    """
    if ratio <= 0.0:
        return False
    if ratio >= 1.0:
        return True
    h = hashlib.md5(f"{u}-{v}".encode()).hexdigest()
    val = int(h[:8], 16) / 0xFFFFFFFF  # mapear a [0,1)
    return val <= ratio


def _call_duration_with_backoff(
        google_maps_api_url: str,
        google_api_key: str,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        max_retries: int = 3,
        backoff_base: float = 0.5,
) -> Optional[float]:
    """
    Llama a Google Routes con reintentos/backoff exponencial.
    Devuelve duración en segundos o None si no es posible obtenerla.
    """
    attempt = 0
    while True:
        try:
            dur_s, dist_m, _raw = compute_route_duration_seconds(
                origin_lat=origin_lat,
                origin_lng=origin_lng,
                dest_lat=dest_lat,
                dest_lng=dest_lng,
                routing_preference="TRAFFIC_AWARE_OPTIMAL",
                departure_time=None,
                traffic_model=None,
                # parámetros propios
                google_maps_api_url=google_maps_api_url,
                google_api_key=google_api_key,
            )
            if dur_s is not None and dur_s > 0:
                return float(dur_s)
            return None
        except Exception:
            attempt += 1
            if attempt > max_retries:
                return None
            # backoff exponencial simple
            sleep_s = backoff_base * (2 ** (attempt - 1))
            time.sleep(sleep_s)


def build_simple_graph(
        google_maps_api_url: str,
        google_api_key: str,
        G,
        weight_type: str = "distance",   # "distance" | "duration"
        sample_ratio: float = 0.001,     # fracción de aristas a consultar en Google (determinista)
        default_speed_kph: float = 25.0, # velocidad por defecto para estimar duración cuando no hay API/resultado
        max_retries: int = 3,
        backoff_base: float = 0.5,
) -> Dict[int, list[Tuple[int, float]]]:
    """
    Construye un grafo simplificado (lista de adyacencia) para algoritmos de ruteo.

    Args:
        google_maps_api_url: endpoint de Google Routes (Directions v2 computeRoutes).
        google_api_key: API key de Google (requerida si weight_type='duration').
        G: grafo de OSMnx (MultiDiGraph dirigido).
        weight_type: "distance" (metros) o "duration" (segundos).
        sample_ratio: fracción de aristas a consultar a Google (determinista por hash).
        default_speed_kph: velocidad por defecto para convertir metros -> segundos en modo "duration".
        max_retries: reintentos por arista para la consulta a Google.
        backoff_base: factor base para backoff exponencial.

    Returns:
        dict: {u: [(v, weight), ...]} usando pesos coherentes al modo escogido.
    """
    graph: Dict[int, list[Tuple[int, float]]] = defaultdict(list)
    edges = list(G.edges(data=True))
    total_edges = len(edges)

    # Caché local de duraciones entre coordenadas (reduce llamadas repetidas)
    duration_cache: Dict[Tuple[float, float, float, float], float] = {}

    # Conversión velocidad -> m/s para estimación de duración
    default_speed_mps = float(default_speed_kph) / 3.6 if default_speed_kph > 0 else 6.94  # ~25 km/h

    for i, (u, v, data) in enumerate(edges):
        # Coordenadas (OSMnx: y=lat, x=lon)
        lat_u, lon_u = float(G.nodes[u]["y"]), float(G.nodes[u]["x"])
        lat_v, lon_v = float(G.nodes[v]["y"]), float(G.nodes[v]["x"])

        # Longitud base en metros (si falta, asume 1.0 para no romper)
        length_m = float(data.get("length", 1.0))
        if length_m <= 0:
            length_m = 1.0

        if weight_type == "distance":
            # Peso = metros (consistente para todo el grafo)
            weight = length_m

        elif weight_type == "duration":
            # Peso = segundos (consistente). Si no hay consulta/resultado, convierte por velocidad por defecto.
            # Muestreo determinista para decidir si se llama a Google por esta arista:
            if _deterministic_sample(u, v, sample_ratio):
                # Redondeo leve de coord para mejorar tasa de acierto en caché (reduce claves “casi iguales”)
                key = (round(lat_u, 5), round(lon_u, 5), round(lat_v, 5), round(lon_v, 5))
                if key in duration_cache:
                    dur_s = duration_cache[key]
                else:
                    dur_s = _call_duration_with_backoff(
                        google_maps_api_url=google_maps_api_url,
                        google_api_key=google_api_key,
                        origin_lat=lat_u,
                        origin_lng=lon_u,
                        dest_lat=lat_v,
                        dest_lng=lon_v,
                        max_retries=max_retries,
                        backoff_base=backoff_base,
                    )
                    if dur_s is not None and dur_s > 0:
                        duration_cache[key] = dur_s

                if dur_s is not None and dur_s > 0:
                    weight = dur_s
                else:
                    # Fallback: estimar tiempo = distancia / velocidad
                    weight = length_m / default_speed_mps
            else:
                # No consultada: estimación por velocidad
                weight = length_m / default_speed_mps

        else:
            raise ValueError("weight_type debe ser 'distance' o 'duration'")

        # Agrega arista u->v
        graph[u].append((v, weight))

        # Si la vía NO es oneway, agrega la arista inversa v->u con el mismo peso
        if not _is_oneway(data):
            graph[v].append((u, weight))


    print(
        f"Grafo simplificado con {len(graph)} nodos (listas de adyacencia), "
        f"modo={weight_type}, edges={total_edges}, cache_durations={len(duration_cache)}"
    )
    return graph