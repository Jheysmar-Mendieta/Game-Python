"""Clase de la pelota"""
import pygame
import math
import random
from settings import *


class Ball:
    """Representa una pelota en el juego"""
    
    def __init__(self, x, y, angle=None):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED_INITIAL
        
        # Dirección inicial aleatoria hacia arriba
        if angle is None:
            angle = random.uniform(-60, -120)
        self.angle = math.radians(angle)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        
        # Estado
        self.active = True
        self.piercing = False
        self.piercing_timer = 0
        
        # Trail effect
        self.trail_positions = []
        self.max_trail_length = 5
        
    def update(self, delta_time):
        """Actualiza la posición de la pelota"""
        if not self.active:
            return
        
        # Mover pelota
        self.x += self.vx
        self.y += self.vy
        
        # Guardar posición para trail
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # Rebotar en paredes laterales
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.radius
            self.vx = -abs(self.vx)
        
        # Rebotar en techo
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        
        # Actualizar timer de piercing
        if self.piercing_timer > 0:
            self.piercing_timer -= delta_time
            if self.piercing_timer <= 0:
                self.piercing = False
        
        # Límite de velocidad
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > BALL_MAX_SPEED:
            factor = BALL_MAX_SPEED / speed
            self.vx *= factor
            self.vy *= factor
    
    def bounce_paddle(self, paddle_rect):
        """Rebota en la pala con control de ángulo"""
        # Calcular punto de impacto relativo (-1 a 1)
        impact_point = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
        impact_point = max(-1, min(1, impact_point))
        
        # Ángulo de rebote basado en punto de impacto
        bounce_angle = impact_point * 60  # -60 a 60 grados
        bounce_angle_rad = math.radians(-90 + bounce_angle)
        
        # Aplicar nueva dirección
        speed = math.sqrt(self.vx**2 + self.vy**2)
        self.vx = math.cos(bounce_angle_rad) * speed
        self.vy = math.sin(bounce_angle_rad) * speed
        
        # Asegurar que va hacia arriba
        if self.vy > 0:
            self.vy = -self.vy
        
        # Colocar pelota sobre la pala
        self.y = paddle_rect.top - self.radius
    
    def bounce_brick(self, brick_rect, side='top'):
        """Rebota en un ladrillo"""
        if side in ['top', 'bottom']:
            self.vy = -self.vy
        else:
            self.vx = -self.vx
    
    def increase_speed(self):
        """Aumenta la velocidad de la pelota"""
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed < BALL_MAX_SPEED:
            factor = (speed + BALL_SPEED_INCREMENT) / speed
            self.vx *= factor
            self.vy *= factor
    
    def apply_powerup(self, powerup_type):
        """Aplica un power-up a la pelota"""
        if powerup_type == POWERUP_SLOW:
            speed = math.sqrt(self.vx**2 + self.vy**2)
            factor = max(0.7, BALL_SPEED_INITIAL / speed)
            self.vx *= factor
            self.vy *= factor
        elif powerup_type == POWERUP_FAST:
            speed = math.sqrt(self.vx**2 + self.vy**2)
            factor = min(1.3, BALL_MAX_SPEED / speed)
            self.vx *= factor
            self.vy *= factor
        elif powerup_type == POWERUP_PIERCE:
            self.piercing = True
            self.piercing_timer = POWERUP_DURATION
    
    def draw(self, screen):
        """Dibuja la pelota con efectos"""
        if not self.active:
            return
        
        # Dibujar trail
        for i, (tx, ty) in enumerate(self.trail_positions[:-1]):
            alpha = int(255 * (i / len(self.trail_positions)))
            radius = int(self.radius * (i / len(self.trail_positions)))
            if radius > 0:
                color = (255, 255, 255, alpha) if not self.piercing else (255, 100, 100, alpha)
                pygame.draw.circle(screen, color[:3], (int(tx), int(ty)), radius)
        
        # Dibujar pelota
        if self.piercing:
            # Efecto de brillo para piercing
            pygame.draw.circle(screen, (255, 150, 150), 
                             (int(self.x), int(self.y)), self.radius + 2)
        
        pygame.draw.circle(screen, BALL_COLOR, 
                         (int(self.x), int(self.y)), self.radius)
        
        # Brillo central
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(self.x - 2), int(self.y - 2)), self.radius // 3)
    
    def is_below_screen(self):
        """Verifica si la pelota cayó por debajo de la pantalla"""
        return self.y - self.radius > WINDOW_HEIGHT
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                          self.radius * 2, self.radius * 2)