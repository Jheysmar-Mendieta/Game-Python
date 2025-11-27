"""Clase que maneja la lógica de la manzana"""
import random
from config import TAM, ANCHO, ALTO

class Manzana:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.generar_nueva_posicion()
    
    def generar_nueva_posicion(self, posiciones_ocupadas=None):
        """Genera una nueva posición aleatoria evitando posiciones ocupadas"""
        if posiciones_ocupadas is None:
            posiciones_ocupadas = []
        
        while True:
            self.x = random.randrange(0, ANCHO - TAM, TAM)
            self.y = random.randrange(0, ALTO - TAM, TAM)
            if (self.x, self.y) not in posiciones_ocupadas:
                break
    
    def get_posicion(self):
        """Retorna la posición de la manzana"""
        return (self.x, self.y)