"""Configuración general del juego"""

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Colores (R, G, B)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 200, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 100, 255)
GRIS_OSCURO = (20, 20, 20)
AMARILLO = (255, 255, 0)
MORADO = (150, 0, 255)
CYAN = (0, 255, 255)
ROSA = (255, 0, 150)
NARANJA = (255, 165, 0)

# Configuración del juego
TAM = 20  # Tamaño de cada bloque
FPS = 12  # Velocidad del juego

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}

# Modos de juego
MODOS_JUEGO = {
    'clasico': {
        'nombre': 'Clásico',
        'descripcion': 'El Snake tradicional',
        'color': VERDE,
        'icono': '🍎'
    },
    'velocidad': {
        'nombre': 'Velocidad',
        'descripcion': 'Aumenta velocidad con cada manzana',
        'color': AMARILLO,
        'icono': '⚡'
    },
    'portal': {
        'nombre': 'Portal',
        'descripcion': 'Atraviesa los bordes',
        'color': CYAN,
        'icono': '🌀'
    },
    'laberinto': {
        'nombre': 'Laberinto',
        'descripcion': 'Evita los obstáculos',
        'color': MORADO,
        'icono': '📦'
    },
    'veneno': {
        'nombre': 'Veneno',
        'descripcion': 'Evita manzanas rojas',
        'color': ROSA,
        'icono': '☠️'
    },
    'tiempo': {
        'nombre': 'Contra Reloj',
        'descripcion': '60 segundos máximo',
        'color': NARANJA,
        'icono': '⏱️'
    }
}