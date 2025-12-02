"""Configuración general del juego"""

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Colores (R, G, B)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 150, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 100, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Configuración del juego
FPS = 60

# Configuración del jugador
JUGADOR_VELOCIDAD = 5
JUGADOR_ANCHO = 50
JUGADOR_ALTO = 40

# Configuración de aliens
ALIEN_ANCHO = 40
ALIEN_ALTO = 30
ALIEN_FILAS = 5
ALIEN_COLUMNAS = 11
ALIEN_ESPACIADO_X = 60
ALIEN_ESPACIADO_Y = 50
ALIEN_VELOCIDAD_INICIAL = 1
ALIEN_VELOCIDAD_BAJADA = 30

# Configuración de disparos
DISPARO_VELOCIDAD = 7
DISPARO_ANCHO = 4
DISPARO_ALTO = 15
DISPARO_COOLDOWN = 500  # milisegundos

# Configuración de barreras
BARRERA_ANCHO = 80
BARRERA_ALTO = 60
BARRERA_VIDA = 5

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}