import osmnx as ox
import os
from src.api.google_maps import get_coordinates_from_address
from src.graph.downloader import download_city_graph
from src.graph.builder import build_simple_graph
from src.algorithms.dijkstra import dijkstra
from src.graph.visualizer import plot_route


def main():
    """
    Entry point for testing the shortest path calculation in a real city graph.
    """
    GOOGLE_API_KEY = "AIzaSyBW5dD65JCw0tA5mmRdhfxJS7SBhHY_vEs"
    google_maps_api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    # ====================================================
    # 1) Download the street network (only once per city)
    # ====================================================
    place = "Bogotá, Colombia"
    print(f"[INFO] Downloading street network for: {place} ...")
    G = download_city_graph(place, network_type="drive")

    print(f"[INFO] Graph ready: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges")

    # ====================================================
    # 2) Build a simplified graph (choose distance or duration)
    # ====================================================
    weight_mode = "distance"  # or "duration" to use Google Maps travel times
    graph = build_simple_graph(google_maps_api_url=google_maps_api_url, GOOGLE_API_KEY=GOOGLE_API_KEY, G=G, weight_type=weight_mode, sample_ratio=0.001)

    # ====================================================
    # 3) Define origin and destination coordinates (lat/lon)
    # ====================================================
    origin_lat, origin_lng = get_coordinates_from_address(google_api_key=GOOGLE_API_KEY, address="Avenida Calle 80 No. 100 - 52 Local 73 - 76, Bogotá D.C, Cundinamarca")
    print(f"[INFO] Origin lat={origin_lat}, lng={origin_lng}")
    dest_lat, dest_lng = get_coordinates_from_address(google_api_key=GOOGLE_API_KEY, address="Cra. 11 #78 - 47, Bogotá")
    print(f"[INFO] Dest lat={dest_lat}, lng={dest_lng}")
    # Convert coordinates to nearest nodes in the OSMnx graph
    origin_node = ox.distance.nearest_nodes(G, X=origin_lng, Y=origin_lat)
    dest_node = ox.distance.nearest_nodes(G, X=dest_lng, Y=dest_lat)

    print(f"[INFO] Origin node: {origin_node}, Destination node: {dest_node}")

    # ====================================================
    # 4) Compute shortest path using your custom Dijkstra
    # ====================================================
    print(f"[INFO] Running Dijkstra based on {weight_mode} ...")
    path, total_cost = dijkstra(graph, origin_node, dest_node, weight_type=weight_mode)

    if weight_mode == "distance":
        print(f"[RESULT] Shortest distance: {total_cost:.2f} meters")
    else:
        print(f"[RESULT] Fastest route: {total_cost/60:.2f} minutes")

    print(f"[INFO] Path includes {len(path)} nodes")

    # ====================================================
    # 5) Visualize the route (optional)
    # ====================================================
    try:
        plot_route(G, path)
    except Exception as e:
        print(f"[WARN] Could not plot route: {e}")


if __name__ == "__main__":
    main()

