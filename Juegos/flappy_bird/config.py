"""Configuración general del juego"""

# Dimensiones de la ventana
ANCHO = 400
ALTO = 600

# Colores (R, G, B)
CIELO = (135, 206, 235)
SUELO = (222, 184, 135)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERDE_OSCURO = (0, 150, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)

# Configuración del juego
FPS = 60
GRAVEDAD = 0.5
FUERZA_SALTO = -10
VELOCIDAD_TUBOS = 3
ESPACIO_TUBOS = 200  # Espacio vertical entre tubo superior e inferior
DISTANCIA_TUBOS = 300  # Distancia horizontal entre tubos

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'games_db'
}