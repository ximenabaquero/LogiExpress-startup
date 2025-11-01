# LogiExpress - Sistema de Rutas Inteligentes

Sistema avanzado de navegación y cálculo de rutas más cortas para ciudades, implementado en Python con algoritmos de grafos, integración con Google Maps API y una interfaz gráfica moderna.

## 📋 Descripción

**LogiExpress** es un sistema de ruteo que modela la red vial de **Bogotá** a partir de datos abiertos de **OpenStreetMap**, consumidos con **OSMnx**.
> **Nota:** aunque OSMnx incluye utilidades para calcular rutas directamente, en este proyecto **se usa OSMnx solo como base para construir un grafo realista de la ciudad**. El cómputo del camino óptimo se implementa **desde cero** con **Dijkstra**, con fines **académicos y didácticos** (POO, estructuras de datos, colas de prioridad, etc.).

El sistema soporta dos modos de optimización:
- **Distancia**: minimiza la longitud total (metros) usando la longitud de las aristas del grafo.
- **Duración**: minimiza el tiempo estimado (segundos). Para estimar pesos temporales entre pares de nodos se integra la **Google Maps API** (tráfico/heurísticas), por lo que requiere **API key** válida.

**Resumen de diseño**
- **OSMnx** → descarga y construcción del **grafo dirigido** de la red vial (nodos = intersecciones, aristas = tramos).
- **Pesos** → distancia (nativa de OSMnx) o duración (calculada vía Google).
- **Algoritmo** → **Dijkstra** propio sobre el grafo simplificado, para reforzar conceptos de teoría de grafos y análisis de algoritmos.


## 🚀 Características Principales

- **Descarga de grafos urbanos** mediante OSMnx con sistema de caché
- **Algoritmo de Dijkstra** para cálculo de rutas más cortas
- **Integración con Google Maps API** para geocodificación y cálculo de duración de rutas
- **Visualización interactiva** de rutas con mapas HTML interactivos
- **Interfaz gráfica moderna** con Tkinter
- **Gestión segura de API keys** con cifrado usando Fernet (cryptography)

## 📦 Instalación

### Requisitos

- Python 3.8 o superior
- Google Maps API Key (opcional, solo para modo "duration")

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/ximenabaquero/LogiExpress-startup.git
cd LogiExpress-startup
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar API Key de Google Maps** (opcional):
   - Obtén una API Key de Google Maps con permisos para:
     - Geocoding API
     - Routes API
   - Ejecuta el módulo de seguridad para cifrar y guardar tu API key:
```bash
python -m src.security.encrypted_env
```

## 🏗️ Estructura del Proyecto

```
LogiExpress-startup/
├── src/
│   ├── __init__.py
│   ├── algorithms/           # Algoritmos de routing
│   │   ├── __init__.py
│   │   └── dijkstra.py      # Implementación del algoritmo de Dijkstra
│   ├── api/                  # Integración con APIs externas
│   │   ├── __init__.py
│   │   └── google_maps.py   # Cliente para Google Maps API
│   ├── graph/                # Gestión de grafos
│   │   ├── __init__.py
│   │   ├── builder.py       # Construcción de grafos simplificados
│   │   ├── downloader.py    # Descarga y caché de grafos OSMnx
│   │   └── visualizer.py    # Visualización de rutas en mapas
│   ├── routing/              # Cálculo de rutas
│   │   ├── __init__.py
│   │   └── compute_routes_async.py  # Cálculo asíncrono de rutas
│   ├── security/             # Seguridad y gestión de secretos
│   │   ├── __init__.py
│   │   └── encrypted_env.py  # Cifrado y descifrado de API keys
│   └── ui/                   # Interfaz de usuario
│       └── app.py            # Aplicación GUI con Tkinter
├── data/
│   └── cache/                # Caché de grafos descargados
├── requirements.txt
└── README.md
```

## 📚 Documentación de Módulos

### 🔧 `src/algorithms/dijkstra.py`

Implementación del algoritmo de Dijkstra para encontrar la ruta más corta en un grafo.

