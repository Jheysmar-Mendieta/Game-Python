"""Clase que maneja la lógica de los tubos"""
import pygame
import random
from config import *

class Tubo:
    def __init__(self, x):
        self.x = x
        self.ancho = 60
        self.altura_hueco = ESPACIO_TUBOS
        
        # Altura aleatoria del hueco (posición Y del centro del hueco)
        altura_minima = 100
        altura_maxima = ALTO - 100 - self.altura_hueco
        self.y_hueco = random.randint(altura_minima, altura_maxima)
        
        self.pasado = False  # Para contar puntos
    
    def actualizar(self):
        """Mueve el tubo hacia la izquierda"""
        self.x -= VELOCIDAD_TUBOS
    
    def esta_fuera_de_pantalla(self):
        """Verifica si el tubo salió completamente de la pantalla"""
        return self.x + self.ancho < 0
    
    def get_rect_superior(self):
        """Retorna el rectángulo del tubo superior"""
        return pygame.Rect(self.x, 0, self.ancho, self.y_hueco)
    
    def get_rect_inferior(self):
        """Retorna el rectángulo del tubo inferior"""
        return pygame.Rect(
            self.x,
            self.y_hueco + self.altura_hueco,
            self.ancho,
            ALTO - (self.y_hueco + self.altura_hueco)
        )
    
    def colisiona_con_pajaro(self, pajaro):
        """Verifica si el pájaro colisiona con este tubo"""
        pajaro_rect = pajaro.get_rect()
        return (pajaro_rect.colliderect(self.get_rect_superior()) or
                pajaro_rect.colliderect(self.get_rect_inferior()))
