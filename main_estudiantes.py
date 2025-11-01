"""
main_estudiantes.py (versión estudiante)
=======================================
Hola! Este archivo lo hice pensando en ENTENDER Dijkstra, no en hacer algo
perfecto. Está todo en un único archivo para leerlo de arriba a abajo sin
abrir más cosas.

Mini índice:
 1. Grafo (diccionario simple) -> tiempos entre puntos (minutos)
 2. Dijkstra (con prints opcionales para ver qué hace por dentro)
 3. Cómo reconstruyo la ruta (usando un diccionario de padres)
 4. Menú en consola (muy simple) + opción de explicación + retos
 5. Ejemplo automático (A -> D) antes de mostrar el menú

Notas personales:
 - Uso float('inf') como "infinito".
 - Distancias = minutos.
 - El diccionario padres me deja reconstruir el camino; sin él solo sabría números.
 - La prioridad la manejo con heapq (cola de prioridad mínima).

Diagrama (boceto rápido, no perfecto):
     A --15--> B --25--> D --10--> E --5--> F --8--> G
     |   \\10    \\                \\10      \\12
     |    20      12
     v      \\
     C --12--> D
     | \\15
     |  \\30
     v    v
     F    E

Cómo ejecutar:
    python main_estudiantes.py

Si te pierdes: ve a la función main() al final y sube desde ahí.
Puedes llamar a retos() dentro de main si quieres ver sugerencias de práctica.
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
    # Dijkstra en una frase (mi resumen):
    #   "Siempre saco el nodo más cercano pendiente y veo si puedo mejorar
    #    las distancias de sus vecinos (relajar)."

    # 1. Inicializamos todas las distancias en infinito menos el origen
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0

    # 2. Diccionario para saber por dónde llegamos a cada nodo
    padres = {nodo: None for nodo in grafo}

    # 3. Cola de prioridad (distancia acumulada, nodo)
    cola = [(0, origen)]

    if ver_pasos:
        print('\n[INICIO DIJKSTRA]')

    while cola:  # Mientras haya candidatos
        # Sacamos el nodo con menor distancia conocida hasta ahora
        dist_actual, nodo = heapq.heappop(cola)

        if ver_pasos:
            print(f"Procesando nodo {nodo} con distancia {dist_actual}")

        # Si la distancia que sacamos ya no es la mejor, la ignoramos (ya hay algo mejor)
        if dist_actual > distancias[nodo]:
            continue

        # Revisamos cada vecino del nodo actual (relajación)
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


def explicar_dijkstra_breve():
    """Imprime un resumen rápido del algoritmo (en estilo estudiante)."""
    print("\nExplicación rápida de Dijkstra:")
    print("1. Empiezo con 0 en el origen y ∞ en los demás.")
    print("2. Saco siempre el nodo 'pendiente' con menor distancia.")
    print("3. Intento mejorar la distancia de cada vecino (relajar).")
    print("4. Si mejoro, actualizo padre[vecino] para reconstruir la ruta luego.")
    print("5. Repito hasta vaciar la cola. Listo.")
    print("6. Ruta = ir desde el destino hacia atrás usando padres y darle la vuelta.")

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
    print('\nSegmentos (qué suma cada tramo):')
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


def retos():
    """Lista de retos prácticos para modificar el código."""
    print('\nRETOS SUGERIDOS:')
    print('1. Cambia el peso A->C a 5. ¿Qué pasa con la ruta A->D?')
    print('2. Agrega un nodo H conectado desde G con peso 4 y prueba A->H.')
    print('3. Elimina la arista D->E y mira si B->E sigue siendo 27.')
    print('4. Crea una función que cuente el número de saltos en la ruta.')
    print('5. Agrega un ciclo (ej: G->A con peso grande) y verifica que no se cuelga.')
    print('6. Añade una opción para mostrar también el padre de cada nodo.')
    print('7. Implementa BFS y compárala con Dijkstra cuando todos los pesos sean 1.')
    print('8. Escribe otra versión sin mirar ésta y luego compara.')


def menu():
    while True:
        print('\n' + '='*50)
        print('SISTEMA DE RUTAS - VERSIÓN ESTUDIANTES')
        print('='*50)
        print('1. Ruta más corta entre dos puntos')
        print('2. Ver todas las distancias desde un origen')
        print('3. Ver ubicaciones')
        print('4. Explicación breve de Dijkstra')
        print('5. Ver retos sugeridos')
        print('6. Salir')
        opcion = input('\nElige una opción (1-6): ').strip()

        if opcion == '1':
            opcion_ruta_mas_corta()
        elif opcion == '2':
            opcion_todas_las_distancias()
        elif opcion == '3':
            mostrar_ubicaciones()
        elif opcion == '4':
            explicar_dijkstra_breve()
        elif opcion == '5':
            retos()
        elif opcion == '6':
            print('\n¡Hasta luego! (Prueba a cambiar un peso y ejecuta de nuevo)')
            break
        else:
            print('Opción inválida (usa 1..6)')

# ---------------------------------------------------------------------------
# 5. EJECUCIÓN DIRECTA / EJEMPLO AUTOMÁTICO
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Ejemplo rápido (antes del menú)
    print('Ejemplo rápido: calcular A -> D')
    dist, padres = dijkstra(GRAFO, 'A')
    ruta = reconstruir_ruta(padres, 'A', 'D')
    print('Ruta A->D:', ' -> '.join(ruta), '| Tiempo =', dist['D'])
    print('(Puedes ver explicación en la opción 4 del menú)')
    menu()