**Funciones principales:**

#### `dijkstra(graph, source, target, weight_type="distance")`

Encuentra la ruta más corta desde un nodo origen hasta un nodo destino.

**Parámetros:**
- `graph` (dict): Lista de adyacencia del grafo en formato `{node: [(neighbor, weight), ...]}`
- `source` (int): ID del nodo de origen
- `target` (int): ID del nodo de destino
- `weight_type` (str): Tipo de peso a usar ("distance" o "time"), usado solo para logging

**Retorna:**
- `tuple`: Tupla `(path, total_cost)` donde:
  - `path`: Lista de IDs de nodos que forman la ruta
  - `total_cost`: Costo total de la ruta (metros si es distancia, segundos si es tiempo)

**Complejidad:** O((V + E) log V) donde V es el número de vértices y E el número de aristas.

**Ejemplo:**
```python
from src.algorithms.dijkstra import dijkstra

graph = {
    1: [(2, 10), (3, 5)],
    2: [(4, 8)],
    3: [(4, 12)],
    4: []
}
path, cost = dijkstra(graph, source=1, target=4, weight_type="distance")
# path = [1, 3, 4], cost = 17
```

---

### 🌐 `src/api/google_maps.py`

Cliente para interactuar con Google Maps API, incluyendo geocodificación y cálculo de duración de rutas.

**Funciones principales:**

#### `google_key_sanity_check(google_api_key: str) -> bool`

Valida una API key de Google realizando una llamada de prueba a la API de Geocoding.

**Parámetros:**
- `google_api_key` (str): La API key a validar

**Retorna:**
- `bool`: `True` si la API key es válida, `False` en caso contrario

**Ejemplo:**
```python
from src.api.google_maps import google_key_sanity_check

is_valid = google_key_sanity_check("YOUR_API_KEY")
```

#### `compute_route_duration_seconds(...)`

Calcula la duración y distancia de una ruta entre dos puntos usando Google Routes API.

**Parámetros:**
- `google_maps_api_url` (str): URL del endpoint de Routes API
- `google_api_key` (str): API key de Google
- `origin_lat` (float): Latitud del origen
- `origin_lng` (float): Longitud del origen
- `dest_lat` (float): Latitud del destino
- `dest_lng` (float): Longitud del destino
- `routing_preference` (str): Preferencia de routing (default: "TRAFFIC_AWARE")
- `departure_time` (str, optional): Tiempo de salida para predicción de tráfico
- `traffic_model` (str, optional): Modelo de tráfico a usar

**Retorna:**
- `tuple`: `(dur_seconds, distance_m, data)` donde:
  - `dur_seconds`: Duración en segundos (None si no hay ruta)
  - `distance_m`: Distancia en metros (None si no hay ruta)
  - `data`: Respuesta completa de la API

#### `get_coordinates_from_address(...)`

Geocodifica una dirección y retorna sus coordenadas geográficas.

**Parámetros:**
- `google_api_key` (str): API key de Google
- `address` (str): Dirección a geocodificar
- `city_hint` (str, optional): Pista de ciudad para mejorar la precisión (default: "Bogotá, Colombia")
- `bounds` (tuple, optional): Límites geográficos `((sw_lat, sw_lng), (ne_lat, ne_lng))`
- `region` (str): Código de región (default: "co")
- `language` (str): Código de idioma (default: "es")

**Retorna:**
- `tuple`: `(lat, lng)` en float, o `(None, None)` si no se encontraron resultados

**Ejemplo:**
```python
from src.api.google_maps import get_coordinates_from_address

lat, lng = get_coordinates_from_address(
    google_api_key="YOUR_KEY",
    address="Diagonal 81F # 72C-1, Bogotá, Colombia",
    city_hint="Bogotá, Colombia"
)
```

---

### 📊 `src/graph/builder.py`

Construye grafos simplificados a partir de grafos OSMnx para uso con algoritmos de routing. Incluye muestreo determinista, caché de duraciones, reintentos con backoff exponencial, y soporte para calles bidireccionales.

