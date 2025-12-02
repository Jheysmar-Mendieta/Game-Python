"""Sistema de power-ups"""
import pygame
import random
from settings import *


class PowerUp:
    """Representa un power-up que cae"""
    
    # Configuración visual de cada power-up
    POWERUP_CONFIG = {
        POWERUP_EXPAND: {'color': (100, 255, 100), 'symbol': '↔'},
        POWERUP_SHRINK: {'color': (255, 100, 100), 'symbol': '→←'},
        POWERUP_MULTIBALL: {'color': (255, 255, 100), 'symbol': '●●'},
        POWERUP_SLOW: {'color': (100, 200, 255), 'symbol': '↓'},
        POWERUP_FAST: {'color': (255, 150, 50), 'symbol': '↑'},
        POWERUP_PIERCE: {'color': (255, 100, 255), 'symbol': '⚡'},
        POWERUP_LIFE: {'color': (255, 50, 50), 'symbol': '♥'},
    }
    
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.width = POWERUP_SIZE
        self.height = POWERUP_SIZE
        self.type = powerup_type
        self.speed = POWERUP_FALL_SPEED
        self.active = True
        
        # Configuración visual
        config = self.POWERUP_CONFIG.get(powerup_type, {'color': (255, 255, 255), 'symbol': '?'})
        self.color = config['color']
        self.symbol = config['symbol']
        
        # Animación
        self.rotation = 0
        self.pulse = 0
    
    def update(self, delta_time):
        """Actualiza la posición del power-up"""
        if not self.active:
            return
        
        self.y += self.speed
        
        # Animaciones
        self.rotation += 2
        self.pulse += delta_time * 5
        
        # Desactivar si sale de la pantalla
        if self.y > WINDOW_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        """Dibuja el power-up"""
        if not self.active:
            return
        
        # Efecto de pulso
        size_mod = int(2 * abs(pygame.math.Vector2(0, self.pulse).length() % 1 - 0.5))
        size = self.width + size_mod
        
        # Rectángulo principal
        rect = pygame.Rect(
            int(self.x - size // 2),
            int(self.y - size // 2),
            size,
            size
        )
        
        # Sombra
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=5)
        
        # Fondo
        pygame.draw.rect(screen, self.color, rect, border_radius=5)
        
        # Brillo
        highlight = tuple(min(c + 50, 255) for c in self.color)
        pygame.draw.rect(screen, highlight, 
                        (rect.x, rect.y, rect.width, rect.height // 3),
                        border_radius=5)
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)
        
        # Símbolo
        font = pygame.font.Font(FONT_NAME, 18)
        text = font.render(self.symbol, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )


class PowerUpManager:
    """Gestiona todos los power-ups activos"""
    
    def __init__(self):
        self.powerups = []
        
        # Probabilidades de cada power-up
        self.powerup_weights = {
            POWERUP_EXPAND: 25,
            POWERUP_SHRINK: 10,
            POWERUP_MULTIBALL: 20,
            POWERUP_SLOW: 15,
            POWERUP_FAST: 10,
            POWERUP_PIERCE: 15,
            POWERUP_LIFE: 5,
        }
    
    def spawn_powerup(self, x, y):
        """Genera un power-up aleatorio en la posición especificada"""
        if random.random() < POWERUP_PROBABILITY:
            # Seleccionar tipo de power-up basado en pesos
            types = list(self.powerup_weights.keys())
            weights = list(self.powerup_weights.values())
            powerup_type = random.choices(types, weights=weights)[0]
            
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.append(powerup)
            return True
        return False
    
    def update(self, delta_time):
        """Actualiza todos los power-ups"""
        for powerup in self.powerups:
            powerup.update(delta_time)
        
        # Eliminar power-ups inactivos
        self.powerups = [p for p in self.powerups if p.active]
    
    def draw(self, screen):
        """Dibuja todos los power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen)
    
    def check_collision(self, paddle_rect):
        """Verifica colisión con la pala y retorna power-ups recolectados"""
        collected = []
        for powerup in self.powerups:
            if powerup.active and paddle_rect.colliderect(powerup.get_rect()):
                collected.append(powerup.type)
                powerup.active = False
        
        return collected
    
    def clear(self):
        """Limpia todos los power-ups"""
        self.powerups = []