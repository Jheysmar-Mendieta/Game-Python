"""Clase que maneja la lógica de las barreras protectoras"""
import pygame
from config import *

class Barrera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = BARRERA_ANCHO
        self.alto = BARRERA_ALTO
        self.vida = BARRERA_VIDA
        self.viva = True
    
    def recibir_danio(self):
        """Recibe daño y reduce la vida"""
        self.vida -= 1
        if self.vida <= 0:
            self.viva = False
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def get_color(self):
        """Retorna el color según la vida restante"""
        porcentaje = self.vida / BARRERA_VIDA
        if porcentaje > 0.6:
            return VERDE
        elif porcentaje > 0.3:
            return AMARILLO
        else:
            return ROJO