**Funciones principales:**

#### `build_simple_graph(google_maps_api_url, google_api_key, G, weight_type="distance", sample_ratio=0.001, default_speed_kph=25.0, max_retries=3, backoff_base=0.5)`

Convierte un grafo OSMnx (MultiDiGraph) en un grafo simplificado con lista de adyacencia.

**Parámetros:**
- `google_maps_api_url` (str): URL de la API de Google Maps Routes (endpoint Directions v2 computeRoutes)
- `google_api_key` (str): API key de Google (requerida si `weight_type="duration"`)
- `G`: Grafo de OSMnx (networkx.MultiDiGraph dirigido)
- `weight_type` (str): Tipo de peso a usar: `"distance"` (metros) o `"duration"` (segundos)
- `sample_ratio` (float): Fracción de aristas a consultar a Google (determinista por hash MD5, default: 0.001 = 0.1%)
- `default_speed_kph` (float): Velocidad por defecto para estimar duración cuando no hay API/resultado (default: 25.0 km/h)
- `max_retries` (int): Número máximo de reintentos por arista para la consulta a Google (default: 3)
- `backoff_base` (float): Factor base para backoff exponencial en reintentos (default: 0.5 segundos)

**Retorna:**
- `dict`: Grafo simplificado en formato `{node: [(neighbor, weight), ...]}` con pesos coherentes al modo escogido

**Características:**

1. **Muestreo Determinista**: Usa hash MD5 del par (u,v) para decidir qué aristas consultar, garantizando resultados reproducibles entre ejecuciones.

2. **Caché de Duraciones**: Almacena resultados de API en memoria para evitar llamadas duplicadas para las mismas coordenadas (con redondeo de coordenadas para mejorar hit rate).

3. **Reintentos con Backoff Exponencial**: Si una llamada a la API falla, reintenta automáticamente con espera exponencial (0.5s, 1s, 2s, ...).

4. **Estimación Inteligente de Duración**: 
   - Si se consulta la API y obtiene resultado → usa duración real
   - Si se consulta pero falla → estima usando `distancia / velocidad_default`
   - Si no se consulta (no muestreada) → estima usando `distancia / velocidad_default`

5. **Soporte Bidireccional**: Detecta automáticamente si una calle es unidireccional (`oneway`) y agrega la arista inversa cuando corresponde.

**Funciones auxiliares:**

##### `_deterministic_sample(u, v, ratio) -> bool`

Muestreo determinista basado en hash MD5 para reproducibilidad.

##### `_call_duration_with_backoff(...) -> Optional[float]`

Llama a Google Routes API con reintentos y backoff exponencial. Devuelve duración en segundos o None.

##### `_is_oneway(edge_data) -> bool`

Determina si una arista es unidireccional según atributos de OSM (soporta múltiples formatos: True, 'true', 'yes', 1).

**Ejemplo:**
```python
from src.graph.builder import build_simple_graph

# Con distancia (no requiere API key)
graph_simple = build_simple_graph(
    google_maps_api_url="https://routes.googleapis.com/directions/v2:computeRoutes",
    google_api_key="",
    G=G_osmnx,
    weight_type="distance"
)

# Con duración (requiere API key válida)
graph_simple = build_simple_graph(
    google_maps_api_url="https://routes.googleapis.com/directions/v2:computeRoutes",
    google_api_key="YOUR_KEY",
    G=G_osmnx,
    weight_type="duration",
    sample_ratio=0.001,        # 0.1% de aristas consultadas determinísticamente
    default_speed_kph=30.0,    # 30 km/h para estimaciones
    max_retries=3,             # 3 reintentos por fallo
    backoff_base=0.5          # Backoff: 0.5s, 1s, 2s
)
```

**Notas importantes:**
- El muestreo determinista garantiza que las mismas aristas se consulten en ejecuciones repetidas (útil para debugging y reproducibilidad).
- Todas las aristas tienen pesos coherentes: todas en metros (distance) o todas en segundos (duration), eliminando mezcla de unidades.
- La velocidad por defecto (25 km/h) es una estimación conservadora para áreas urbanas; ajusta según tu contexto.

