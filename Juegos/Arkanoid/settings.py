"""Configuración general del juego Arkanoid"""

# Configuración de ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colores
COLOR_BG = (20, 20, 30)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (220, 50, 50)
COLOR_GREEN = (50, 220, 50)
COLOR_BLUE = (50, 50, 220)
COLOR_YELLOW = (220, 220, 50)
COLOR_PURPLE = (180, 50, 180)
COLOR_ORANGE = (255, 140, 0)
COLOR_CYAN = (50, 220, 220)

# Colores de ladrillos por nivel
BRICK_COLORS = {
    1: (255, 100, 100),   # Rojo claro
    2: (255, 180, 100),   # Naranja
    3: (255, 255, 100),   # Amarillo
    4: (100, 255, 100),   # Verde
    5: (100, 180, 255),   # Azul
}

# Configuración de la pala
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
PADDLE_Y = WINDOW_HEIGHT - 50
PADDLE_COLOR = (100, 200, 255)

# Configuración de la pelota
BALL_RADIUS = 8
BALL_SPEED_INITIAL = 6
BALL_SPEED_INCREMENT = 0.1
BALL_MAX_SPEED = 12
BALL_COLOR = (255, 255, 255)

# Configuración de ladrillos
BRICK_WIDTH = 60
BRICK_HEIGHT = 25
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 80
BRICK_OFFSET_LEFT = 35

# Tipos de ladrillos
BRICK_NORMAL = 1      # 1 golpe
BRICK_RESISTANT = 2   # 2 golpes
BRICK_STRONG = 3      # 3 golpes
BRICK_INDESTRUCTIBLE = 9  # No se puede destruir

# Puntos por tipo de ladrillo
BRICK_POINTS = {
    BRICK_NORMAL: 10,
    BRICK_RESISTANT: 20,
    BRICK_STRONG: 30,
    BRICK_INDESTRUCTIBLE: 0
}

# Power-ups
POWERUP_SIZE = 30
POWERUP_FALL_SPEED = 3
POWERUP_PROBABILITY = 0.15  # 15% de probabilidad

# Tipos de power-ups
POWERUP_EXPAND = 'expand'        # Agrandar pala
POWERUP_SHRINK = 'shrink'        # Reducir pala
POWERUP_MULTIBALL = 'multiball'  # Pelota extra
POWERUP_SLOW = 'slow'            # Ralentizar pelota
POWERUP_FAST = 'fast'            # Acelerar pelota
POWERUP_PIERCE = 'pierce'        # Bola perforante
POWERUP_LIFE = 'life'            # Vida extra

POWERUP_DURATION = 10  # segundos

# Sistema de vidas
INITIAL_LIVES = 3

# Puntos extra
BONUS_PERFECT_LEVEL = 500
BONUS_POWERUP = 50

# Configuración de partículas
PARTICLE_COUNT = 8
PARTICLE_LIFETIME = 0.5

# Fuentes
FONT_NAME = None
FONT_SIZE = 24
FONT_TITLE = 48

# Base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}

GAME_NAME = 'Arkanoid'

# Volumen (0.0 a 1.0)
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7