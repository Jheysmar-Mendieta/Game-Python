"""Clase que maneja los enemigos"""
import pygame
from config import *

class Enemigo:
    def __init__(self, x, y, velocidad=2):
        self.x = x
        self.y = y
        self.ancho = ENEMIGO_ANCHO
        self.alto = ENEMIGO_ALTO
        self.velocidad = velocidad
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        self.vivo = True
        self.rango_inicio = x - 100
        self.rango_fin = x + 100
    
    def actualizar(self):
        """Actualiza el movimiento del enemigo"""
        if not self.vivo:
            return
        
        self.x += self.velocidad * self.direccion
        
        # Cambiar dirección en los límites del rango
        if self.x <= self.rango_inicio or self.x >= self.rango_fin:
            self.direccion *= -1
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def morir(self):
        """Marca al enemigo como muerto"""
        self.vivo = False
