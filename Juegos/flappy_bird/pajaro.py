# ==================== config.py ====================
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


# ==================== pajaro.py ====================
"""Clase que maneja la lógica del pájaro"""
import pygame
from config import *

class Pajaro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad_y = 0
        self.radio = 15
        self.angulo = 0
        self.vivo = True
    
    def saltar(self):
        """Hace que el pájaro salte"""
        if self.vivo:
            self.velocidad_y = FUERZA_SALTO
    
    def actualizar(self):
        """Actualiza la física del pájaro"""
        if not self.vivo:
            return
        
        # Aplicar gravedad
        self.velocidad_y += GRAVEDAD
        self.y += self.velocidad_y
        
        # Calcular ángulo basado en velocidad
        if self.velocidad_y < 0:
            self.angulo = min(30, -self.velocidad_y * 3)
        else:
            self.angulo = max(-90, -self.velocidad_y * 3)
        
        # Limitar movimiento vertical
        if self.y < 0:
            self.y = 0
            self.velocidad_y = 0
    
    def colisiona_con_suelo(self, altura_suelo):
        """Verifica si el pájaro toca el suelo"""
        return self.y + self.radio >= altura_suelo
    
    def colisiona_con_techo(self):
        """Verifica si el pájaro toca el techo"""
        return self.y - self.radio <= 0
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del pájaro"""
        return pygame.Rect(
            self.x - self.radio,
            self.y - self.radio,
            self.radio * 2,
            self.radio * 2
        )
    
    def morir(self):
        """Marca al pájaro como muerto"""
        self.vivo = False