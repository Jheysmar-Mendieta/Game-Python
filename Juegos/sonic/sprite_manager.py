"""Gestor de sprites y animaciones para Sonic"""
import pygame
import math
from config import *

class SpriteManager:
    """Maneja la carga y creación de sprites del juego"""
    
    def __init__(self):
        self.sprites = {}
        self.crear_sprites()
    
    def crear_sprites(self):
        """Crea todos los sprites del juego"""
        self.crear_sonic_sprites()
        self.crear_anillo_sprite()
        self.crear_enemigo_sprites()
        self.crear_tiles_mapa()
    
    def crear_sonic_sprites(self):
        """Crea los sprites de Sonic (idle, run, jump)"""
        # IDLE - Sonic parado
        idle = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Cuerpo
        pygame.draw.circle(idle, AZUL_SONIC, (20, 20), 15)
        # Panza blanca
        pygame.draw.circle(idle, (240, 220, 200), (20, 22), 8)
        # Ojos
        pygame.draw.ellipse(idle, BLANCO, (14, 14, 8, 10))
        pygame.draw.ellipse(idle, BLANCO, (26, 14, 8, 10))
        pygame.draw.circle(idle, NEGRO, (17, 18), 3)
        pygame.draw.circle(idle, NEGRO, (29, 18), 3)
        pygame.draw.circle(idle, BLANCO, (18, 17), 1)
        pygame.draw.circle(idle, BLANCO, (30, 17), 1)
        # Púas
        for i in range(3):
            x = 10 + i * 8
            pygame.draw.polygon(idle, AZUL_SONIC, [
                (x, 8), (x + 4, 2), (x + 8, 8)
            ])
        self.sprites['sonic_idle'] = idle
        
        # RUN - Sonic corriendo (frames de animación)
        run_frames = []
        for frame in range(4):
            run = pygame.Surface((40, 40), pygame.SRCALPHA)
            offset_y = 2 if frame % 2 == 0 else 0
            # Cuerpo más ovalado
            pygame.draw.ellipse(run, AZUL_SONIC, (8, 12 + offset_y, 28, 20))
            # Panza
            pygame.draw.ellipse(run, (240, 220, 200), (14, 16 + offset_y, 16, 12))
            # Ojos
            pygame.draw.ellipse(run, BLANCO, (14, 14 + offset_y, 8, 8))
            pygame.draw.ellipse(run, BLANCO, (24, 14 + offset_y, 8, 8))
            pygame.draw.circle(run, NEGRO, (17, 17 + offset_y), 2)
            pygame.draw.circle(run, NEGRO, (27, 17 + offset_y), 2)
            # Púas inclinadas
            for i in range(3):
                x = 8 + i * 9
                pygame.draw.polygon(run, AZUL_SONIC, [
                    (x, 8 + offset_y), (x + 3, 3 + offset_y), (x + 8, 10 + offset_y)
                ])
            # Líneas de velocidad
            for i in range(3):
                pygame.draw.line(run, CYAN, (2, 18 + i * 4), (8, 18 + i * 4), 2)
            run_frames.append(run)
        self.sprites['sonic_run'] = run_frames
        
        # JUMP - Sonic en bola
        jump = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Bola girando
        pygame.draw.circle(jump, AZUL_SONIC, (20, 20), 16)
        # Rayas de púas
        for i in range(4):
            angle = i * 90
            # Calcular posiciones usando matemáticas
            angle_rad = math.radians(angle)
            start_x = 20 + int(12 * math.cos(angle_rad))
            start_y = 20 + int(12 * math.sin(angle_rad))
            end_x = 20 + int(16 * math.cos(angle_rad))
            end_y = 20 + int(16 * math.sin(angle_rad))
            pygame.draw.line(jump, AZUL_OSCURO, (start_x, start_y), (end_x, end_y), 3)
        self.sprites['sonic_jump'] = jump
    
    def crear_anillo_sprite(self):
        """Crea los frames de animación del anillo"""
        frames = []
        for i in range(8):
            frame = pygame.Surface((30, 30), pygame.SRCALPHA)
            # Efecto de rotación 3D
            width = int(20 * abs(math.cos(i * math.pi / 4)))
            if width > 2:
                # Anillo exterior dorado
                pygame.draw.ellipse(frame, AMARILLO, (15 - width//2, 7, width, 16))
                # Interior más oscuro
                inner_width = max(2, width - 6)
                pygame.draw.ellipse(frame, (200, 160, 0), (15 - inner_width//2, 10, inner_width, 10))
                # Brillo
                pygame.draw.ellipse(frame, (255, 255, 150), (15 - width//2, 8, width//2, 4))
            frames.append(frame)
        self.sprites['anillo'] = frames
    
    def crear_enemigo_sprites(self):
        """Crea los sprites de los enemigos (Badnik estilo Sonic)"""
        # Enemigo tipo "Motobug"
        enemigo = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Cuerpo rojo
        pygame.draw.ellipse(enemigo, ROJO, (5, 15, 30, 18))
        # Cabeza
        pygame.draw.circle(enemigo, (180, 0, 0), (20, 20), 10)
        # Ojos verdes brillantes
        pygame.draw.circle(enemigo, (0, 255, 0), (16, 18), 4)
        pygame.draw.circle(enemigo, (0, 255, 0), (24, 18), 4)
        pygame.draw.circle(enemigo, (0, 150, 0), (16, 18), 2)
        pygame.draw.circle(enemigo, (0, 150, 0), (24, 18), 2)
        # Antena
        pygame.draw.line(enemigo, (80, 80, 80), (20, 10), (20, 5), 2)
        pygame.draw.circle(enemigo, AMARILLO, (20, 5), 3)
        # Ruedas
        pygame.draw.circle(enemigo, (40, 40, 40), (12, 32), 5)
        pygame.draw.circle(enemigo, (40, 40, 40), (28, 32), 5)
        pygame.draw.circle(enemigo, (80, 80, 80), (12, 32), 3)
        pygame.draw.circle(enemigo, (80, 80, 80), (28, 32), 3)
        self.sprites['enemigo'] = enemigo
    
    def crear_tiles_mapa(self):
        """Crea los tiles para el mapa"""
        # Tile de pasto (superficie de plataforma)
        pasto = pygame.Surface((20, 20))
        pasto.fill(VERDE_PASTO)
        # Detalles de césped
        for i in range(5):
            x = i * 4 + 2
            pygame.draw.line(pasto, (20, 120, 20), (x, 15), (x, 19), 1)
            pygame.draw.line(pasto, (50, 180, 50), (x+1, 16), (x+1, 19), 1)
        self.sprites['pasto'] = pasto
        
        # Tile de tierra
        tierra = pygame.Surface((20, 20))
        tierra.fill(MARRON)
        # Textura de tierra
        for i in range(10):
            x = (i * 7) % 20
            y = (i * 11) % 20
            pygame.draw.circle(tierra, (120, 60, 20), (x, y), 2)
        self.sprites['tierra'] = tierra
        
        # Tile de piedra para plataformas flotantes
        piedra = pygame.Surface((20, 20))
        piedra.fill((100, 100, 100))
        # Textura de piedra
        pygame.draw.rect(piedra, (120, 120, 120), (0, 0, 19, 19), 1)
        pygame.draw.line(piedra, (80, 80, 80), (5, 5), (15, 15), 1)
        pygame.draw.line(piedra, (80, 80, 80), (15, 5), (5, 15), 1)
        self.sprites['piedra'] = piedra
        
        # Fondo de cielo con nubes
        fondo = pygame.Surface((ANCHO, ALTO))
        # Degradado de cielo
        for y in range(ALTO):
            color_r = 135 + int((y / ALTO) * 50)
            color_g = 206 - int((y / ALTO) * 50)
            color_b = 250
            pygame.draw.line(fondo, (color_r, color_g, color_b), (0, y), (ANCHO, y))
        # Nubes
        for i in range(8):
            x = (i * 150 + 50) % ANCHO
            y = 50 + (i * 70) % 200
            # Nube con varios círculos
            pygame.draw.circle(fondo, BLANCO, (x, y), 25)
            pygame.draw.circle(fondo, BLANCO, (x + 20, y), 20)
            pygame.draw.circle(fondo, BLANCO, (x - 20, y), 20)
            pygame.draw.circle(fondo, BLANCO, (x + 10, y - 15), 18)
        self.sprites['fondo'] = fondo
    
    def get_sprite(self, nombre):
        """Obtiene un sprite por nombre"""
        return self.sprites.get(nombre)