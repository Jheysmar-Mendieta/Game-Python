"""Sistema de pistas para el juego de carreras"""
import pygame
import json
from config import *


class Track:
    """Representa una pista de carreras"""
    
    def __init__(self, track_id):
        self.track_id = track_id
        self.info = TRACKS[track_id]
        self.grid = []
        self.checkpoints = []
        self.spawn_points = []
        self.ai_path = []
        self.width = 0
        self.height = 0
        
        # Generar pista
        self._generate_track()
        
        # Crear superficie de la pista
        self._create_surface()
        
    def _generate_track(self):
        """Genera la pista según el ID"""
        if self.track_id == 'track1':
            self._generate_oval_track()
        elif self.track_id == 'track2':
            self._generate_serpentine_track()
        elif self.track_id == 'track3':
            self._generate_complex_track()
            
    def _generate_oval_track(self):
        """Genera pista oval simple"""
        # Grid: 0=césped, 1=pista, 2=checkpoint, 3=borde
        self.width = 40
        self.height = 30
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Crear pista oval
        center_x = self.width // 2
        center_y = self.height // 2
        
        for y in range(self.height):
            for x in range(self.width):
                # Distancia elíptica
                dx = (x - center_x) / (self.width * 0.35)
                dy = (y - center_y) / (self.height * 0.35)
                dist = dx * dx + dy * dy
                
                if 0.7 < dist < 1.3:
                    self.grid[y][x] = 1  # Pista
                elif 0.6 < dist < 0.75 or 1.25 < dist < 1.4:
                    self.grid[y][x] = 3  # Borde
                    
        # Checkpoints
        self.checkpoints = [
            pygame.Rect(center_x * TILE_SIZE - 50, 3 * TILE_SIZE, 100, TILE_SIZE * 2),
            pygame.Rect((self.width - 3) * TILE_SIZE, center_y * TILE_SIZE - 50, TILE_SIZE * 2, 100),
            pygame.Rect(center_x * TILE_SIZE - 50, (self.height - 5) * TILE_SIZE, 100, TILE_SIZE * 2),
        ]
        
        # Puntos de spawn
        for i in range(6):
            self.spawn_points.append((
                center_x * TILE_SIZE - 60 + i * 25,
                5 * TILE_SIZE
            ))
            
        # Ruta de IA (círculo)
        for angle in range(0, 360, 15):
            import math
            rad = math.radians(angle)
            x = center_x * TILE_SIZE + math.cos(rad) * (self.width * TILE_SIZE * 0.3)
            y = center_y * TILE_SIZE + math.sin(rad) * (self.height * TILE_SIZE * 0.3)
            self.ai_path.append((x, y))
            
    def _generate_serpentine_track(self):
        """Genera pista con curvas tipo serpiente"""
        self.width = 50
        self.height = 35
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        import math
        
        # Crear camino serpenteante
        for i in range(200):
            t = i / 200
            x = int(self.width * 0.2 + self.width * 0.6 * t)
            y = int(self.height * 0.5 + math.sin(t * math.pi * 4) * self.height * 0.3)
            
            # Dibujar pista alrededor del punto
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    px = x + dx
                    py = y + dy
                    if 0 <= py < self.height and 0 <= px < self.width:
                        dist = (dx*dx + dy*dy) ** 0.5
                        if dist < 3:
                            self.grid[py][px] = 1
                        elif dist < 4:
                            self.grid[py][px] = 3
                            
        # Checkpoints
        self.checkpoints = [
            pygame.Rect(self.width * TILE_SIZE * 0.25, self.height * TILE_SIZE * 0.3, 60, 80),
            pygame.Rect(self.width * TILE_SIZE * 0.5, self.height * TILE_SIZE * 0.7, 60, 80),
            pygame.Rect(self.width * TILE_SIZE * 0.75, self.height * TILE_SIZE * 0.4, 60, 80),
        ]
        
        # Spawn points
        start_x = int(self.width * 0.15 * TILE_SIZE)
        start_y = int(self.height * 0.5 * TILE_SIZE)
        for i in range(6):
            self.spawn_points.append((start_x, start_y - 30 + i * 12))
            
        # IA path sigue la curva
        for i in range(100):
            t = i / 100
            x = self.width * TILE_SIZE * (0.2 + 0.6 * t)
            y = self.height * TILE_SIZE * (0.5 + math.sin(t * math.pi * 4) * 0.3)
            self.ai_path.append((x, y))
            
    def _generate_complex_track(self):
        """Genera pista compleja"""
        self.width = 45
        self.height = 35
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Figura 8
        import math
        
        for i in range(300):
            t = i / 300 * 2 * math.pi
            scale = 0.35
            x = int(self.width * 0.5 + math.sin(t) * self.width * scale)
            y = int(self.height * 0.5 + math.sin(t * 2) * self.height * scale * 0.7)
            
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    px = x + dx
                    py = y + dy
                    if 0 <= py < self.height and 0 <= px < self.width:
                        dist = (dx*dx + dy*dy) ** 0.5
                        if dist < 2.5:
                            self.grid[py][px] = 1
                        elif dist < 3.5:
                            self.grid[py][px] = 3
                            
        # Checkpoints
        cx = self.width * TILE_SIZE * 0.5
        cy = self.height * TILE_SIZE * 0.5
        
        self.checkpoints = [
            pygame.Rect(cx - 40, cy - self.height * TILE_SIZE * 0.3, 80, 50),
            pygame.Rect(cx + self.width * TILE_SIZE * 0.25, cy, 50, 80),
            pygame.Rect(cx - 40, cy + self.height * TILE_SIZE * 0.25, 80, 50),
        ]
        
        # Spawn points
        for i in range(6):
            self.spawn_points.append((
                cx - 40 + i * 15,
                cy - self.height * TILE_SIZE * 0.35
            ))
            
        # AI path
        for i in range(150):
            t = i / 150 * 2 * math.pi
            scale = 0.35
            x = self.width * TILE_SIZE * (0.5 + math.sin(t) * scale)
            y = self.height * TILE_SIZE * (0.5 + math.sin(t * 2) * scale * 0.7)
            self.ai_path.append((x, y))
            
    def _create_surface(self):
        """Crea la superficie visual de la pista"""
        self.surface = pygame.Surface(
            (self.width * TILE_SIZE, self.height * TILE_SIZE)
        )
        
        # Dibujar tiles
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile == 0:  # Césped
                    color = COLORS['grass']
                    self.surface.fill(color, rect)
                    # Textura de césped
                    for _ in range(5):
                        import random
                        px = random.randint(rect.x, rect.right)
                        py = random.randint(rect.y, rect.bottom)
                        darker = tuple(max(0, c - 20) for c in color)
                        pygame.draw.circle(self.surface, darker, (px, py), 1)
                        
                elif tile == 1:  # Pista
                    self.surface.fill(COLORS['track'], rect)
                    # Líneas de pista
                    if (x + y) % 4 == 0:
                        pygame.draw.line(self.surface, (100, 100, 100),
                                       (rect.centerx, rect.top),
                                       (rect.centerx, rect.bottom), 1)
                        
                elif tile == 3:  # Borde
                    self.surface.fill(COLORS['border'], rect)
                    
        # Dibujar checkpoints en la superficie
        for i, checkpoint in enumerate(self.checkpoints):
            s = pygame.Surface((checkpoint.width, checkpoint.height), pygame.SRCALPHA)
            s.fill((255, 255, 100, 60))
            self.surface.blit(s, checkpoint)
            
            # Número de checkpoint
            font = pygame.font.Font(None, 36)
            text = font.render(str(i + 1), True, (255, 255, 255))
            text_rect = text.get_rect(center=checkpoint.center)
            self.surface.blit(text, text_rect)
            
    def check_collision(self, car):
        """Verifica colisión con bordes"""
        car_rect = car.get_collision_rect()
        
        # Verificar grid
        grid_x = int(car.x / TILE_SIZE)
        grid_y = int(car.y / TILE_SIZE)
        
        # Verificar tiles adyacentes
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                check_x = grid_x + dx
                check_y = grid_y + dy
                
                if 0 <= check_y < len(self.grid) and 0 <= check_x < len(self.grid[0]):
                    if self.grid[check_y][check_x] == 3:  # Borde
                        tile_rect = pygame.Rect(
                            check_x * TILE_SIZE, check_y * TILE_SIZE,
                            TILE_SIZE, TILE_SIZE
                        )
                        
                        if car_rect.colliderect(tile_rect):
                            # Calcular normal de colisión
                            normal_x = car.x - tile_rect.centerx
                            normal_y = car.y - tile_rect.centery
                            length = (normal_x**2 + normal_y**2) ** 0.5
                            if length > 0:
                                normal_x /= length
                                normal_y /= length
                                car.handle_collision(normal_x, normal_y)
                                return True
        return False
        
    def check_checkpoint(self, car):
        """Verifica paso por checkpoint"""
        car_rect = car.get_collision_rect()
        
        for i, checkpoint in enumerate(self.checkpoints):
            if car_rect.colliderect(checkpoint):
                car.pass_checkpoint(i)
                return i
        return None
        
    def draw(self, surface, camera_x, camera_y):
        """Dibuja la pista"""
        surface.blit(self.surface, (-camera_x, -camera_y))