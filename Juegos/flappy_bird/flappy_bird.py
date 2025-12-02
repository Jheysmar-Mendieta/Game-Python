"""Juego Flappy Bird - Archivo principal con lógica de juego y ejecución"""
import pygame
import sys
sys.path.append("../../")  # Para importar db.py desde raíz

from config import *
from pajaro import Pajaro
from tubo import Tubo
from renderizador import Renderizador

# Intentar importar DatabaseManager, si no existe, usar una versión mock
try:
    from db import DatabaseManager
    DB_DISPONIBLE = True
except ImportError:
    DB_DISPONIBLE = False
    print("⚠ Base de datos no disponible. El juego funcionará sin guardar puntuaciones.")
    
    class DatabaseManager:
        """Mock de DatabaseManager cuando no está disponible"""
        def __init__(self):
            pass
        def guardar_puntuacion(self, *args):
            return False
        def cerrar(self):
            pass


class Juego:
    """Clase principal que maneja la lógica del juego"""
    
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.renderizador = Renderizador(self.ventana)
        self.db = DatabaseManager() if DB_DISPONIBLE else None
        self.mejor_puntuacion = 0
        self.jugando = True
    
    def pantalla_inicio(self):
        """Muestra la pantalla de inicio"""
        esperando = True
        while esperando:
            self.renderizador.dibujar_pantalla_inicio()
            self.renderizador.actualizar()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        return True
        return False
    
    def nueva_partida(self):
        """Inicializa una nueva partida"""
        self.pajaro = Pajaro(100, ALTO // 2)
        self.tubos = []
        self.puntuacion = 0
        self.contador_frames = 0
        
        # Crear primer tubo
        self.tubos.append(Tubo(ANCHO + 100))
    
    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.pajaro.saltar()
        
        return True
    
    def actualizar_logica(self):
        """Actualiza la lógica del juego"""
        self.pajaro.actualizar()
        
        # Verificar colisión con suelo o techo
        if (self.pajaro.colisiona_con_suelo(self.renderizador.get_altura_suelo()) or
            self.pajaro.colisiona_con_techo()):
            self.pajaro.morir()
            return False
        
        # Actualizar tubos
        for tubo in self.tubos:
            tubo.actualizar()
            
            # Verificar colisión con tubos
            if tubo.colisiona_con_pajaro(self.pajaro):
                self.pajaro.morir()
                return False
            
            # Contar puntos
            if not tubo.pasado and tubo.x + tubo.ancho < self.pajaro.x:
                tubo.pasado = True
                self.puntuacion += 1
        
        # Eliminar tubos fuera de pantalla
        self.tubos = [tubo for tubo in self.tubos if not tubo.esta_fuera_de_pantalla()]
        
        # Generar nuevos tubos
        self.contador_frames += 1
        if self.contador_frames >= DISTANCIA_TUBOS / VELOCIDAD_TUBOS:
            self.tubos.append(Tubo(ANCHO))
            self.contador_frames = 0
        
        return True
    
    def renderizar(self):
        """Renderiza todos los elementos del juego"""
        self.renderizador.limpiar_pantalla()
        
        # Dibujar tubos
        for tubo in self.tubos:
            self.renderizador.dibujar_tubo(tubo)
        
        self.renderizador.dibujar_suelo()
        self.renderizador.dibujar_pajaro(self.pajaro)
        self.renderizador.dibujar_puntuacion(self.puntuacion)
        self.renderizador.actualizar()
    
    def pedir_nombre(self):
        """Pide al jugador que ingrese su nombre (3 letras estilo arcade)"""
        nombre = ""
        ingresando = True
        
        while ingresando:
            self.renderizador.dibujar_pantalla_ingreso_nombre(nombre)
            self.renderizador.actualizar()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and len(nombre) == 3:
                        return nombre.upper()
                    
                    elif evento.key == pygame.K_BACKSPACE and len(nombre) > 0:
                        nombre = nombre[:-1]
                    
                    elif len(nombre) < 3:
                        if evento.unicode.isalpha():
                            nombre += evento.unicode.upper()
        
        return None
    
    def game_over(self):
        """Maneja la pantalla de game over y guarda puntuación si corresponde"""
        # Actualizar mejor puntuación local
        if self.puntuacion > self.mejor_puntuacion:
            self.mejor_puntuacion = self.puntuacion
        
        # Si hay puntuación y DB disponible, pedir nombre y guardar
        if self.puntuacion > 0 and DB_DISPONIBLE and self.db:
            nombre = self.pedir_nombre()
            
            if nombre:
                self.renderizador.dibujar_pantalla_guardando()
                self.renderizador.actualizar()
                pygame.time.delay(500)
                
                self.db.guardar_puntuacion(nombre, "Flappy Bird", self.puntuacion)
        
        # Mostrar pantalla de game over
        self.renderizador.dibujar_pantalla_game_over(self.puntuacion, self.mejor_puntuacion)
        self.renderizador.mostrar_texto("ESPACIO para jugar - ESC para salir", 
                                        ANCHO // 2, ALTO // 2 + 80, 
                                        self.renderizador.fuente_pequeña, AZUL)
        self.renderizador.actualizar()
        
        # Esperar decisión del jugador
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        return True  # Reiniciar
                    elif evento.key == pygame.K_ESCAPE:
                        return False  # Salir
        
        return False
    
    def ejecutar(self):
        """Loop principal del juego"""
        # Mostrar pantalla de inicio
        if not self.pantalla_inicio():
            self.jugando = False
        
        while self.jugando:
            self.nueva_partida()
            
            partida_activa = True
            while partida_activa:
                if not self.manejar_eventos():
                    self.jugando = False
                    break
                
                if not self.actualizar_logica():
                    partida_activa = False
                
                self.renderizar()
                self.clock.tick(FPS)
            
            if self.jugando:
                self.jugando = self.game_over()
        
        # Cerrar conexión a la base de datos
        if self.db:
            self.db.cerrar()
        pygame.quit()


# Punto de entrada del juego
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()