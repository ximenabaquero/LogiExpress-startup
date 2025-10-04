"""
main_estudiantes.py
====================
Versión SÚPER SIMPLE del sistema de rutas pensada para estudiantes que recién
empiezan con grafos y algoritmos de caminos más cortos.

IDEA CLAVE: Mostrar de la forma más clara posible cómo funciona Dijkstra.

Contenido del archivo (todo en un solo lugar para que sea fácil de leer):
1. Definición del grafo (nodos y aristas) usando un diccionario
2. Algoritmo de Dijkstra paso a paso (con opción de ver cada iteración)
3. Función para reconstruir la ruta encontrada
4. Menú muy sencillo para interactuar
5. Ejemplo automático si se ejecuta directamente

NOTA: Esta versión NO usa clases ni archivos separados para que sea
más fácil seguir la lógica en orden.
"""

import heapq  # Proporciona una cola de prioridad eficiente

# ---------------------------------------------------------------------------
# 1. DEFINICIÓN DEL GRAFO
# ---------------------------------------------------------------------------
# Representamos el grafo como un diccionario donde:
#   - La llave es el nombre del nodo ("A", "B", ...)
#   - El valor es una lista de tuplas (vecino, peso)
# El "peso" representa el tiempo (en minutos) entre las ubicaciones.
# Este grafo fue diseñado para que las rutas A->D = 32 y B->E = 27.
GRAFO = {
    'A': [('B', 15), ('C', 20), ('F', 35)],
    'B': [('D', 25), ('C', 10), ('E', 27)],
    'C': [('D', 12), ('F', 15), ('E', 30)],
    'D': [('E', 10), ('F', 10)],
    'E': [('F', 5), ('G', 12)],
    'F': [('G', 8)],
    'G': []  # G no tiene salidas
}

# Diccionario opcional para mostrar nombres amigables (pueden cambiarlo)
NOMBRES = {
    'A': 'Aeropuerto',
    'B': 'Terminal',
    'C': 'Simón Bolívar',
    'D': 'Museo del Oro',
    'E': 'Monserrate',
    'F': 'Zona T',
    'G': 'EAN'
}

# ---------------------------------------------------------------------------
# 2. ALGORITMO DE DIJKSTRA (VERSIÓN EXPLICADA)
# ---------------------------------------------------------------------------
# Objetivo: Encontrar el tiempo mínimo desde un nodo origen hasta todos los demás.
# Idea básica:
#   - Empezamos con distancia 0 para el origen y ∞ (infinito) para los demás.
#   - Usamos una cola de prioridad que siempre extrae el nodo "más cercano" aún
#     no procesado.
#   - Intentamos mejorar (relajar) las distancias a los vecinos.
#   - Repetimos hasta que no quedan nodos en la cola.

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

# ---------------------------------------------------------------------------
# 3. RECONSTRUCCIÓN DE RUTA
# ---------------------------------------------------------------------------
# Usamos el diccionario 'padres' para regresar desde el destino hasta el origen.

def reconstruir_ruta(padres: dict, origen: str, destino: str):
    if padres[destino] is None and destino != origen:
        return None  # No hay ruta
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]
    ruta.reverse()
    return ruta

# ---------------------------------------------------------------------------
# 4. MENÚ INTERACTIVO MUY SIMPLE
# ---------------------------------------------------------------------------

def mostrar_ubicaciones():
    print('\nUbicaciones disponibles:')
    for k in GRAFO:
        print(f"  {k} - {NOMBRES[k]}")


def opcion_ruta_mas_corta():
    mostrar_ubicaciones()
    origen = input('\nOrigen: ').strip().upper()
    destino = input('Destino: ').strip().upper()

    if origen not in GRAFO or destino not in GRAFO:
        print('❌ Nodo inválido')
        return

    ver = input('¿Ver pasos internos de Dijkstra? (s/N): ').lower().strip() == 's'
    distancias, padres = dijkstra(GRAFO, origen, ver_pasos=ver)
    ruta = reconstruir_ruta(padres, origen, destino)

    if not ruta:
        print('No existe ruta')
        return

    print('\nResultado:')
    print('  Ruta: ' + ' -> '.join(ruta))
    print(f"  Tiempo total: {distancias[destino]} minutos")

    # Mostrar tabla de segmentos
    print('\nSegmentos:')
    acumulado = 0
    for i in range(len(ruta) - 1):
        a, b = ruta[i], ruta[i+1]
        # Buscar peso de a->b
        peso = next(p for v, p in GRAFO[a] if v == b)
        acumulado += peso
        print(f"  {a} -> {b}: {peso} (acumulado: {acumulado})")


def opcion_todas_las_distancias():
    mostrar_ubicaciones()
    origen = input('\nOrigen: ').strip().upper()
    if origen not in GRAFO:
        print('❌ Nodo inválido')
        return
    distancias, padres = dijkstra(GRAFO, origen)
    print(f"\nDistancias mínimas desde {origen}:")
    for nodo, d in distancias.items():
        ruta = reconstruir_ruta(padres, origen, nodo)
        if ruta:
            print(f"  {origen} -> {nodo}: {d} min | Ruta: {' -> '.join(ruta)}")


def menu():
    while True:
        print('\n' + '='*50)
        print('SISTEMA DE RUTAS - VERSIÓN ESTUDIANTES')
        print('='*50)
        print('1. Ruta más corta entre dos puntos')
        print('2. Ver todas las distancias desde un origen')
        print('3. Ver ubicaciones')
        print('4. Salir')
        opcion = input('\nElige una opción (1-4): ').strip()

        if opcion == '1':
            opcion_ruta_mas_corta()
        elif opcion == '2':
            opcion_todas_las_distancias()
        elif opcion == '3':
            mostrar_ubicaciones()
        elif opcion == '4':
            print('\n¡Hasta luego!')
            break
        else:
            print('Opción inválida')

# ---------------------------------------------------------------------------
# 5. EJECUCIÓN DIRECTA / EJEMPLO AUTOMÁTICO
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Ejemplo rápido para que se vea algo al ejecutar sin interactuar
    print('Ejemplo rápido: calcular A -> D')
    dist, padres = dijkstra(GRAFO, 'A')
    ruta = reconstruir_ruta(padres, 'A', 'D')
    print('Ruta A->D:', ' -> '.join(ruta), '| Tiempo =', dist['D'])

    # Luego lanzar el menú
    menu()
