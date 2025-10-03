# Guía de Uso - Sistema de Rutas de Bogotá

## Inicio Rápido

### 1. Ejecutar la Aplicación Interactiva

```bash
python main.py
```

La aplicación presentará un menú interactivo con las siguientes opciones:

```
============================================================
SISTEMA DE RUTAS DE BOGOTÁ - LOGIEXPRESS
============================================================
1. Ruta más corta origen → destino
2. Todas las rutas desde un origen
3. Matriz de todos los pares de distancias
4. Ver ubicaciones
5. Salir
============================================================
```

### 2. Ejecutar la Demostración

Para ver todas las funcionalidades del sistema en acción:

```bash
python demo.py
```

Este script ejecuta automáticamente ejemplos de todas las características del sistema.

### 3. Ejecutar Tests

Para verificar que el sistema funciona correctamente:

```bash
python test_graph.py
```

Todos los tests deben pasar, incluyendo los casos requeridos:
- A → D = 32 minutos ✓
- B → E = 27 minutos ✓

## Uso de la Interfaz CLI

### Opción 1: Ruta más corta origen → destino

Esta opción calcula la ruta más corta entre dos ubicaciones usando el algoritmo de Dijkstra.

**Ejemplo:**
```
Seleccione una opción (1-5): 1

--- RUTA MÁS CORTA ---
Ingrese el nodo origen (A-G): A
Ingrese el nodo destino (A-G): D

Origen: A (Aeropuerto)
Destino: D (Museo del Oro)

============================================================
VISUALIZACIÓN DE RUTA
============================================================

Ruta: A → C → D
Distancia total: 32 minutos

------------------------------------------------------------
TABLA DE SEGMENTOS
------------------------------------------------------------
Desde      Hacia      Tiempo          Acumulado      
------------------------------------------------------------
A          C          20              20             
C          D          12              32             
------------------------------------------------------------
```

**Características:**
- Muestra la ruta completa con flechas
- Indica el tiempo total del trayecto
- Desglosa cada segmento del viaje
- Muestra tiempos acumulados en cada punto

### Opción 2: Todas las rutas desde un origen

Muestra todas las rutas posibles desde una ubicación origen a todos los demás destinos.

**Ejemplo:**
```
Seleccione una opción (1-5): 2

--- TODAS LAS RUTAS DESDE UN ORIGEN ---
Ingrese el nodo origen (A-G): A

Origen: A (Aeropuerto)

============================================================
TODAS LAS RUTAS DESDE A
============================================================
Destino    Distancia       Ruta                          
------------------------------------------------------------
B          15              A → B                         
C          20              A → C                         
D          32              A → C → D                     
E          42              A → B → E                     
F          35              A → F                         
G          43              A → F → G                     
------------------------------------------------------------
```

**Características:**
- Calcula rutas a todos los destinos simultáneamente
- Usa el algoritmo de Dijkstra desde el origen
- Muestra distancias y rutas completas
- Indica cuando no hay ruta disponible (∞)

### Opción 3: Matriz de todos los pares de distancias

Muestra una matriz completa con las distancias más cortas entre todos los pares de ubicaciones usando Floyd-Warshall.

**Ejemplo:**
```
Seleccione una opción (1-5): 3

--- MATRIZ DE TODOS LOS PARES ---

============================================================
MATRIZ DE TODAS LAS DISTANCIAS (FLOYD-WARSHALL)
============================================================
   |   A    |   B    |   C    |   D    |   E    |   F    |   G    |
-------------------------------------------------------------------
 A |   0    |   15   |   20   |   32   |   42   |   35   |   43   |
 B |   ∞    |   0    |   10   |   22   |   27   |   25   |   33   |
 C |   ∞    |   ∞    |   0    |   12   |   22   |   15   |   23   |
 D |   ∞    |   ∞    |   ∞    |   0    |   10   |   10   |   18   |
 E |   ∞    |   ∞    |   ∞    |   ∞    |   0    |   5    |   12   |
 F |   ∞    |   ∞    |   ∞    |   ∞    |   ∞    |   0    |   8    |
 G |   ∞    |   ∞    |   ∞    |   ∞    |   ∞    |   ∞    |   0    |
-------------------------------------------------------------------
```

**Características:**
- Calcula todas las distancias de una sola vez
- Formato de matriz fácil de leer
- El símbolo ∞ indica que no hay ruta disponible
- La diagonal siempre es 0 (distancia de un nodo a sí mismo)

### Opción 4: Ver ubicaciones

Muestra la leyenda completa de ubicaciones con sus códigos.

**Ejemplo:**
```
============================================================
UBICACIONES EN BOGOTÁ
============================================================
A: Aeropuerto
B: Terminal
C: Simón Bolívar
D: Museo del Oro
E: Monserrate
F: Zona T
G: EAN
============================================================
```

## Uso Programático

### Importar los módulos

