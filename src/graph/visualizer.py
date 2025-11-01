# Render interactivo con GeoPandas.explore

# Comentarios en español, variables en inglés.
import os
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point

def plot_route_explore_compliant(
        G,
        route_nodes,
        save_path="data/outputs/route_map.html",
        show_network=False,
        network_padding_deg=0.01,
):
    """
    Render interactivo con GeoPandas.explore SIN fijar zoom inicial.
    - No usa helpers deprecados de OSMnx.
    - Crea un mapa base vacío con .explore() (sin centrar/zoom manual),
      agrega capas, y al final hace fit_bounds a la ruta.
    """

    if not route_nodes or len(route_nodes) < 2:
        raise ValueError("Ruta muy corta para dibujar (>=2 nodos).")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 1) Grafo -> GeoDataFrames
    nodes_all, edges_all = ox.graph_to_gdfs(G, nodes=True, edges=True)

    # 2) Ruta -> GeoDataFrames (firma cambia según versión de OSMnx)
    r = ox.routing.route_to_gdf(G, route_nodes)
    if isinstance(r, tuple) and len(r) == 2:
        route_nodes_gdf, route_edges_gdf = r
    else:
        route_edges_gdf = r
        idx = [n for n in route_nodes if n in nodes_all.index]
        route_nodes_gdf = nodes_all.loc[idx].copy()
        if "geometry" not in route_nodes_gdf.columns or route_nodes_gdf.geometry.isna().any():
            route_nodes_gdf["geometry"] = [Point(G.nodes[n]["x"], G.nodes[n]["y"]) for n in idx]
            route_nodes_gdf = gpd.GeoDataFrame(route_nodes_gdf, geometry="geometry", crs=nodes_all.crs)

    # 3) Construir polilínea en [lat, lon] para encuadre final sin confusiones
    latlngs = [[float(G.nodes[n]["y"]), float(G.nodes[n]["x"])] for n in route_nodes]
    south = min(p[0] for p in latlngs)
    north = max(p[0] for p in latlngs)
    west  = min(p[1] for p in latlngs)
    east  = max(p[1] for p in latlngs)

    # 4) (Opcional) recorte de red alrededor de la ruta para aligerar el HTML
    edges_clip = edges_all
    if show_network:
        min_lat = south - network_padding_deg
        max_lat = north + network_padding_deg
        min_lon = west  - network_padding_deg
        max_lon = east  + network_padding_deg
        # GeoPandas.cx usa lon,lat en ese orden:
        edges_clip = edges_all.cx[min_lon:max_lon, min_lat:max_lat]

    # 5) Crear mapa base con .explore() sin fijar zoom/centro (clave para “como antes”)
    #    Mapa vacío/ligero como base:
    base_empty = edges_clip.head(0)  # GDF vacío con el mismo CRS
    m = base_empty.explore(tiles="CartoDB positron", name="Base")

    # 6) Capas: red (opcional), ruta, origen/destino/intermedios
    if show_network and not edges_clip.empty:
        edges_clip.explore(
            m=m,
            name="Street network",
            style_kwds={"weight": 1, "opacity": 0.25},
        )

    route_edges_gdf.explore(
        m=m,
        name="Route",
        color="red",
        style_kwds={"weight": 5, "opacity": 0.9},
    )

    if not route_nodes_gdf.empty:
        first_id = route_nodes[0]
        last_id  = route_nodes[-1]
        if first_id in route_nodes_gdf.index:
            route_nodes_gdf.loc[[first_id]].explore(
                m=m, name="Origin", color="green", marker_kwds={"radius": 6}
            )
        if last_id in route_nodes_gdf.index:
            route_nodes_gdf.loc[[last_id]].explore(
                m=m, name="Destination", color="black", marker_kwds={"radius": 6}
            )
        inter_ids = [n for n in route_nodes[1:-1] if n in route_nodes_gdf.index]
        if inter_ids:
            route_nodes_gdf.loc[inter_ids].explore(
                m=m, name="Route nodes", color="red", marker_kwds={"radius": 3}
            )

    # 7) Encadrar a la ruta (bounds en [lat, lon]) y guardar
    m.fit_bounds([[south, west], [north, east]])
    m.save(save_path)
    return save_path