---

### 📥 `src/graph/downloader.py`

Descarga y gestiona el caché de grafos urbanos desde OpenStreetMap usando OSMnx.

**Funciones principales:**

#### `download_city_graph(place, network_type="drive", use_cache=True, max_age_days=30)`

Descarga o carga desde caché el grafo vial de una ciudad.

**Parámetros:**
- `place` (str): Nombre de la ciudad o región (ej: "Bogotá, Colombia")
- `network_type` (str): Tipo de red ("drive", "walk", "bike", etc., default: "drive")
- `use_cache` (bool): Si es `True`, reutiliza el grafo en caché si existe (default: True)
- `max_age_days` (int): Días máximos de antigüedad del caché antes de descargar uno nuevo (default: 30)

**Retorna:**
- `networkx.MultiDiGraph`: Grafo vial de la ciudad con nodos y aristas

**Comportamiento:**
1. Si existe un grafo en caché y es reciente (≤ `max_age_days`), lo carga desde el disco
2. Si no existe o está desactualizado, descarga un nuevo grafo desde OpenStreetMap
3. Guarda el grafo descargado en `data/cache/{place}_{network_type}.graphml`

**Ejemplo:**
```python
from src.graph.downloader import download_city_graph

# Descargar grafo de Bogotá para vehículos
G = download_city_graph(
    place="Bogotá, Colombia",
    network_type="drive",
    use_cache=True,
    max_age_days=30
)

print(f"Nodos: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")
```

---

### 🗺️ `src/graph/visualizer.py`

Genera visualizaciones interactivas de rutas en mapas HTML usando GeoPandas.

**Funciones principales:**

#### `plot_route_explore_compliant(G, route_nodes, save_path="data/outputs/route_map.html", show_network=False, network_padding_deg=0.01)`

Genera un mapa HTML interactivo de una ruta calculada.

**Parámetros:**
- `G`: Grafo de OSMnx (networkx.MultiDiGraph)
- `route_nodes` (list): Lista de IDs de nodos que forman la ruta
- `save_path` (str): Ruta donde guardar el archivo HTML (default: "data/outputs/route_map.html")
- `show_network` (bool): Si es `True`, muestra la red de calles alrededor de la ruta (default: False)
- `network_padding_deg` (float): Grados de padding alrededor de la ruta para mostrar la red (default: 0.01)

**Retorna:**
- `str`: Ruta del archivo HTML guardado

**Características del mapa generado:**
- Mapa base con tiles de CartoDB Positron
- Ruta resaltada en rojo
- Marcador verde en el origen
- Marcador negro en el destino
- Marcadores rojos en nodos intermedios (si los hay)
- Zoom automático para encuadrar toda la ruta
- Capa opcional de red de calles

**Ejemplo:**
```python
from src.graph.visualizer import plot_route_explore_compliant

html_path = plot_route_explore_compliant(
    G=G,
    route_nodes=[123, 456, 789, 101112],
    save_path="data/outputs/mi_ruta.html",
    show_network=True
)
```

---

### 🛣️ `src/routing/compute_routes_async.py`

Calcula rutas de forma asíncrona, integrando geocodificación, búsqueda de nodos más cercanos y ejecución de Dijkstra.

**Funciones principales:**

#### `compute_route_async(...) -> RouteResult`

Función asíncrona que calcula la ruta completa desde una dirección de origen hasta una de destino.

**Parámetros:**
- `G`: Grafo de OSMnx (networkx.MultiDiGraph)
- `graph_simple` (dict): Grafo simplificado en formato lista de adyacencia
- `dijkstra_fn` (Callable): Función de Dijkstra a usar
- `get_coordinates_from_address` (Callable): Función de geocodificación
- `origin_text` (str): Dirección de origen
- `dest_text` (str): Dirección de destino
- `google_api_key` (str): API key de Google (requerida para geocodificación)
- `weight_type` (str): Tipo de peso: "distance" o "duration" (default: "distance")
- `timeout_seconds` (int): Timeout máximo para la operación (default: 25)

