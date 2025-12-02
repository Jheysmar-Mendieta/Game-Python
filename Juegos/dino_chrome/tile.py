"""Clase para representar una ficha del juego 2048"""
import pygame
from settings import *
from colors import get_tile_color, get_text_color


class Tile:
    """Representa una ficha en el tablero de 2048"""
    
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = self._get_x()
        self.y = self._get_y()
        self.target_x = self.x
        self.target_y = self.y
        self.merged = False
        self.is_new = True
        self.scale = 0.0 if value > 0 else 1.0
        self.merge_scale = 1.0
    
    def _get_x(self):
        """Calcula la posición X en píxeles"""
        return BOARD_X + CELL_PADDING + self.col * (CELL_SIZE + CELL_PADDING)
    
    def _get_y(self):
        """Calcula la posición Y en píxeles"""
        return BOARD_Y + CELL_PADDING + self.row * (CELL_SIZE + CELL_PADDING)
    
    def update_position(self, row, col):
        """Actualiza la posición objetivo de la ficha"""
        self.row = row
        self.col = col
        self.target_x = self._get_x()
        self.target_y = self._get_y()
    
    def animate_movement(self, delta_time):
        """Anima el movimiento de la ficha"""
        speed = 1000 * delta_time  # píxeles por segundo
        
        if abs(self.x - self.target_x) > 1:
            if self.x < self.target_x:
                self.x = min(self.x + speed, self.target_x)
            else:
                self.x = max(self.x - speed, self.target_x)
        else:
            self.x = self.target_x
        
        if abs(self.y - self.target_y) > 1:
            if self.y < self.target_y:
                self.y = min(self.y + speed, self.target_y)
            else:
                self.y = max(self.y - speed, self.target_y)
        else:
            self.y = self.target_y
    
    def animate_spawn(self, delta_time):
        """Anima la aparición de una nueva ficha"""
        if self.is_new and self.scale < 1.0:
            self.scale += delta_time / SPAWN_ANIMATION_SPEED
            if self.scale >= 1.0:
                self.scale = 1.0
                self.is_new = False
    
    def animate_merge(self, delta_time):
        """Anima la fusión de fichas"""
        if self.merged:
            # Efecto de "pop": crece y vuelve al tamaño normal
            self.merge_scale += delta_time / MERGE_ANIMATION_SPEED * 3
            if self.merge_scale >= 1.2:
                self.merge_scale = 1.2
                self.merged = False
        elif self.merge_scale > 1.0:
            self.merge_scale -= delta_time / MERGE_ANIMATION_SPEED * 3
            if self.merge_scale <= 1.0:
                self.merge_scale = 1.0
    
    def is_animating(self):
        """Verifica si la ficha está en animación"""
        return (self.x != self.target_x or 
                self.y != self.target_y or 
                self.is_new or 
                self.merged or 
                self.merge_scale != 1.0)
    
    def draw(self, screen, font):
        """Dibuja la ficha en la pantalla"""
        if self.value == 0:
            return
        
        # Calcular el tamaño con la escala aplicada
        current_scale = self.scale * self.merge_scale
        scaled_size = int(CELL_SIZE * current_scale)
        offset = (CELL_SIZE - scaled_size) // 2
        
        # Crear superficie con transparencia para bordes redondeados
        tile_surface = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
        
        # Dibujar fondo con bordes redondeados
        bg_color = get_tile_color(self.value)
        pygame.draw.rect(
            tile_surface, 
            bg_color, 
            (0, 0, scaled_size, scaled_size), 
            border_radius=8
        )
        
        # Dibujar sombra sutil
        shadow_surface = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (*bg_color, 50),
            (2, 2, scaled_size, scaled_size),
            border_radius=8
        )
        screen.blit(shadow_surface, (int(self.x) + offset, int(self.y) + offset))
        
        # Dibujar la ficha
        screen.blit(tile_surface, (int(self.x) + offset, int(self.y) + offset))
        
        # Dibujar el número
        text_color = get_text_color(self.value)
        font_size = CELL_FONT_SIZE if self.value < 100 else (CELL_FONT_SIZE - 10 if self.value < 1000 else CELL_FONT_SIZE - 15)
        number_font = pygame.font.Font(FONT_NAME, int(font_size * current_scale))
        text = number_font.render(str(self.value), True, text_color)
        text_rect = text.get_rect(center=(
            int(self.x) + CELL_SIZE // 2,
            int(self.y) + CELL_SIZE // 2
        ))
        screen.blit(text, text_rect)