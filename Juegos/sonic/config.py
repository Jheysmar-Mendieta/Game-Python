"""Configuración general del juego"""

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Colores (R, G, B)
CIELO_AZUL = (135, 206, 250)
VERDE_PASTO = (34, 139, 34)
MARRON = (139, 69, 19)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_SONIC = (0, 100, 200)
AZUL_OSCURO = (0, 50, 120)
AMARILLO = (255, 215, 0)
ROJO = (255, 0, 0)
GRIS = (128, 128, 128)
CYAN = (0, 255, 255)

# Configuración del juego
FPS = 60

# Física del jugador
GRAVEDAD = 0.8
VELOCIDAD_MAXIMA = 8
ACELERACION = 0.5
FRICCION = 0.9
FUERZA_SALTO = -16  # Aumentado para salto más potente

# Configuración de Sonic
SONIC_ANCHO = 40
SONIC_ALTO = 40

# Configuración de anillos
ANILLO_RADIO = 10
ANILLOS_POR_NIVEL = 20

# Configuración de enemigos
ENEMIGO_ANCHO = 30
ENEMIGO_ALTO = 30
ENEMIGOS_POR_NIVEL = 5

# Scroll de cámara
SCROLL_MARGEN = 300  # Margen para empezar a hacer scroll

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}