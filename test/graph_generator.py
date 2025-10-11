import osmnx as ox
import networkx as nx

PLACE = "Bogotá, Colombia"

print("Descargando red…")
G = ox.graph_from_place(PLACE, network_type="drive")

# 1) métricas básicas
print(f"Nodos: {G.number_of_nodes():,}")
print(f"Aristas (dirigidas): {G.number_of_edges():,}")

# 2) muestra algunos nodos con coordenadas
some_nodes = list(G.nodes())[:5]
print("Ejemplo de nodos (id -> (lat, lon)):")
for n in some_nodes:
    print(f"  {n} -> ({G.nodes[n]['y']:.6f}, {G.nodes[n]['x']:.6f})")

# 3) recorre aristas y arma 'edges' y 'pairs'
edges = []
pairs = []
for u, v, k, data in G.edges(keys=True, data=True):
    lat_u = G.nodes[u]["y"]; lon_u = G.nodes[u]["x"]
    lat_v = G.nodes[v]["y"]; lon_v = G.nodes[v]["x"]
    edges.append((u, v, k))
    pairs.append(((lat_u, lon_u), (lat_v, lon_v)))

print(f"Total edges recopiladas: {len(edges):,}")
print(f"Total pairs (origen->destino): {len(pairs):,}")

# 4) muestra algunas aristas con longitudes
print("Ejemplo de aristas:")
for (u, v, k) in edges[:5]:
    length = G[u][v][k].get("length", None)
    print(f"  {u} -> {v} (k={k}) length={length:.1f} m" if length else f"  {u} -> {v} (k={k})")

# 5) muestra algunos pares lat/lon
print("Ejemplo de pairs (lat_u, lon_u) -> (lat_v, lon_v):")
for p in pairs[:5]:
    print("  ", p)

# 6) validaciones simples
assert len(edges) == len(pairs), "edges y pairs deben tener el mismo tamaño"
assert all(-90 <= lat <= 90 and -180 <= lon <= 180 for (lat, lon), _ in pairs[:100]), "coords fuera de rango"
assert all(-90 <= lat <= 90 and -180 <= lon <= 180 for _, (lat, lon) in pairs[:100]), "coords fuera de rango"

print("OK: grafo y pares construidos correctamente.")
