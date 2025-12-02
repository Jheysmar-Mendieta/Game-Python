"""Elementos del fondo: piso, nubes y estrellas"""
import pygame
import random
from settings import *
from sprites import SpriteGenerator


class Ground:
    """Representa el piso que se desplaza"""
    
    def __init__(self):
        self.x1 = 0
        self.x2 = WINDOW_WIDTH
        self.y = GROUND_Y
        self.speed = INITIAL_OBSTACLE_SPEED
        
        # Crear patrón del piso
        self.tile_width = 20
        self.create_ground_pattern()
    
    def create_ground_pattern(self):
        """Crea el patrón visual del piso"""
        self.pattern = pygame.Surface((self.tile_width, GROUND_HEIGHT))
        self.pattern.fill(COLOR_DAY_GROUND)
        
        # Agregar algunos píxeles aleatorios para textura
        for _ in range(5):
            x = random.randint(0, self.tile_width - 1)
            y = random.randint(0, GROUND_HEIGHT - 1)
            pygame.draw.rect(self.pattern, (100, 100, 100), (x, y, 1, 1))
    
    def update(self, speed):
        """Actualiza la posición del piso"""
        self.speed = speed
        self.x1 -= self.speed
        self.x2 -= self.speed
        
        # Resetear posición cuando sale de pantalla
        if self.x1 <= -WINDOW_WIDTH:
            self.x1 = self.x2 + WINDOW_WIDTH
        if self.x2 <= -WINDOW_WIDTH:
            self.x2 = self.x1 + WINDOW_WIDTH
    
    def draw(self, screen, night_mode=False):
        """Dibuja el piso"""
        color = COLOR_NIGHT_GROUND if night_mode else COLOR_DAY_GROUND
        
        # Dibujar línea del piso
        pygame.draw.line(screen, color, (0, self.y), (WINDOW_WIDTH, self.y), 2)
        
        # Dibujar patrón de tiles
        x_offset = int(self.x1) % self.tile_width
        for x in range(-self.tile_width, WINDOW_WIDTH + self.tile_width, self.tile_width):
            # Dibujar pequeños segmentos en el piso
            if random.random() > 0.7:
                segment_x = x + x_offset
                pygame.draw.line(screen, color, 
                               (segment_x, self.y + 2), 
                               (segment_x + 3, self.y + 2), 2)
    
    def reset(self):
        """Reinicia el piso"""
        self.x1 = 0
        self.x2 = WINDOW_WIDTH
        self.speed = INITIAL_OBSTACLE_SPEED


class Cloud:
    """Representa una nube o estrella"""
    
    def __init__(self, x=None, is_star=False):
        self.is_star = is_star
        
        if is_star:
            self.sprite = SpriteGenerator.create_star()
            self.width = 4
            self.height = 4
        else:
            self.sprite = SpriteGenerator.create_cloud()
            self.width = CLOUD_WIDTH
            self.height = CLOUD_HEIGHT
        
        self.x = x if x is not None else WINDOW_WIDTH + random.randint(0, 300)
        self.y = random.randint(CLOUD_MIN_Y, CLOUD_MAX_Y)
        self.speed = CLOUD_SPEED
    
    def update(self):
        """Actualiza la posición de la nube/estrella"""
        self.x -= self.speed
    
    def draw(self, screen):
        """Dibuja la nube/estrella"""
        screen.blit(self.sprite, (int(self.x), int(self.y)))
    
    def is_off_screen(self):
        """Verifica si está fuera de la pantalla"""
        return self.x < -self.width


class CloudManager:
    """Maneja las nubes y estrellas del fondo"""
    
    def __init__(self):
        self.clouds = []
        self.spawn_timer = 0
        self.spawn_interval = random.uniform(2, 4)
        
        # Generar algunas nubes iniciales
        for i in range(3):
            cloud = Cloud(x=random.randint(100, WINDOW_WIDTH - 100))
            self.clouds.append(cloud)
    
    def update(self, delta_time, night_mode=False):
        """Actualiza todas las nubes/estrellas"""
        # Mover nubes existentes
        for cloud in self.clouds:
            cloud.update()
        
        # Eliminar nubes fuera de pantalla
        self.clouds = [cloud for cloud in self.clouds if not cloud.is_off_screen()]
        
        # Generar nuevas nubes/estrellas
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            cloud = Cloud(is_star=night_mode)
            self.clouds.append(cloud)
            self.spawn_timer = 0
            self.spawn_interval = random.uniform(2, 4)
    
    def draw(self, screen):
        """Dibuja todas las nubes/estrellas"""
        for cloud in self.clouds:
            cloud.draw(screen)
    
    def switch_mode(self, night_mode):
        """Cambia entre nubes y estrellas"""
        # Limpiar nubes existentes y crear nuevas del tipo correcto
        self.clouds = []
        for i in range(3):
            cloud = Cloud(x=random.randint(100, WINDOW_WIDTH - 100), is_star=night_mode)
            self.clouds.append(cloud)
    
    def reset(self):
        """Reinicia el manager de nubes"""
        self.clouds = []
        self.spawn_timer = 0
        self.spawn_interval = random.uniform(2, 4)
        
        # Generar algunas nubes iniciales
        for i in range(3):
            cloud = Cloud(x=random.randint(100, WINDOW_WIDTH - 100))
            self.clouds.append(cloud)