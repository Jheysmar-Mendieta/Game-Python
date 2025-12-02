"""Obstáculos del juego Dino"""
import pygame
import random
from settings import *
from sprites import SpriteGenerator


class Obstacle:
    """Representa un obstáculo (cactus)"""
    
    def __init__(self, x, obstacle_type='small'):
        self.type = obstacle_type
        
        if obstacle_type == 'small':
            self.sprite = SpriteGenerator.create_cactus_small()
            self.width = CACTUS_SMALL_WIDTH
            self.height = CACTUS_SMALL_HEIGHT
        else:
            self.sprite = SpriteGenerator.create_cactus_large()
            self.width = CACTUS_LARGE_WIDTH
            self.height = CACTUS_LARGE_HEIGHT
        
        self.x = x
        self.y = GROUND_Y - self.height
        
        # Rectángulo de colisión
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, speed):
        """Actualiza la posición del obstáculo"""
        self.x -= speed
        self.rect.x = int(self.x)
    
    def draw(self, screen, night_mode=False):
        """Dibuja el obstáculo"""
        if night_mode:
            # Recolorear para modo noche
            colored_sprite = self.sprite.copy()
            pixels = pygame.surfarray.pixels3d(colored_sprite)
            mask = (pixels[:, :, 0] == 83) & (pixels[:, :, 1] == 83) & (pixels[:, :, 2] == 83)
            pixels[mask] = [150, 150, 150]
            del pixels
            screen.blit(colored_sprite, (int(self.x), int(self.y)))
        else:
            screen.blit(self.sprite, (int(self.x), int(self.y)))
    
    def is_off_screen(self):
        """Verifica si el obstáculo está fuera de la pantalla"""
        return self.x < -self.width
    
    def get_collision_rect(self):
        """Retorna el rectángulo de colisión"""
        return self.rect


class ObstacleManager:
    """Maneja la generación y actualización de obstáculos"""
    
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.next_spawn_time = random.uniform(1.5, 2.5)
        self.speed = INITIAL_OBSTACLE_SPEED
    
    def update(self, delta_time):
        """Actualiza todos los obstáculos"""
        # Aumentar velocidad gradualmente
        self.speed += SPEED_INCREMENT
        
        # Mover obstáculos existentes
        for obstacle in self.obstacles:
            obstacle.update(self.speed)
        
        # Eliminar obstáculos fuera de pantalla
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]
        
        # Generar nuevos obstáculos
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.next_spawn_time:
            self.spawn_obstacle()
            self.spawn_timer = 0
            # Tiempo variable entre obstáculos
            distance = random.uniform(OBSTACLE_MIN_DISTANCE, OBSTACLE_MAX_DISTANCE)
            self.next_spawn_time = distance / self.speed / 60
    
    def spawn_obstacle(self):
        """Genera un nuevo obstáculo"""
        obstacle_type = random.choice(['small', 'small', 'large'])  # 2/3 pequeños, 1/3 grandes
        obstacle = Obstacle(WINDOW_WIDTH, obstacle_type)
        self.obstacles.append(obstacle)
    
    def draw(self, screen, night_mode=False):
        """Dibuja todos los obstáculos"""
        for obstacle in self.obstacles:
            obstacle.draw(screen, night_mode)
    
    def check_collision(self, player_rect):
        """Verifica colisión con el jugador"""
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_collision_rect()):
                return True
        return False
    
    def reset(self):
        """Reinicia el manager de obstáculos"""
        self.obstacles = []
        self.spawn_timer = 0
        self.next_spawn_time = random.uniform(1.5, 2.5)
        self.speed = INITIAL_OBSTACLE_SPEED