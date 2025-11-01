import os
import osmnx as ox
from datetime import datetime, timedelta

def download_city_graph(place: str, network_type: str = "drive", use_cache: bool = True, max_age_days: int = 30):
    """
    Descarga o carga desde caché el grafo vial de una ciudad usando OSMnx.

    Args:
        place (str): Nombre de la ciudad o región, por ejemplo: "Bogotá, Colombia".
        network_type (str): Tipo de red ("drive", "walk", "bike", etc.).
        use_cache (bool): Si es True, reutiliza el archivo en caché si existe.
        max_age_days (int): Número máximo de días antes de volver a descargar el grafo.

    Returns:
        networkx.MultiDiGraph: Grafo vial de la ciudad con nodos y aristas.
    """

    # === Preparar ruta del archivo de caché ===
    safe_name = place.lower().replace(",", "").replace(" ", "_")
    cache_dir = os.path.join(os.path.dirname(__file__), "../../data/cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{safe_name}_{network_type}.graphml")

    # === Verificar si el grafo ya existe en caché ===
    if use_cache and os.path.exists(cache_file):
        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))).days
        if file_age_days <= max_age_days:
            print(f"[INFO] Cargando grafo en caché: {cache_file} (edad: {file_age_days} días)")
            G = ox.load_graphml(cache_file)
            return G
        else:
            print(f"[WARN] El grafo tiene {file_age_days} días. Se descargará uno nuevo.")

    # === Descargar el grafo desde OpenStreetMap ===
    print(f"[INFO] Descargando grafo de OSM para: {place} ...")
    G = ox.graph_from_place(place, network_type=network_type)
    print(f"[INFO] Grafo descargado: {G.number_of_nodes():,} nodos, {G.number_of_edges():,} aristas")

    # === Guardar el grafo en caché ===
    ox.save_graphml(G, cache_file)
    print(f"[INFO] Grafo guardado en caché en: {cache_file}")

    return G
