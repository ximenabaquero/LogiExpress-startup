from collections import defaultdict
from src.api.google_maps import compute_route_duration_seconds
import random
import time

def build_simple_graph(google_maps_api_url, headers, G, weight_type="distance", sample_ratio=0.001):
    """
    Construye un grafo simplificado para algoritmos de rutas.

    Args:
        G: grafo de OSMnx
        weight_type: "distance" o "duration"
        sample_ratio: para limitar llamadas API (por ejemplo, 0.001 usa 0.1% de aristas)
    """
    graph = defaultdict(list)
    edges = list(G.edges(data=True))
    total_edges = len(edges)

    for i, (u, v, data) in enumerate(edges):
        lat_u, lon_u = G.nodes[u]["y"], G.nodes[u]["x"]
        lat_v, lon_v = G.nodes[v]["y"], G.nodes[v]["x"]

        if weight_type == "distance":
            weight = data.get("length", 1.0)

        elif weight_type == "duration":
            # (1) Límite de llamadas API
            if random.random() > sample_ratio:
                # Usa fallback (distancia) si no se llama API
                weight = data.get("length", 1.0)
            else:
                dur_s, dist_m, _ = compute_route_duration_seconds(
                    google_maps_api_url= google_maps_api_url,
                    headers = headers,
                    origin_lat=lat_u,
                    origin_lng=lon_u,
                    dest_lat=lat_v,
                    dest_lng=lon_v,
                    routing_preference="TRAFFIC_AWARE_OPTIMAL"
                )
                weight = dur_s if dur_s else data.get("length", 1.0)
                time.sleep(0.1)  # evitar rate limit

        graph[u].append((v, weight))

    print(f"Grafo simplificado con {len(graph)} nodos y modo={weight_type}")
    return graph
