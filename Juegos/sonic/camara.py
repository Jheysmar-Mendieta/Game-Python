"""Clase que maneja la cámara con scroll horizontal"""
from config import *

class Camara:
    def __init__(self):
        self.offset_x = 0
    
    def actualizar(self, sonic, ancho_nivel):
        """Actualiza el offset de la cámara siguiendo a Sonic"""
        # Calcular la posición objetivo de la cámara
        objetivo = sonic.x - SCROLL_MARGEN
        
        # Limitar el scroll
        if objetivo < 0:
            self.offset_x = 0
        elif objetivo > ancho_nivel - ANCHO:
            self.offset_x = ancho_nivel - ANCHO
        else:
            self.offset_x = objetivo
    
    def aplicar(self, objeto_x):
        """Aplica el offset de la cámara a una coordenada X"""
        return objeto_x - self.offset_x