**Retorna:**
- `RouteResult`: Objeto dataclass con:
  - `path_nodes`: Lista de IDs de nodos de la ruta
  - `total_cost`: Costo total (metros o segundos según `weight_type`)
  - `weight_type`: Tipo de peso usado
  - `origin_node`: ID del nodo de origen en el grafo
  - `dest_node`: ID del nodo de destino en el grafo
  - `origin_lat`, `origin_lng`: Coordenadas del origen
  - `dest_lat`, `dest_lng`: Coordenadas del destino

**Flujo de ejecución:**
1. Obtiene los límites geográficos del grafo para sesgar la geocodificación
2. Geocodifica las direcciones de origen y destino usando Google Maps API
3. Encuentra los nodos más cercanos en el grafo usando `ox.distance.nearest_nodes`
4. Ejecuta Dijkstra para encontrar la ruta más corta
5. Retorna un objeto `RouteResult` con toda la información

**Ejemplo:**
```python
import asyncio
from src.routing.compute_routes_async import compute_route_async
from src.algorithms.dijkstra import dijkstra
from src.api.google_maps import get_coordinates_from_address

result = asyncio.run(compute_route_async(
    G=G,
    graph_simple=graph_simple,
    dijkstra_fn=dijkstra,
    get_coordinates_from_address=get_coordinates_from_address,
    origin_text="Diagonal 81F # 72C-1, Bogotá, Colombia",
    dest_text="Diagonal 57C Sur # 62-60, Bogotá, Colombia",
    google_api_key="YOUR_KEY",
    weight_type="distance",
    timeout_seconds=30
))

print(f"Ruta: {len(result.path_nodes)} nodos")
print(f"Costo total: {result.total_cost:.2f} metros")
```

**Clase `RouteResult`:**

```python
@dataclass
class RouteResult:
    path_nodes: list[int]
    total_cost: float
    weight_type: str  # "distance" | "duration"
    origin_node: int
    dest_node: int
    origin_lat: float
    origin_lng: float
    dest_lat: float
    dest_lng: float
```

---

### 🔒 `src/security/encrypted_env.py`

Gestiona el almacenamiento seguro de secretos (API keys) usando cifrado simétrico con Fernet.

**Funciones principales:**

#### `generate_key()`

Genera una llave de cifrado Fernet y la guarda en `encryption.key` si no existe.

**Comportamiento:**
- Lee la llave existente si ya existe
- Genera una nueva llave si no existe
- Guarda la llave en el directorio base del proyecto

#### `encrypt_secret()`

Solicita un secreto (API key) al usuario y lo guarda cifrado en `.env.enc`.

**Flujo:**
1. Genera o carga la llave de cifrado
2. Solicita el secreto al usuario (oculto con `getpass`)
3. Cifra el secreto usando Fernet
4. Guarda el secreto cifrado en `.env.enc`

#### `load_secret() -> str`

Descifra y retorna el secreto guardado en `.env.enc`.

**Comportamiento:**
1. Verifica si existen los archivos `encryption.key` y `.env.enc`
2. Si no existen, solicita crear uno nuevo llamando a `encrypt_secret()`
3. Descifra el secreto usando la llave
4. Si el descifrado falla (llave incorrecta), solicita crear uno nuevo
5. Retorna el secreto descifrado

**Ejemplo de uso:**

```python
from src.security.encrypted_env import load_secret, encrypt_secret

# Para cifrar y guardar un secreto (solo una vez)
encrypt_secret()

# Para cargar el secreto en tu aplicación
api_key = load_secret()
```

**Archivos generados:**
- `encryption.key`: Llave de cifrado (NO debe compartirse)
- `.env.enc`: Secreto cifrado (puede versionarse con cuidado)

**⚠️ Importante:**
- No compartas `encryption.key` en repositorios públicos
- Añade `encryption.key` a `.gitignore`
- El archivo `.env.enc` puede versionarse si se desea, pero es inútil sin la llave

