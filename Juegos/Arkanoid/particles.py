"""Sistema de partículas para efectos visuales"""
import pygame
import random
import math
from settings import *


class Particle:
    """Representa una partícula individual"""
    
    def __init__(self, x, y, color, velocity_x=None, velocity_y=None):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME
        
        # Velocidad aleatoria si no se especifica
        if velocity_x is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx = velocity_x
            self.vy = velocity_y
        
        # Tamaño
        self.size = random.randint(2, 5)
    
    def update(self, delta_time):
        """Actualiza la partícula"""
        self.x += self.vx
        self.y += self.vy
        
        # Aplicar gravedad suave
        self.vy += 0.2
        
        # Reducir velocidad
        self.vx *= 0.98
        self.vy *= 0.98
        
        # Reducir lifetime
        self.lifetime -= delta_time
    
    def draw(self, screen):
        """Dibuja la partícula"""
        if self.lifetime <= 0:
            return
        
        # Calcular alpha basado en lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color[:3], alpha)
        
        # Dibujar partícula
        pygame.draw.circle(screen, color[:3], (int(self.x), int(self.y)), self.size)
    
    def is_alive(self):
        """Verifica si la partícula sigue activa"""
        return self.lifetime > 0


class ParticleSystem:
    """Gestiona todas las partículas"""
    
    def __init__(self):
        self.particles = []
    
    def create_explosion(self, x, y, color, count=None):
        """Crea una explosión de partículas"""
        if count is None:
            count = PARTICLE_COUNT
        
        for _ in range(count):
            # Crear partículas en todas direcciones
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = Particle(x, y, color, vx, vy)
            self.particles.append(particle)
    
    def create_spark(self, x, y, color):
        """Crea una chispa (partícula única brillante)"""
        particle = Particle(x, y, (255, 255, 255))
        particle.size = 3
        particle.lifetime = 0.2
        self.particles.append(particle)
    
    def update(self, delta_time):
        """Actualiza todas las partículas"""
        for particle in self.particles:
            particle.update(delta_time)
        
        # Eliminar partículas muertas
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, screen):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Limpia todas las partículas"""
        self.particles = []