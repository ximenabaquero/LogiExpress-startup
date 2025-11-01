import osmnx as ox
from src.api.google_maps import get_coordinates_from_address
from src.graph.downloader import download_city_graph
from src.graph.builder import build_simple_graph
from src.algorithms.dijkstra import dijkstra
from src.graph.visualizer import plot_route
from src.security.encrypted_env import load_secret


def main():
    """
    Entry point for testing the shortest path calculation in a real city graph.
    """
    load_secret()  # Pide la api key y la guarda cifrada
    google_api_key = load_secret()
    google_maps_api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    # ====================================================
    # 1) Descarga informacion vial. Se limita a Bogota
    # ====================================================
    place = "Bogotá, Colombia"
    print(f"[INFO] Descargando red vial para: {place} ...")
    G = download_city_graph(place, network_type="drive", use_cache=True, max_age_days=30)

    print(f"[INFO] Grapo construido: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges")

    # ====================================================
    # 2) Se construye grafo simplificado (Se puede construir por distancia o tiempo)
    # ====================================================
    weight_mode = "distance"  # "duration" Se obtienen tiempos con la api de google
    graph = build_simple_graph(google_maps_api_url=google_maps_api_url, google_api_key=google_api_key, G=G, weight_type=weight_mode, sample_ratio=0.001)

    # ====================================================
    # 3) Se definen coordenadas de origen y destino (lat/lon)
    # ====================================================
    origin_lat, origin_lng = get_coordinates_from_address(google_api_key=google_api_key, address="a 72c-87, Dg. 81f #72c1, Bogotá")
    print(f"[INFO] Origin lat={origin_lat}, lng={origin_lng}")
    dest_lat, dest_lng = get_coordinates_from_address(google_api_key=google_api_key, address="Dg. 57c Sur #62-60, Bogotá")
    print(f"[INFO] Dest lat={dest_lat}, lng={dest_lng}")
    # Se convierten coordenadas al nodo mas cercano en el grafo obtenido con osmnx
    origin_node = ox.distance.nearest_nodes(G, X=origin_lng, Y=origin_lat)
    dest_node = ox.distance.nearest_nodes(G, X=dest_lng, Y=dest_lat)

    print(f"[INFO] Origin node: {origin_node}, Destination node: {dest_node}")

    # ====================================================
    # 4) Calcular el camino mas corto con Dijkstra
    # ====================================================
    print(f"[INFO] Corriendo Dijkstra basado en {weight_mode} ...")
    path, total_cost = dijkstra(graph, origin_node, dest_node, weight_type=weight_mode)

    if weight_mode == "distance":
        print(f"[RESULT] Distancia mas corta: {total_cost:.2f} meters")
    else:
        print(f"[RESULT] Ruta mas rapida: {total_cost/60:.2f} minutes")

    print(f"[INFO] Path includes {len(path)} nodes")

    # ====================================================
    # 5) Se visualiza trayecto
    # ====================================================
    try:
        plot_route(G, path)
    except Exception as e:
        print(f"[WARN] Could not plot route: {e}")


if __name__ == "__main__":
    main()

