"""Clase que maneja la lógica de la serpiente"""
import random
from config import TAM, ANCHO, ALTO

class Serpiente:
    def __init__(self, x, y):
        self.cuerpo = [(x, y)]
        self.direccion = (0, 0)  # (dx, dy)
        self.longitud = 1
        self.creciendo = False
    
    def cambiar_direccion(self, dx, dy):
        """Cambia la dirección si es válida (no reversa)"""
        actual_dx, actual_dy = self.direccion
        
        # No permitir ir en reversa
        if dx != 0 and actual_dx == 0:
            self.direccion = (dx, dy)
        elif dy != 0 and actual_dy == 0:
            self.direccion = (dx, dy)
    
    def mover(self):
        """Mueve la serpiente en la dirección actual"""
        if self.direccion == (0, 0):
            return  # No se mueve hasta que se presione una tecla
        
        dx, dy = self.direccion
        cabeza_x, cabeza_y = self.cuerpo[-1]
        nueva_cabeza = (cabeza_x + dx, cabeza_y + dy)
        
        self.cuerpo.append(nueva_cabeza)
        
        if not self.creciendo:
            self.cuerpo.pop(0)
        else:
            self.creciendo = False
    
    def crecer(self):
        """Marca que la serpiente debe crecer en el próximo movimiento"""
        self.longitud += 1
        self.creciendo = True
    
    def colisiona_consigo_misma(self):
        """Verifica si la cabeza colisiona con el cuerpo"""
        cabeza = self.cuerpo[-1]
        return cabeza in self.cuerpo[:-1]
    
    def colisiona_con_borde(self):
        """Verifica si la cabeza está fuera de los límites"""
        cabeza_x, cabeza_y = self.cuerpo[-1]
        return cabeza_x < 0 or cabeza_x >= ANCHO or cabeza_y < 0 or cabeza_y >= ALTO
    
    def get_cabeza(self):
        """Retorna la posición de la cabeza"""
        return self.cuerpo[-1]
    
    def get_cuerpo(self):
        """Retorna todo el cuerpo"""
        return self.cuerpo