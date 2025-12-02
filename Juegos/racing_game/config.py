"""Configuración general del juego de carreras"""

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
TILE_SIZE = 32

# Colores
COLORS = {
    'background': (40, 40, 40),
    'grass': (50, 120, 50),
    'track': (80, 80, 80),
    'border': (200, 50, 50),
    'checkpoint': (255, 255, 100, 100),
    'text': (255, 255, 255),
    'hud_bg': (0, 0, 0, 180),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 50, 50),
    'green': (50, 255, 50),
    'blue': (50, 150, 255),
    'yellow': (255, 255, 50),
    'orange': (255, 150, 50)
}

# Física del vehículo
CAR_ACCELERATION = 0.3
CAR_DECELERATION = 0.15
CAR_FRICTION = 0.05
CAR_MAX_SPEED = 12.0
CAR_MIN_SPEED = -6.0
CAR_TURN_SPEED = 4.0
CAR_DRIFT_FACTOR = 0.92

# Penalizaciones
OFFTRACK_FRICTION = 0.3
COLLISION_SPEED_REDUCTION = 0.5

# Configuración de carrera
MAX_LAPS = 3
CHECKPOINT_THRESHOLD = 50

# IA
AI_BASE_SPEED = 8.0
AI_AGGRESSION = 0.7  # 0.0 = conservadora, 1.0 = agresiva
AI_REACTION_TIME = 0.1

# Partículas
PARTICLE_LIFETIME = 1.0
SMOKE_SPEED_THRESHOLD = 8.0

# Cámara
CAMERA_SMOOTHNESS = 0.1

# Nombre del juego en BD
GAME_NAME = "Racing Game"

# Pistas disponibles
TRACKS = {
    'track1': {
        'name': 'Circuito Speedway',
        'laps': 3,
        'difficulty': 'Fácil',
        'description': 'Pista oval con curvas suaves'
    },
    'track2': {
        'name': 'Circuito Serpiente',
        'laps': 3,
        'difficulty': 'Medio',
        'description': 'Pista con chicanas y curvas cerradas'
    },
    'track3': {
        'name': 'Circuito Infierno',
        'laps': 3,
        'difficulty': 'Difícil',
        'description': 'Pista técnica con secciones complicadas'
    }
}

# Colores de coches
CAR_COLORS = [
    (255, 50, 50),    # Rojo
    (50, 150, 255),   # Azul
    (50, 255, 50),    # Verde
    (255, 255, 50),   # Amarillo
    (255, 150, 50),   # Naranja
    (200, 50, 200),   # Magenta
]