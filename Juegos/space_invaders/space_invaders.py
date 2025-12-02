"""Juego Space Invaders - Archivo principal con lógica de juego y ejecución"""
import pygame
import random
import sys
sys.path.append("../../")  # Para importar db.py desde raíz

from config import *
from jugador import Jugador
from alien import GrupoAliens
from disparo import Disparo
from barrera import Barrera
from renderizador import Renderizador

# Intentar importar DatabaseManager
try:
    from db import DatabaseManager
    DB_DISPONIBLE = True
except ImportError:
    DB_DISPONIBLE = False
    print("⚠ Base de datos no disponible. El juego funcionará sin guardar puntuaciones.")
    
    class DatabaseManager:
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
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.renderizador = Renderizador(self.ventana)
        self.db = DatabaseManager() if DB_DISPONIBLE else None
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
        self.jugador = Jugador(ANCHO // 2 - JUGADOR_ANCHO // 2, ALTO - 80)
        self.aliens = GrupoAliens()
        self.disparos_jugador = []
        self.barreras = self.crear_barreras()
        self.puntuacion = 0
        self.vidas = 3
        self.nivel = 1
        self.ultimo_disparo = 0
    
    def crear_barreras(self):
        """Crea las barreras protectoras"""
        barreras = []
        num_barreras = 4
        espacio_total = ANCHO - (num_barreras * BARRERA_ANCHO)
        espacio = espacio_total // (num_barreras + 1)
        
        y = ALTO - 150
        for i in range(num_barreras):
            x = espacio + i * (BARRERA_ANCHO + espacio)
            barreras.append(Barrera(x, y))
        
        return barreras
    
    def nivel_completado(self):
        """Avanza al siguiente nivel"""
        self.nivel += 1
        
        # Mostrar pantalla de nivel completado
        self.renderizador.dibujar_pantalla_nivel_completado(self.nivel - 1)
        self.renderizador.actualizar()
        pygame.time.delay(2000)
        
        # Reiniciar elementos para el nuevo nivel
        self.aliens = GrupoAliens()
        self.aliens.velocidad += 0.5  # Aumentar velocidad cada nivel
        self.disparos_jugador = []
        self.barreras = self.crear_barreras()
    
    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.disparar()
        
        # Movimiento continuo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.jugador.mover_izquierda()
        if teclas[pygame.K_RIGHT]:
            self.jugador.mover_derecha()
        
        return True
    
    def disparar(self):
        """El jugador dispara"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > DISPARO_COOLDOWN:
            x = self.jugador.x + self.jugador.ancho // 2 - DISPARO_ANCHO // 2
            y = self.jugador.y
            self.disparos_jugador.append(Disparo(x, y, 1))
            self.ultimo_disparo = tiempo_actual
    
    def actualizar_logica(self):
        """Actualiza la lógica del juego"""
        # Actualizar aliens
        self.aliens.actualizar()
        self.aliens.aumentar_velocidad()
        
        # Verificar si los aliens llegaron al jugador
        for alien in self.aliens.obtener_aliens_vivos():
            if alien.y + alien.alto >= self.jugador.y:
                self.vidas = 0  # Game over instantáneo
                return False
        
        # Actualizar disparos
        for disparo in self.disparos_jugador[:]:
            disparo.actualizar()
            if not disparo.activo:
                self.disparos_jugador.remove(disparo)
        
        # Colisiones: disparos con aliens
        for disparo in self.disparos_jugador[:]:
            for alien in self.aliens.obtener_aliens_vivos():
                if disparo.get_rect().colliderect(alien.get_rect()):
                    alien.morir()
                    self.puntuacion += alien.puntos
                    if disparo in self.disparos_jugador:
                        self.disparos_jugador.remove(disparo)
                    break
        
        # Colisiones: disparos con barreras
        for disparo in self.disparos_jugador[:]:
            for barrera in self.barreras:
                if barrera.viva and disparo.get_rect().colliderect(barrera.get_rect()):
                    barrera.recibir_danio()
                    if disparo in self.disparos_jugador:
                        self.disparos_jugador.remove(disparo)
                    break
        
        # Verificar si se completó el nivel
        if self.aliens.todos_muertos():
            self.nivel_completado()
        
        return True
    
    def renderizar(self):
        """Renderiza todos los elementos del juego"""
        self.renderizador.limpiar_pantalla()
        
        # Dibujar barreras
        for barrera in self.barreras:
            if barrera.viva:
                self.renderizador.dibujar_barrera(barrera)
        
        # Dibujar aliens
        for alien in self.aliens.obtener_aliens_vivos():
            self.renderizador.dibujar_alien(alien)
        
        # Dibujar disparos
        for disparo in self.disparos_jugador:
            self.renderizador.dibujar_disparo(disparo)
        
        # Dibujar jugador
        if self.jugador.vivo:
            self.renderizador.dibujar_jugador(self.jugador)
        
        # Dibujar HUD
        self.renderizador.dibujar_hud(self.puntuacion, self.vidas, self.nivel)
        
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
        # Si hay puntuación y DB disponible, pedir nombre y guardar
        if self.puntuacion > 0 and DB_DISPONIBLE and self.db:
            nombre = self.pedir_nombre()
            
            if nombre:
                self.renderizador.dibujar_pantalla_guardando()
                self.renderizador.actualizar()
                pygame.time.delay(500)
                
                self.db.guardar_puntuacion(nombre, "Space Invaders", self.puntuacion)
        
        # Mostrar pantalla de game over
        self.renderizador.dibujar_pantalla_game_over(self.puntuacion, self.nivel)
        self.renderizador.mostrar_texto("ESPACIO para jugar - ESC para salir", 
                                        ANCHO // 2, ALTO // 2 + 100, 
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
                
                # Verificar si perdió todas las vidas
                if self.vidas <= 0:
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