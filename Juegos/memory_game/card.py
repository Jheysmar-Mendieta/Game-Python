"""Clase para representar una carta del juego"""
import pygame
import math
from config import COLORS, FLIP_SPEED, CARD_BORDER_RADIUS, CARD_SHADOW_OFFSET


class Card:
    """Representa una carta del juego de memoria"""
    
    def __init__(self, x, y, width, height, image_id):
        self.rect = pygame.Rect(x, y, width, height)
        self.image_id = image_id
        self.is_flipped = False
        self.is_matched = False
        self.flip_progress = 0  # 0 = boca abajo, 1 = boca arriba
        self.target_flip = 0
        self.flash_timer = 0
        self.hover = False
        
    def start_flip(self, face_up):
        """Inicia animación de volteo"""
        self.target_flip = 1 if face_up else 0
        
    def update(self, dt):
        """Actualiza animación"""
        # Animación de flip
        if self.flip_progress != self.target_flip:
            direction = 1 if self.target_flip > self.flip_progress else -1
            self.flip_progress += direction * FLIP_SPEED * dt / 1000
            
            if direction > 0 and self.flip_progress >= self.target_flip:
                self.flip_progress = self.target_flip
                self.is_flipped = self.target_flip == 1
            elif direction < 0 and self.flip_progress <= self.target_flip:
                self.flip_progress = self.target_flip
                self.is_flipped = self.target_flip == 1
        
        # Timer de flash
        if self.flash_timer > 0:
            self.flash_timer -= dt
            
    def draw(self, surface, card_images):
        """Dibuja la carta con animación"""
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.x += CARD_SHADOW_OFFSET
        shadow_rect.y += CARD_SHADOW_OFFSET
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (*COLORS['shadow'][:3], 50), 
                        shadow_surface.get_rect(), border_radius=CARD_BORDER_RADIUS)
        surface.blit(shadow_surface, shadow_rect)
        
        # Calcular ancho según animación (efecto 3D)
        scale = abs(math.cos(self.flip_progress * math.pi))
        scaled_width = int(self.rect.width * scale)
        
        if scaled_width < 5:
            return
            
        # Determinar color/imagen
        if self.flip_progress < 0.5:
            # Mostrar reverso
            color = COLORS['hover'] if self.hover else COLORS['card_back']
            card_surface = pygame.Surface((scaled_width, self.rect.height))
            card_surface.fill(color)
            
            # Patrón decorativo
            for i in range(0, self.rect.height, 20):
                for j in range(0, scaled_width, 20):
                    pygame.draw.circle(card_surface, (*COLORS['text_light'], 30), 
                                     (j + 10, i + 10), 5)
        else:
            # Mostrar frente
            card_surface = pygame.Surface((scaled_width, self.rect.height))
            card_surface.fill(COLORS['card_front'])
            
            # Dibujar imagen
            if self.image_id < len(card_images):
                img = card_images[self.image_id]
                img_rect = img.get_rect(center=(scaled_width // 2, self.rect.height // 2))
                card_surface.blit(img, img_rect)
        
        # Efecto de flash cuando se empareja
        if self.flash_timer > 0:
            flash_surface = pygame.Surface((scaled_width, self.rect.height), pygame.SRCALPHA)
            alpha = int(128 * (self.flash_timer / 500))
            flash_surface.fill((*COLORS['success'], alpha))
            card_surface.blit(flash_surface, (0, 0))
        
        # Borde redondeado
        final_surface = pygame.Surface((scaled_width, self.rect.height), pygame.SRCALPHA)
        final_surface.blit(card_surface, (0, 0))
        
        # Borde
        border_color = COLORS['highlight'] if self.hover else COLORS['primary']
        pygame.draw.rect(final_surface, border_color, final_surface.get_rect(), 
                        width=3, border_radius=CARD_BORDER_RADIUS)
        
        # Posicionar centrado
        x_offset = (self.rect.width - scaled_width) // 2
        surface.blit(final_surface, (self.rect.x + x_offset, self.rect.y))
        
    def contains_point(self, pos):
        """Verifica si un punto está dentro de la carta"""
        return self.rect.collidepoint(pos)
    
    def set_matched(self, flash_duration):
        """Marca la carta como emparejada"""
        self.is_matched = True
        self.flash_timer = flash_duration