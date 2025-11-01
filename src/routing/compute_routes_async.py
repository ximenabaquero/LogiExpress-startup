from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Dict

import osmnx as ox
import numpy as np


GeocoderFn = Callable[..., Tuple[Optional[float], Optional[float]]]
DijkstraFn = Callable[..., Tuple[list[int], float]]


@dataclass
class RouteResult:
    """Resultado estructurado del cálculo de ruta."""
    path_nodes: list[int]
    total_cost: float
    weight_type: str  # "distance" | "duration"
    origin_node: int
    dest_node: int
    origin_lat: float
    origin_lng: float
    dest_lat: float
    dest_lng: float


def _as_float(value) -> float:
    """Normaliza a float y valida finitud."""
    if value is None:
        raise ValueError("Valor None no válido para coordenada.")
    if isinstance(value, (list, tuple)) and value:
        value = value[0]
    if isinstance(value, str):
        value = value.strip().replace(",", ".")
    f = float(value)
    if not np.isfinite(f):
        raise ValueError(f"Valor no finito: {value}")
    return f


def _graph_bounds_latlon(G) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Devuelve ((sw_lat, sw_lng), (ne_lat, ne_lng)) a partir del grafo."""
    nodes_gdf, _ = ox.graph_to_gdfs(G, nodes=True, edges=True)
    minx, miny, maxx, maxy = nodes_gdf.total_bounds  # lon, lat
    return (miny, minx), (maxy, maxx)


async def compute_route_async(
        G,
        graph_simple: Dict[int, list[tuple[int, float]]],
        dijkstra_fn: DijkstraFn,
        get_coordinates_from_address: GeocoderFn,
        origin_text: str,
        dest_text: str,
        google_api_key: str,
        weight_type: str = "distance",
        timeout_seconds: int = 25,
) -> RouteResult:
    """
    Calcula la ruta de forma asíncrona usando SIEMPRE Google (requiere API key):
      1) Geocodifica origen y destino con sesgo de bounds del grafo y city_hint.
      2) Normaliza/valida coordenadas; nearest_nodes con arrays.
      3) Ejecuta Dijkstra con el grafo simplificado.
      4) Devuelve RouteResult.
    """
    if not google_api_key:
        raise ValueError("Google API key es obligatoria para geocodificar direcciones.")

    # 0) bounds del grafo para sesgar la geocodificación
    sw, ne = _graph_bounds_latlon(G)

    async def _geocode_google(addr: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Envuelve la llamada al geocoder de Google en un hilo,
        pasando bounds y city_hint si la firma lo soporta.
        """
        def _call():
            try:
                # Firma extendida: (key, address, city_hint=..., bounds=..., region=..., language=...)
                return get_coordinates_from_address(
                    google_api_key,
                    addr,
                    city_hint="Bogotá, Colombia",
                    bounds=(sw, ne),
                    region="co",
                    language="es",
                )
            except TypeError:
                # Firma antigua: (key, address)
                return get_coordinates_from_address(google_api_key, addr)

        return await asyncio.to_thread(_call)

    async def _geocode_or_fail(addr: str) -> Tuple[float, float]:
        lat, lng = await _geocode_google(addr)
        if lat is None or lng is None:
            raise ValueError(f"No se pudo geocodificar: {addr}")
        return float(lat), float(lng)

    async def _compute() -> RouteResult:
        # 1) Geocodificar con Google (obligatorio)
        o_lat, o_lng = await _geocode_or_fail(origin_text)
        d_lat, d_lng = await _geocode_or_fail(dest_text)

        # 2) Normalizar/validar
        o_lat = _as_float(o_lat); o_lng = _as_float(o_lng)
        d_lat = _as_float(d_lat); d_lng = _as_float(d_lng)
        for name, lat, lng in [("origen", o_lat, o_lng), ("destino", d_lat, d_lng)]:
            if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                raise ValueError(f"Coordenadas fuera de rango para {name}: lat={lat}, lng={lng}")

        # 3) nearest_nodes pasando arrays (compatibilidad con versiones que usan .any())
        origin_node = ox.distance.nearest_nodes(G, X=[o_lng], Y=[o_lat])[0]
        dest_node   = ox.distance.nearest_nodes(G, X=[d_lng], Y=[d_lat])[0]

        # 4) Dijkstra (en hilo)
        path, total_cost = await asyncio.to_thread(
            dijkstra_fn, graph_simple, origin_node, dest_node, weight_type
        )

        return RouteResult(
            path_nodes=path,
            total_cost=total_cost,
            weight_type=weight_type,
            origin_node=origin_node,
            dest_node=dest_node,
            origin_lat=o_lat,
            origin_lng=o_lng,
            dest_lat=d_lat,
            dest_lng=d_lng,
        )

    # Timeout exterior para todo el flujo
    return await asyncio.wait_for(_compute(), timeout=timeout_seconds)
