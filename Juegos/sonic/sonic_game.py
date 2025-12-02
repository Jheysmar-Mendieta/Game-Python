"""Juego Sonic - Archivo principal con lógica de juego y ejecución"""
import pygame
import sys
from config import *
from sonic import Sonic
from nivel import Nivel
from camara import Camara
from renderizador import Renderizador
from sprite_manager import SpriteManager

# Intentar importar DatabaseManager
try:
    from db import DatabaseManager
    DB_DISPONIBLE = True
except ImportError:
    DB_DISPONIBLE = False
    print("⚠ Base de datos no disponible.")
    
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
        pygame.display.set_caption("Sonic The Hedgehog")
        self.clock = pygame.time.Clock()
        self.sprite_manager = SpriteManager()
        self.renderizador = Renderizador(self.ventana, self.sprite_manager)
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
        self.sonic = Sonic(100, 100, self.sprite_manager)
        self.nivel_actual = 1
        self.nivel = Nivel(self.nivel_actual)
        self.camara = Camara()
        self.anillos_recolectados = 0
        self.tiempo = 0
        self.frame_count = 0
    
    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.sonic.saltar()
                if evento.key == pygame.K_ESCAPE:
                    return False
        
        # Movimiento continuo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.sonic.mover_izquierda()
        if teclas[pygame.K_RIGHT]:
            self.sonic.mover_derecha()
        
        return True
    
    def actualizar_logica(self):
        """Actualiza la lógica del juego"""
        # Actualizar tiempo (cada segundo = 60 frames)
        self.frame_count += 1
        if self.frame_count >= FPS:
            self.tiempo += 1
            self.frame_count = 0
        
        # Actualizar Sonic
        self.sonic.actualizar(self.nivel.plataformas)
        
        if not self.sonic.vivo:
            return False
        
        # Actualizar nivel
        self.nivel.actualizar()
        
        # Actualizar cámara
        self.camara.actualizar(self.sonic, self.nivel.ancho_total)
        
        # Colisiones con anillos
        sonic_rect = self.sonic.get_rect()
        for anillo in self.nivel.obtener_anillos_activos():
            if sonic_rect.colliderect(anillo.get_rect()):
                anillo.recolectar()
                self.anillos_recolectados += 1
        
        # Colisiones con enemigos
        if not self.sonic.invencible:
            for enemigo in self.nivel.obtener_enemigos_vivos():
                if sonic_rect.colliderect(enemigo.get_rect()):
                    # Si Sonic está cayendo sobre el enemigo
                    if self.sonic.velocidad_y > 0 and self.sonic.y < enemigo.y:
                        enemigo.morir()
                        self.sonic.velocidad_y = -10  # Rebote
                        self.anillos_recolectados += 5
                    else:
                        # Perder anillos
                        if self.anillos_recolectados > 0:
                            self.anillos_recolectados = max(0, self.anillos_recolectados - 10)
                            self.sonic.activar_invencibilidad()
                        else:
                            self.sonic.morir()
                            return False
        
        # Verificar si llegó al final del nivel
        if self.sonic.x > self.nivel.ancho_total - 200:
            self.nivel_completado()
        
        return True
    
    def nivel_completado(self):
        """Avanza al siguiente nivel"""
        self.renderizador.dibujar_pantalla_nivel_completado(self.nivel_actual)
        self.renderizador.actualizar()
        pygame.time.delay(2000)
        
        self.nivel_actual += 1
        self.nivel = Nivel(self.nivel_actual)
        self.sonic = Sonic(100, 100, self.sprite_manager)
        self.camara = Camara()
    
    def renderizar(self):
        """Renderiza todos los elementos del juego"""
        self.renderizador.limpiar_pantalla(self.camara)
        
        # Dibujar plataformas
        for plataforma in self.nivel.plataformas:
            self.renderizador.dibujar_plataforma(plataforma, self.camara)
        
        # Dibujar anillos
        for anillo in self.nivel.obtener_anillos_activos():
            self.renderizador.dibujar_anillo(anillo, self.camara)
        
        # Dibujar enemigos
        for enemigo in self.nivel.obtener_enemigos_vivos():
            self.renderizador.dibujar_enemigo(enemigo, self.camara)
        
        # Dibujar Sonic
        if self.sonic.vivo:
            self.renderizador.dibujar_sonic(self.sonic, self.camara)
        
        # Dibujar HUD
        self.renderizador.dibujar_hud(self.anillos_recolectados, self.tiempo, self.nivel_actual)
        
        self.renderizador.actualizar()
    
    def pedir_nombre(self):
        """Pide el nombre al jugador para guardar puntuación"""
        nombre = ""
        esperando = True
        
        while esperando and len(nombre) < 3:
            self.renderizador.dibujar_pantalla_ingreso_nombre(nombre)
            self.renderizador.actualizar()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and len(nombre) == 3:
                        esperando = False
                    elif evento.key == pygame.K_BACKSPACE and len(nombre) > 0:
                        nombre = nombre[:-1]
                    elif evento.unicode.isalpha() and len(nombre) < 3:
                        nombre += evento.unicode.upper()
        
        return nombre if len(nombre) == 3 else None
    
    def game_over(self):
        """Muestra la pantalla de game over"""
        self.renderizador.dibujar_pantalla_game_over(
            self.anillos_recolectados, 
            self.tiempo, 
            self.nivel_actual
        )
        self.renderizador.actualizar()
        
        # Intentar guardar puntuación si la DB está disponible
        if DB_DISPONIBLE and self.db:
            nombre = self.pedir_nombre()
            if nombre:
                self.renderizador.dibujar_pantalla_guardando()
                self.renderizador.actualizar()
                self.db.guardar_puntuacion(nombre, self.anillos_recolectados, self.tiempo)
                pygame.time.delay(1000)
        
        pygame.time.delay(3000)
    
    def ejecutar(self):
        """Bucle principal del juego"""
        if not self.pantalla_inicio():
            self.jugando = False
        
        while self.jugando:
            # Nueva partida
            self.nueva_partida()
            
            # Bucle de juego
            jugando_nivel = True
            while jugando_nivel:
                self.clock.tick(FPS)
                
                # Manejar eventos
                if not self.manejar_eventos():
                    jugando_nivel = False
                    self.jugando = False
                    break
                
                # Actualizar lógica
                if not self.actualizar_logica():
                    jugando_nivel = False
                    self.game_over()
                    self.jugando = False
                    break
                
                # Renderizar
                self.renderizar()
        
        # Cerrar
        if self.db:
            self.db.cerrar()
        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    juego = Juego()
    juego.ejecutar()


if __name__ == "__main__":
    main()