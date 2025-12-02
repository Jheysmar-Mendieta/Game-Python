"""Clase que maneja la lógica de los aliens"""
import pygame
from config import *

class Alien:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.ancho = ALIEN_ANCHO
        self.alto = ALIEN_ALTO
        self.tipo = tipo  # 0, 1, 2 (diferentes tipos de aliens)
        self.vivo = True
        self.puntos = (30, 20, 10)[tipo]  # Puntos según el tipo
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def morir(self):
        """Marca al alien como muerto"""
        self.vivo = False


class GrupoAliens:
    """Maneja el grupo completo de aliens"""
    def __init__(self):
        self.aliens = []
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        self.velocidad = ALIEN_VELOCIDAD_INICIAL
        self.crear_formacion()
    
    def crear_formacion(self):
        """Crea la formación inicial de aliens"""
        inicio_x = (ANCHO - (ALIEN_COLUMNAS * ALIEN_ESPACIADO_X)) // 2
        inicio_y = 80
        
        for fila in range(ALIEN_FILAS):
            tipo = fila // 2  # Diferentes tipos según la fila
            for col in range(ALIEN_COLUMNAS):
                x = inicio_x + col * ALIEN_ESPACIADO_X
                y = inicio_y + fila * ALIEN_ESPACIADO_Y
                self.aliens.append(Alien(x, y, tipo))
    
    def actualizar(self):
        """Actualiza la posición de todos los aliens"""
        # Verificar si algún alien toca los bordes
        bajar = False
        for alien in self.aliens:
            if alien.vivo:
                if (alien.x <= 0 and self.direccion == -1) or \
                   (alien.x >= ANCHO - ALIEN_ANCHO and self.direccion == 1):
                    bajar = True
                    break
        
        # Si toca el borde, cambiar dirección y bajar
        if bajar:
            self.direccion *= -1
            for alien in self.aliens:
                if alien.vivo:
                    alien.y += ALIEN_VELOCIDAD_BAJADA
        
        # Mover todos los aliens
        for alien in self.aliens:
            if alien.vivo:
                alien.x += self.velocidad * self.direccion
    
    def obtener_aliens_vivos(self):
        """Retorna lista de aliens vivos"""
        return [alien for alien in self.aliens if alien.vivo]
    
    def todos_muertos(self):
        """Verifica si todos los aliens están muertos"""
        return len(self.obtener_aliens_vivos()) == 0
    
    def aumentar_velocidad(self):
        """Aumenta la velocidad cuando quedan pocos aliens"""
        vivos = len(self.obtener_aliens_vivos())
        if vivos < 10:
            self.velocidad = ALIEN_VELOCIDAD_INICIAL * 2
        elif vivos < 20:
            self.velocidad = ALIEN_VELOCIDAD_INICIAL * 1.5
