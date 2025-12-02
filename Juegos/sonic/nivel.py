"""Clase que maneja la generación y lógica de niveles"""
import random
from plataforma import Plataforma
from anillo import Anillo
from enemigo import Enemigo
from config import *

class Nivel:
    def __init__(self, numero):
        self.numero = numero
        self.ancho_total = 3000  # Nivel largo con scroll
        self.plataformas = []
        self.anillos = []
        self.enemigos = []
        self.generar_nivel()
    
    def generar_nivel(self):
        """Genera el nivel con plataformas, anillos y enemigos"""
        # Suelo base
        self.plataformas.append(Plataforma(0, ALTO - 50, self.ancho_total, 50))
        
        # Plataformas flotantes
        for i in range(15):
            x = random.randint(200, self.ancho_total - 300)
            y = random.randint(200, ALTO - 150)
            ancho = random.randint(100, 200)
            self.plataformas.append(Plataforma(x, y, ancho, 20))
        
        # Generar anillos
        for i in range(ANILLOS_POR_NIVEL):
            x = random.randint(100, self.ancho_total - 100)
            y = random.randint(100, ALTO - 100)
            self.anillos.append(Anillo(x, y))
        
        # Generar enemigos
        for i in range(ENEMIGOS_POR_NIVEL):
            x = random.randint(300, self.ancho_total - 300)
            y = ALTO - 100  # En el suelo
            self.enemigos.append(Enemigo(x, y))
    
    def actualizar(self):
        """Actualiza todos los elementos del nivel"""
        for anillo in self.anillos:
            if not anillo.recolectado:
                anillo.actualizar()
        
        for enemigo in self.enemigos:
            if enemigo.vivo:
                enemigo.actualizar()
    
    def obtener_anillos_activos(self):
        """Retorna lista de anillos no recolectados"""
        return [a for a in self.anillos if not a.recolectado]
    
    def obtener_enemigos_vivos(self):
        """Retorna lista de enemigos vivos"""
        return [e for e in self.enemigos if e.vivo]