"""Clase de la pala del jugador"""
import pygame
from settings import *


class Paddle:
    """Representa la pala controlada por el jugador"""
    
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = PADDLE_Y
        self.speed = PADDLE_SPEED
        self.color = PADDLE_COLOR
        
        # Estado de power-ups
        self.powerup_timer = 0
        self.original_width = PADDLE_WIDTH
        self.current_powerup = None
        
        # Interpolación suave
        self.target_x = self.x
        
    def update(self, delta_time, mouse_x=None, keys=None):
        """Actualiza la posición de la pala"""
        # Control por ratón
        if mouse_x is not None:
            self.target_x = mouse_x - self.width // 2
        
        # Control por teclado
        if keys:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.target_x -= self.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.target_x += self.speed
        
        # Limitar dentro de la pantalla
        self.target_x = max(0, min(self.target_x, WINDOW_WIDTH - self.width))
        
        # Interpolación suave
        self.x += (self.target_x - self.x) * 0.3
        
        # Actualizar timer de power-ups
        if self.powerup_timer > 0:
            self.powerup_timer -= delta_time
            if self.powerup_timer <= 0:
                self.reset_size()
    
    def apply_powerup(self, powerup_type):
        """Aplica un power-up a la pala"""
        if powerup_type == POWERUP_EXPAND:
            self.width = min(self.original_width * 1.5, WINDOW_WIDTH * 0.3)
            self.current_powerup = POWERUP_EXPAND
            self.powerup_timer = POWERUP_DURATION
        elif powerup_type == POWERUP_SHRINK:
            self.width = max(self.original_width * 0.6, 50)
            self.current_powerup = POWERUP_SHRINK
            self.powerup_timer = POWERUP_DURATION
    
    def reset_size(self):
        """Restaura el tamaño original de la pala"""
        self.width = self.original_width
        self.current_powerup = None
        self.powerup_timer = 0
    
    def draw(self, screen):
        """Dibuja la pala"""
        # Cuerpo principal
        rect = pygame.Rect(int(self.x), int(self.y), int(self.width), self.height)
        pygame.draw.rect(screen, self.color, rect, border_radius=5)
        
        # Borde brillante superior
        highlight = (min(self.color[0] + 50, 255), 
                    min(self.color[1] + 50, 255), 
                    min(self.color[2] + 50, 255))
        pygame.draw.rect(screen, highlight, 
                        (int(self.x), int(self.y), int(self.width), 3))
        
        # Sombra inferior
        shadow = (max(self.color[0] - 50, 0), 
                 max(self.color[1] - 50, 0), 
                 max(self.color[2] - 50, 0))
        pygame.draw.rect(screen, shadow,
                        (int(self.x), int(self.y) + self.height - 3, int(self.width), 3))
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(int(self.x), int(self.y), int(self.width), self.height)
    
    def reset(self):
        """Reinicia la pala a su estado inicial"""
        self.width = self.original_width
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.target_x = self.x
        self.powerup_timer = 0
        self.current_powerup = None