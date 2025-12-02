"""Sistema de partículas para efectos visuales"""
import pygame
import random
import math
from config import *


class Particle:
    """Partícula individual"""
    
    def __init__(self, x, y, vx, vy, color, lifetime, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        
    def update(self, dt):
        """Actualiza la partícula"""
        self.x += self.vx * dt / 16
        self.y += self.vy * dt / 16
        self.lifetime -= dt / 1000
        
        # Fricción
        self.vx *= 0.98
        self.vy *= 0.98
        
    def draw(self, surface, camera_x, camera_y):
        """Dibuja la partícula"""
        if self.lifetime <= 0:
            return
            
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Fade out
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))
        
        size = int(self.size * (self.lifetime / self.max_lifetime))
        size = max(1, size)
        
        color = (*self.color[:3], alpha)
        
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (size, size), size)
        surface.blit(s, (screen_x - size, screen_y - size))


class ParticleSystem:
    """Sistema de gestión de partículas"""
    
    def __init__(self):
        self.particles = []
        
    def emit_smoke(self, x, y, angle, speed):
        """Emite humo de derrape"""
        angle_rad = math.radians(angle + random.uniform(-20, 20))
        
        for _ in range(2):
            vx = -math.sin(angle_rad) * speed * 0.3 + random.uniform(-1, 1)
            vy = math.cos(angle_rad) * speed * 0.3 + random.uniform(-1, 1)
            
            # Humo gris
            gray = random.randint(80, 120)
            color = (gray, gray, gray)
            
            particle = Particle(
                x + random.uniform(-10, 10),
                y + random.uniform(-10, 10),
                vx, vy,
                color,
                lifetime=0.5 + random.random() * 0.5,
                size=random.randint(4, 8)
            )
            
            self.particles.append(particle)
            
    def emit_sparks(self, x, y):
        """Emite chispas de colisión"""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice([
                (255, 200, 50),  # Amarillo
                (255, 150, 50),  # Naranja
                (255, 100, 50),  # Naranja rojizo
            ])
            
            particle = Particle(
                x, y, vx, vy,
                color,
                lifetime=0.3 + random.random() * 0.2,
                size=random.randint(2, 4)
            )
            
            self.particles.append(particle)
            
    def emit_dust(self, x, y):
        """Emite polvo al estar fuera de pista"""
        for _ in range(1):
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0.5)
            
            # Color tierra
            brown = random.randint(100, 150)
            color = (brown, brown - 20, brown - 40)
            
            particle = Particle(
                x + random.uniform(-15, 15),
                y + random.uniform(-15, 15),
                vx, vy,
                color,
                lifetime=0.4 + random.random() * 0.3,
                size=random.randint(3, 6)
            )
            
            self.particles.append(particle)
            
    def update(self, dt):
        """Actualiza todas las partículas"""
        # Actualizar partículas
        for particle in self.particles:
            particle.update(dt)
            
        # Eliminar partículas muertas
        self.particles = [p for p in self.particles if p.lifetime > 0]
        
    def draw(self, surface, camera_x, camera_y):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(surface, camera_x, camera_y)
            
    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()