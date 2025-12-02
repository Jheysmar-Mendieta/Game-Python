"""Sistema de partículas para efectos visuales"""
import pygame
import random
import math
from config import COLORS


class Particle:
    """Partícula individual"""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.life = 1.0
        self.size = random.randint(3, 8)
        self.color = color
        self.gravity = 0.2
        
    def update(self, dt):
        """Actualiza posición y vida"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= dt / 1000
        
    def draw(self, surface):
        """Dibuja la partícula"""
        if self.life > 0:
            alpha = int(255 * self.life)
            size = int(self.size * self.life)
            if size > 0:
                color = (*self.color[:3], alpha)
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)


class ParticleSystem:
    """Sistema de partículas"""
    
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, count=20, color=None):
        """Emite partículas desde una posición"""
        color = color or COLORS['success']
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
            
    def emit_burst(self, x, y, count=50):
        """Emite ráfaga de partículas (victoria)"""
        colors = [COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['highlight']]
        for _ in range(count):
            color = random.choice(colors)
            self.particles.append(Particle(x, y, color))
            
    def update(self, dt):
        """Actualiza todas las partículas"""
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update(dt)
            
    def draw(self, surface):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(surface)
            
    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()


class Star:
    """Estrella decorativa de fondo"""
    
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.randint(1, 3)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.5, 2.0)
        self.phase = random.uniform(0, math.pi * 2)
        
    def update(self, dt):
        """Actualiza brillo parpadeante"""
        self.phase += self.twinkle_speed * dt / 1000
        self.brightness = 0.5 + 0.5 * math.sin(self.phase)
        
    def draw(self, surface):
        """Dibuja la estrella"""
        alpha = int(255 * self.brightness * 0.4)
        color = (*COLORS['text_light'], alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class BackgroundStars:
    """Sistema de estrellas de fondo"""
    
    def __init__(self, screen_width, screen_height, count=30):
        self.stars = [Star(screen_width, screen_height) for _ in range(count)]
        
    def update(self, dt):
        """Actualiza todas las estrellas"""
        for star in self.stars:
            star.update(dt)
            
    def draw(self, surface):
        """Dibuja todas las estrellas"""
        for star in self.stars:
            star.draw(surface)