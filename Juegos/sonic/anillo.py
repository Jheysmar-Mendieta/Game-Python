"""Clase que maneja los anillos coleccionables"""
import pygame
from config import *

class Anillo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = ANILLO_RADIO
        self.recolectado = False
        self.angulo = 0  # Para animación de rotación
    
    def actualizar(self):
        """Actualiza la animación del anillo"""
        self.angulo = (self.angulo + 5) % 360
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x - self.radio, self.y - self.radio, 
                          self.radio * 2, self.radio * 2)
    
    def recolectar(self):
        """Marca el anillo como recolectado"""
        self.recolectado = True