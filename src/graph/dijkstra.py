import heapq
def dijkstra(grafo: dict, origen: str, ver_pasos: bool = False):
    """
    Calcula las distancias más cortas desde 'origen' a todos los nodos.

    Parámetros:
        grafo: dict con la estructura {nodo: [(vecino, peso), ...]}
        origen: nodo desde el cual comenzamos
        ver_pasos: si True, imprime el proceso interno paso a paso

    Retorna:
        distancias: dict con la mejor distancia encontrada a cada nodo
        padres: dict para poder reconstruir rutas (padres[n] = nodo anterior)
    """
    # 1. Inicializamos todas las distancias en infinito menos el origen
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0

    # 2. Diccionario para saber por dónde llegamos a cada nodo
    padres = {nodo: None for nodo in grafo}

    # 3. Cola de prioridad (distancia acumulada, nodo)
    cola = [(0, origen)]

    if ver_pasos:
        print('\n[INICIO DIJKSTRA]')

    while cola:
        # Sacamos el nodo con menor distancia conocida hasta ahora
        dist_actual, nodo = heapq.heappop(cola)

        if ver_pasos:
            print(f"Procesando nodo {nodo} con distancia {dist_actual}")

        # Si la distancia que sacamos ya no es la mejor, la ignoramos
        if dist_actual > distancias[nodo]:
            continue

        # Revisamos cada vecino del nodo actual
        for vecino, peso in grafo[nodo]:
            nueva_dist = dist_actual + peso

            if ver_pasos:
                print(f"  Vecino {vecino}: distancia actual={distancias[vecino]} posible nueva={nueva_dist}")

            # Si encontramos un mejor camino, actualizamos
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                padres[vecino] = nodo  # Llegamos a 'vecino' desde 'nodo'
                heapq.heappush(cola, (nueva_dist, vecino))
                if ver_pasos:
                    print(f"    ✅ Actualizado {vecino}: {nueva_dist} (padre={nodo})")

    if ver_pasos:
        print('[FIN DIJKSTRA]\n')

    return distancias, padres