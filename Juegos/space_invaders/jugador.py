"""Clase que maneja la lógica del jugador"""
import pygame
from config import *

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = JUGADOR_ANCHO
        self.alto = JUGADOR_ALTO
        self.velocidad = JUGADOR_VELOCIDAD
        self.vivo = True
    
    def mover_izquierda(self):
        """Mueve el jugador a la izquierda"""
        if self.x > 0:
            self.x -= self.velocidad
    
    def mover_derecha(self):
        """Mueve el jugador a la derecha"""
        if self.x < ANCHO - self.ancho:
            self.x += self.velocidad
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def morir(self):
        """Marca al jugador como muerto"""
        self.vivo = False