---

### 🖥️ `src/ui/app.py`

Aplicación de interfaz gráfica construida con Tkinter que integra todos los módulos del sistema.

**Clase principal:**

#### `RouteGUI`

Interfaz gráfica para construir grafos, calcular rutas y visualizarlas.

**Métodos principales:**

##### `__init__(root: tk.Tk)`

Inicializa la aplicación y crea la interfaz.

**Componentes de la UI:**
- Campo de ciudad/lugar (`place_var`)
- Selector de modo de peso (`weight_mode_var`: "distance" | "duration")
- Botón "Load API Key" para cargar la API key de Google
- Botón "Build/Load Graph" para descargar/cargar el grafo
- Campos de dirección de origen y destino
- Botón "Compute Route (Dijkstra)" para calcular la ruta
- Botón "Open Map" para abrir el mapa HTML en el navegador
- Botón "Save As..." para guardar el mapa en otra ubicación
- Consola de log para mostrar información de operaciones

##### `_load_key()`

Carga y valida la API key de Google usando el módulo de seguridad.

##### `on_build_graph()` / `_build_graph_async()`

Descarga o carga el grafo de la ciudad especificada y construye el grafo simplificado.

**Flujo:**
1. Descarga/carga el grafo usando `download_city_graph()`
2. Construye el grafo simplificado usando `build_simple_graph()`
3. Actualiza el estado de la UI

##### `on_compute_route()` / `_compute_route_async()`

Calcula la ruta entre origen y destino y genera la visualización.

**Flujo:**
1. Valida que el grafo esté construido
2. Valida que haya API key si el modo es "duration"
3. Ejecuta `compute_route_async()` para calcular la ruta
4. Genera el mapa HTML usando `plot_route_explore_compliant()`
5. Muestra información en la consola

##### `on_open_map()`

Abre el archivo HTML del mapa en el navegador predeterminado.

##### `on_save_as()`

Guarda una copia del mapa HTML en una ubicación seleccionada por el usuario.

**Función principal:**

#### `run_app()`

Inicializa y ejecuta la aplicación GUI.

**Ejemplo de uso:**

```python
from src.ui.app import run_app

if __name__ == "__main__":
    run_app()
```

**Ejecución desde línea de comandos:**
```bash
python -m src.ui.app
```

---

## 🎮 Uso de la Aplicación

### Modo GUI (Recomendado)

1. **Iniciar la aplicación**:
```bash
python -m src.ui.app
```

2. **Configurar API Key** (si planeas usar modo "duration"):
   - Haz clic en "Load API Key"
   - Si es la primera vez, se te pedirá ingresar tu API key
   - El sistema validará la API key automáticamente

3. **Construir el grafo**:
   - Ingresa el nombre de la ciudad (ej: "Bogotá, Colombia")
   - Selecciona el modo de peso: "distance" o "duration"
   - Haz clic en "Build/Load Graph"
   - Espera a que se descargue/cargue el grafo (puede tardar unos minutos la primera vez)

4. **Calcular una ruta**:
   - Ingresa la dirección de origen
   - Ingresa la dirección de destino
   - Haz clic en "Compute Route (Dijkstra)"
   - El sistema calculará la ruta y generará un mapa HTML

5. **Visualizar el resultado**:
   - Haz clic en "Open Map" para ver el mapa en tu navegador
   - O haz clic en "Save As..." para guardar el mapa en otra ubicación

### Modo Programático

