"""
Configuración para la integración con Google Maps API.
"""

# Coordenadas reales de las ubicaciones en Bogotá
BOGOTA_LOCATIONS = {
    'A': {
        'name': 'Aeropuerto El Dorado',
        'coordinates': (4.7016, -74.1469),
        'address': 'Av. El Dorado #103-9, Bogotá, Colombia'
    },
    'B': {
        'name': 'Terminal de Transporte',
        'coordinates': (4.6391, -74.1300),
        'address': 'Diagonal 23 #69-60, Bogotá, Colombia'
    },
    'C': {
        'name': 'Parque Simón Bolívar',
        'coordinates': (4.6553, -74.0907),
        'address': 'Calle 63 ##60-00, Bogotá, Colombia'
    },
    'D': {
        'name': 'Museo del Oro',
        'coordinates': (4.6016, -74.0726),
        'address': 'Calle 16 #5-41, Bogotá, Colombia'
    },
    'E': {
        'name': 'Monserrate',
        'coordinates': (4.6055, -74.0563),
        'address': 'Cerro de Monserrate, Bogotá, Colombia'
    },
    'F': {
        'name': 'Zona T (Zona Rosa)',
        'coordinates': (4.6698, -74.0542),
        'address': 'Carrera 13 con Calle 82, Bogotá, Colombia'
    },
    'G': {
        'name': 'Universidad EAN',
        'coordinates': (4.6392, -74.0642),
        'address': 'Calle 79 #11-45, Bogotá, Colombia'
    }
}

# Configuración de Google Maps API
GOOGLE_MAPS_CONFIG = {
    'API_KEY': 'TU_API_KEY_AQUI',  # Reemplazar con tu API key real
    'BASE_URL': 'https://maps.googleapis.com/maps/api',
    'LANGUAGE': 'es',
    'REGION': 'CO'
}

# Configuración de visualización
MAP_CONFIG = {
    'DEFAULT_ZOOM': 12,
    'CENTER_BOGOTA': (4.6097, -74.0817),
    'MAP_TYPE': 'roadmap'
}