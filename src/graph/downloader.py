import osmnx as ox

def download_city_graph(place: str, network_type: str = "drive"):
    print(f"Descargando red de {place}…")
    G = ox.graph_from_place(place, network_type=network_type)
    print(f"Nodos: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")
    return G