```python
import asyncio
from src.graph.downloader import download_city_graph
from src.graph.builder import build_simple_graph
from src.routing.compute_routes_async import compute_route_async
from src.algorithms.dijkstra import dijkstra
from src.api.google_maps import get_coordinates_from_address
from src.security.encrypted_env import load_secret

# 1. Cargar API key
api_key = load_secret()

# 2. Descargar/cargar grafo
G = download_city_graph("Bogotá, Colombia", network_type="drive", use_cache=True)

# 3. Construir grafo simplificado
graph_simple = build_simple_graph(
    google_maps_api_url="https://routes.googleapis.com/directions/v2:computeRoutes",
    google_api_key=api_key,
    G=G,
    weight_type="distance"
)

# 4. Calcular ruta
result = asyncio.run(compute_route_async(
    G=G,
    graph_simple=graph_simple,
    dijkstra_fn=dijkstra,
    get_coordinates_from_address=get_coordinates_from_address,
    origin_text="Diagonal 81F # 72C-1, Bogotá, Colombia",
    dest_text="Diagonal 57C Sur # 62-60, Bogotá, Colombia",
    google_api_key=api_key,
    weight_type="distance",
    timeout_seconds=30
))

print(f"Ruta calculada: {len(result.path_nodes)} nodos")
print(f"Costo total: {result.total_cost:.2f} metros")
```

## 🔧 Configuración

### Variables de Entorno

El proyecto utiliza cifrado para almacenar la API key. Para configurarla:

```bash
python -m src.security.encrypted_env
```

Esto te pedirá ingresar tu API key de Google Maps y la guardará cifrada.

### Requisitos de la API Key de Google Maps

La API key debe tener habilitados los siguientes servicios:
- **Geocoding API**: Para convertir direcciones en coordenadas
- **Routes API (v2)**: Para calcular duraciones de rutas (solo si usas modo "duration")

**Limitaciones importantes:**
- El modo "duration" requiere hacer llamadas a la API por cada arista (limitado por `sample_ratio` determinista)
- El modo "distance" NO requiere API key

## 📝 Notas de Implementación

### Sistema de Caché

Los grafos descargados se guardan en `data/cache/` con el formato:
```
{city_name}_{network_type}.graphml
```

Los grafos se recargan automáticamente si tienen más de 30 días de antigüedad (configurable).

### Optimización para Duración

Para evitar costos excesivos de API, el modo "duration" utiliza:

1. **Muestreo Determinista**: Solo consulta un porcentaje pequeño de aristas (configurable con `sample_ratio`, default 0.1%). El muestreo es determinista usando hash MD5, garantizando que las mismas aristas se consulten en ejecuciones repetidas.

2. **Estimación por Velocidad**: Las aristas no muestreadas o sin respuesta de API estiman su duración usando `distancia / velocidad_default` (default: 25 km/h). Esto asegura que todos los pesos estén en la misma unidad (segundos).

3. **Caché de Duraciones**: Los resultados de API se almacenan en memoria para evitar llamadas duplicadas.

4. **Reintentos Automáticos**: Si una llamada falla, se reintenta automáticamente con backoff exponencial.

**Ventajas del nuevo sistema:**
- ✅ Pesos coherentes: todas las aristas en segundos (no mezcla metros/segundos)
- ✅ Resultados reproducibles (muestreo determinista)
- ✅ Mejor uso de la API (caché y reintentos)
- ✅ Estimaciones más realistas (velocidad vs distancia pura)

### Compatibilidad de Versiones

El código es compatible con diferentes versiones de OSMnx y maneja cambios en la API usando verificaciones de tipo y fallbacks.

## 🐛 Solución de Problemas

### Error: "API key no cargada"
- Ejecuta `python -m src.security.encrypted_env` para configurar la API key
- Asegúrate de que los servicios necesarios estén habilitados en Google Cloud Console

### Error: "No se pudo geocodificar"
- Verifica que la dirección sea válida
- Asegúrate de incluir la ciudad en la dirección
- Revisa que la API key tenga permisos para Geocoding API

### El mapa no se genera
- Verifica que exista el directorio `data/outputs/`
- Revisa los logs en la consola de la aplicación para ver errores específicos

### El grafo tarda mucho en descargarse
- La primera descarga puede tardar varios minutos según el tamaño de la ciudad
- Los grafos se guardan en caché, las siguientes cargas serán instantáneas
- Considera usar `use_cache=True` para reutilizar grafos descargados previamente

## 👥 Autores

LogiExpress Startup - Ximena Baquero y Jhonners Penuela

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o contacta al equipo de desarrollo.