```python
from graph import create_bogota_graph
from algorithms import dijkstra, floyd_warshall, reconstruct_path
from visualization import visualize_path
```

### Ejemplo: Calcular ruta más corta

```python
# Crear el grafo
graph = create_bogota_graph()

# Ejecutar Dijkstra desde el nodo A
distances, predecessors = dijkstra(graph, 'A')

# Reconstruir la ruta de A a D
path = reconstruct_path(predecessors, 'A', 'D')

# Visualizar la ruta
visualize_path(path, distances, graph)
```

### Ejemplo: Usar Floyd-Warshall

```python
# Crear el grafo
graph = create_bogota_graph()

# Ejecutar Floyd-Warshall
distances, next_node = floyd_warshall(graph)

# Obtener distancia entre A y D
distance_a_d = distances['A']['D']
print(f"Distancia de A a D: {distance_a_d} minutos")
```

### Ejemplo: Crear un grafo personalizado

```python
from graph import Graph

# Crear un nuevo grafo
my_graph = Graph()

# Agregar nodos
my_graph.add_node('X')
my_graph.add_node('Y')
my_graph.add_node('Z')

# Agregar aristas (from, to, weight)
my_graph.add_edge('X', 'Y', 10)
my_graph.add_edge('Y', 'Z', 5)
my_graph.add_edge('X', 'Z', 20)

# Usar algoritmos
from algorithms import dijkstra
distances, predecessors = dijkstra(my_graph, 'X')
print(f"Distancia de X a Z: {distances['Z']} minutos")
```

## Casos de Uso Comunes

### 1. Planificar una ruta de viaje

**Escenario:** Necesitas ir del Aeropuerto (A) al Museo del Oro (D).

```bash
python main.py
# Seleccionar opción 1
# Origen: A
# Destino: D
# Resultado: A → C → D (32 minutos)
```

### 2. Explorar todas las opciones desde una ubicación

**Escenario:** Estás en la Terminal (B) y quieres saber a dónde puedes llegar.

```bash
python main.py
# Seleccionar opción 2
# Origen: B
# Ver todas las rutas disponibles
```

### 3. Comparar rutas entre múltiples destinos

**Escenario:** Quieres ver una tabla completa de tiempos de viaje.

```bash
python main.py
# Seleccionar opción 3
# Ver matriz completa de distancias
```

## Algoritmos Implementados

### Dijkstra (Single Source Shortest Path)

**Complejidad:** O((V + E) log V)

**Uso:**
- Mejor para calcular rutas desde un único origen
- Más eficiente cuando solo necesitas rutas desde un punto
- Implementado con cola de prioridad (heap)

**Cuándo usar:**
- Planificar una ruta específica
- Explorar destinos desde un origen
- Navegación en tiempo real

### Floyd-Warshall (All Pairs Shortest Path)

**Complejidad:** O(V³)

**Uso:**
- Calcula todas las rutas entre todos los pares de nodos
- Mejor cuando necesitas una matriz completa de distancias
- Útil para análisis y planificación general

**Cuándo usar:**
- Generar tablas de tiempos completas
- Análisis de red completo
- Preprocesamiento para múltiples consultas

## Estructura de Datos

### Lista de Adyacencia

**Ventajas:**
- Eficiente para grafos dispersos
- Usa menos memoria
- Rápida para iterar sobre vecinos

**Formato:**
```python
{
    'A': [('B', 15), ('C', 20), ('F', 35)],
    'B': [('D', 25), ('C', 10), ('E', 27)],
    ...
}
```

### Matriz de Adyacencia

**Ventajas:**
- Acceso O(1) a pesos de aristas
- Ideal para Floyd-Warshall
- Fácil de visualizar

**Formato:**
```python
{
    'A': {'A': 0, 'B': 15, 'C': 20, 'D': inf, ...},
    'B': {'A': inf, 'B': 0, 'C': 10, 'D': 25, ...},
    ...
}
```

## Solución de Problemas

### Error: "Nodo inválido"

**Problema:** Ingresaste un nodo que no existe.

**Solución:** Los nodos válidos son A, B, C, D, E, F, G. Usa la opción 4 del menú para ver la leyenda.

### Error: "No hay ruta disponible"

**Problema:** No existe un camino entre el origen y el destino.

**Solución:** El grafo es dirigido. Por ejemplo, hay ruta de A a B, pero no de B a A. Verifica la matriz de todos los pares (opción 3) para ver todas las conexiones.

### Error al importar módulos

**Problema:** Python no encuentra los módulos.

**Solución:** Asegúrate de estar en el directorio del proyecto:
```bash
cd /ruta/al/LogiExpress-startup
python main.py
```

## Contribuir

Si deseas agregar más ubicaciones o modificar las conexiones:

1. Edita `graph.py`
2. Modifica la función `create_bogota_graph()`
3. Actualiza los tests en `test_graph.py`
4. Ejecuta los tests para verificar: `python test_graph.py`

## Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio de GitHub.
