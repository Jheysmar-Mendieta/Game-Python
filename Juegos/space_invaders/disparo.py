"""Clase que maneja la lógica de los disparos"""
import pygame
from config import *

class Disparo:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.ancho = DISPARO_ANCHO
        self.alto = DISPARO_ALTO
        self.velocidad = DISPARO_VELOCIDAD * direccion  # 1 = arriba, -1 = abajo
        self.activo = True
    
    def actualizar(self):
        """Actualiza la posición del disparo"""
        self.y -= self.velocidad
        
        # Desactivar si sale de la pantalla
        if self.y < 0 or self.y > ALTO:
            self.activo = False
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)