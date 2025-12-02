"""Configuración general del Memory Game"""

# Configuración de base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}

# Configuración de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colores
COLORS = {
    'background': (245, 245, 250),
    'card_back': (100, 150, 255),
    'card_front': (255, 255, 255),
    'text': (50, 50, 50),
    'text_light': (255, 255, 255),
    'primary': (100, 150, 255),
    'success': (80, 200, 120),
    'warning': (255, 180, 0),
    'shadow': (0, 0, 0, 30),
    'highlight': (255, 230, 100),
    'hover': (120, 170, 255)
}

# Configuración de niveles
LEVELS = {
    1: {'rows': 4, 'cols': 4, 'name': 'Nivel 1 - Fácil'},
    2: {'rows': 4, 'cols': 5, 'name': 'Nivel 2 - Medio'},
    3: {'rows': 6, 'cols': 6, 'name': 'Nivel 3 - Difícil'}
}

# Nombre del juego en la base de datos
GAME_NAME = "Memory Game"

# Animaciones
FLIP_SPEED = 15
MATCH_FLASH_DURATION = 500
CARD_REVEAL_DELAY = 1000

# HUD
HUD_HEIGHT = 80
HUD_MARGIN = 20

# Cartas
CARD_MARGIN = 10
CARD_BORDER_RADIUS = 15
CARD_SHADOW_OFFSET = 5