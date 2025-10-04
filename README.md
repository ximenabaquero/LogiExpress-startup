# LogiExpress - Sistema de Rutas de Bogotá

Sistema de navegación y cálculo de rutas más cortas para ubicaciones clave en Bogotá, implementado en Python con algoritmos de grafos.

## Descripción

Este proyecto implementa un grafo de Bogotá con 7 ubicaciones clave y utiliza algoritmos de búsqueda de rutas más cortas para encontrar las mejores rutas entre cualquier par de ubicaciones.

### Ubicaciones

- **A**: Aeropuerto
- **B**: Terminal
- **C**: Simón Bolívar
- **D**: Museo del Oro
- **E**: Monserrate
- **F**: Zona T
- **G**: EAN

## Características

### Algoritmos Implementados

1. **Dijkstra (SSSP - Single Source Shortest Path)**
   - Encuentra la ruta más corta desde un origen a todos los demás nodos
   - Complejidad: O((V + E) log V)
   
2. **Floyd-Warshall (APSP - All Pairs Shortest Path)**
   - Calcula las rutas más cortas entre todos los pares de nodos
   - Complejidad: O(V³)

### Estructura de Datos

- **Lista de Adyacencia**: Representación eficiente para grafos dispersos
- **Matriz de Adyacencia**: Utilizada para Floyd-Warshall

## Estructura del Proyecto

```
LogiExpress-startup/
├── graph.py           # Estructura de datos del grafo
├── algorithms.py      # Implementación de Dijkstra y Floyd-Warshall
├── visualization.py   # Funciones de visualización y tablas
├── main.py           # Interfaz CLI
├── test_graph.py     # Tests unitarios
└── README.md         # Este archivo
```

## Instalación

### Instalación Básica

El proyecto básico utiliza solo la biblioteca estándar de Python:

```bash
# Clonar el repositorio
git clone https://github.com/ximenabaquero/LogiExpress-startup.git
cd LogiExpress-startup
```

### Instalación con Google Maps (Recomendada)

Para funcionalidades completas con integración de Google Maps:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar API key de Google Maps (opcional)
# Editar config.py y agregar tu API key
```

### Requisitos para Google Maps

1. **API Key de Google Cloud Platform**
   - Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
   - Habilita las APIs: Maps JavaScript API, Directions API, Distance Matrix API
   - Crea credenciales (API Key)

2. **Dependencias Python**
   - `requests>=2.28.0`
   - `urllib3>=1.26.0`

## Uso

### Interfaz CLI Básica

```bash
python main.py
```

### Interfaz CLI con Google Maps (Recomendada)

```bash
python main_google_maps.py
```

### Demostraciones

```bash
# Demo básico
python demo.py

# Demo con Google Maps
python demo_google_maps.py
```

El menú principal ofrece las siguientes opciones:

1. **Ruta más corta origen → destino**: Calcula y visualiza la ruta óptima entre dos ubicaciones
2. **Todas las rutas desde un origen**: Muestra todas las rutas posibles desde una ubicación
3. **Matriz de todos los pares de distancias**: Muestra la tabla completa de distancias usando Floyd-Warshall
4. **Ver ubicaciones**: Muestra la leyenda de ubicaciones
5. **Salir**: Termina la aplicación

### Ejemplo de Uso

```
SISTEMA DE RUTAS DE BOGOTÁ - LOGIEXPRESS
1. Ruta más corta origen → destino
2. Todas las rutas desde un origen
3. Matriz de todos los pares de distancias
4. Ver ubicaciones
5. Salir

Seleccione una opción (1-5): 1
Ingrese el nodo origen (A-G): A
Ingrese el nodo destino (A-G): D

Ruta: A → C → D
Distancia total: 32 minutos
```

## Tests

Ejecutar los tests:

```bash
python test_graph.py
```

### Tests Requeridos

El sistema verifica que:
- A → D = 32 minutos ✓
- B → E = 27 minutos ✓

### Cobertura de Tests

- Creación del grafo
- Algoritmo de Dijkstra
- Algoritmo de Floyd-Warshall
- Reconstrucción de rutas
- Matriz de adyacencia
- Consistencia entre algoritmos

## Visualización

El sistema proporciona:

1. **Visualización de Ruta**: Muestra la ruta completa con flechas
2. **Tabla de Segmentos**: Detalla cada segmento del viaje con:
   - Nodo de origen
   - Nodo de destino
   - Tiempo del segmento
   - Tiempo acumulado

Ejemplo:
```
TABLA DE SEGMENTOS
------------------------------------------------------------
Desde      Hacia      Tiempo          Acumulado      
------------------------------------------------------------
A          C          20              20             
C          D          12              32             
------------------------------------------------------------
```

## Implementación Técnica

### Módulo `graph.py`

Define la clase `Graph` con:
- Representación mediante lista de adyacencia
- Conversión a matriz de adyacencia
- Función `create_bogota_graph()` que inicializa el grafo con las ubicaciones y conexiones

### Módulo `algorithms.py`

Implementa:
- `dijkstra(graph, start)`: Algoritmo de Dijkstra
- `floyd_warshall(graph)`: Algoritmo de Floyd-Warshall
- `reconstruct_path()`: Reconstrucción de rutas
- `reconstruct_path_floyd_warshall()`: Reconstrucción con Floyd-Warshall

### Módulo `visualization.py`

Proporciona:
- `visualize_path()`: Visualización de rutas con tabla de segmentos
- `print_all_routes_from_source()`: Tabla de todas las rutas desde un origen
- `print_all_pairs_matrix()`: Matriz de distancias Floyd-Warshall
- `print_location_legend()`: Leyenda de ubicaciones

### Módulo `main.py`

Interfaz CLI que integra todos los módulos y proporciona un menú interactivo.

## Autor

Ximena Baquero - LogiExpress Startup

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
