"""Clase de ladrillos"""
import pygame
from settings import *


class Brick:
    """Representa un ladrillo"""
    
    def __init__(self, x, y, brick_type, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.type = brick_type
        self.original_type = brick_type
        self.color = color
        self.original_color = color
        self.destroyed = False
        
    def hit(self):
        """Golpea el ladrillo"""
        if self.type == BRICK_INDESTRUCTIBLE:
            return False
        
        self.type -= 1
        
        # Cambiar color según resistencia
        if self.type > 0:
            factor = self.type / self.original_type
            self.color = tuple(int(c * factor) for c in self.original_color)
            return False
        else:
            self.destroyed = True
            return True
    
    def draw(self, screen):
        """Dibuja el ladrillo"""
        if self.destroyed:
            return
        
        rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        
        # Dibujar ladrillo según tipo
        if self.type == BRICK_INDESTRUCTIBLE:
            # Patrón especial para indestructibles
            pygame.draw.rect(screen, (80, 80, 80), rect, border_radius=3)
            pygame.draw.rect(screen, (120, 120, 120), rect, 2, border_radius=3)
            
            # Patrón de rayas
            for i in range(0, self.width, 8):
                pygame.draw.line(screen, (100, 100, 100),
                               (int(self.x) + i, int(self.y)),
                               (int(self.x) + i, int(self.y) + self.height))
        else:
            # Ladrillo normal con gradiente
            pygame.draw.rect(screen, self.color, rect, border_radius=3)
            
            # Borde brillante superior
            highlight = tuple(min(c + 40, 255) for c in self.color)
            pygame.draw.line(screen, highlight,
                           (int(self.x) + 2, int(self.y) + 2),
                           (int(self.x) + self.width - 2, int(self.y) + 2), 2)
            
            # Sombra inferior
            shadow = tuple(max(c - 40, 0) for c in self.color)
            pygame.draw.line(screen, shadow,
                           (int(self.x) + 2, int(self.y) + self.height - 2),
                           (int(self.x) + self.width - 2, int(self.y) + self.height - 2), 2)
            
            # Borde
            pygame.draw.rect(screen, shadow, rect, 1, border_radius=3)
            
            # Indicador de resistencia
            if self.type > 1:
                font = pygame.font.Font(FONT_NAME, 12)
                text = font.render(str(self.type), True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def get_collision_side(self, ball_rect, ball_vx, ball_vy):
        """Determina el lado de colisión con la pelota"""
        brick_rect = self.get_rect()
        
        # Calcular penetración en cada dirección
        dx = ball_rect.centerx - brick_rect.centerx
        dy = ball_rect.centery - brick_rect.centery
        
        # Determinar lado basado en dirección de movimiento y penetración
        if abs(dx) > abs(dy):
            return 'left' if dx < 0 else 'right'
        else:
            return 'top' if dy < 0 else 'bottom'