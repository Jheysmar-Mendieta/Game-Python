"""Componentes de interfaz de usuario"""
import pygame
from config import COLORS, CARD_BORDER_RADIUS


class Button:
    """Botón interactivo"""
    
    def __init__(self, x, y, width, height, text, color=None, text_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color or COLORS['primary']
        self.text_color = text_color or COLORS['text_light']
        self.hover = False
        self.active = True
        
    def update(self, mouse_pos):
        """Actualiza estado hover"""
        self.hover = self.rect.collidepoint(mouse_pos) if self.active else False
        
    def draw(self, surface, font):
        """Dibuja el botón"""
        color = tuple(min(c + 20, 255) for c in self.color[:3]) if self.hover else self.color
        
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, (*COLORS['shadow'][:3], 80), shadow_rect, 
                        border_radius=CARD_BORDER_RADIUS)
        
        # Botón
        pygame.draw.rect(surface, color, self.rect, border_radius=CARD_BORDER_RADIUS)
        
        # Borde
        if self.hover:
            pygame.draw.rect(surface, COLORS['highlight'], self.rect, 
                           width=3, border_radius=CARD_BORDER_RADIUS)
        
        # Texto
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, mouse_pos, mouse_pressed):
        """Verifica si el botón fue clickeado"""
        return self.active and self.hover and mouse_pressed


class Label:
    """Etiqueta de texto"""
    
    def __init__(self, x, y, text, font_size=24, color=None):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color or COLORS['text']
        
    def draw(self, surface, font):
        """Dibuja la etiqueta"""
        text_surf = font.render(str(self.text), True, self.color)
        text_rect = text_surf.get_rect(topleft=(self.x, self.y))
        surface.blit(text_surf, text_rect)
        
    def set_text(self, text):
        """Actualiza el texto"""
        self.text = text


class Panel:
    """Panel contenedor"""
    
    def __init__(self, x, y, width, height, color=None, alpha=255):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color or COLORS['card_front']
        self.alpha = alpha
        
    def draw(self, surface):
        """Dibuja el panel"""
        panel_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*self.color[:3], self.alpha), 
                        panel_surf.get_rect(), border_radius=15)
        
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (*COLORS['shadow'][:3], 60), 
                        shadow_surf.get_rect(), border_radius=15)
        surface.blit(shadow_surf, shadow_rect)
        
        surface.blit(panel_surf, self.rect)


class InputBox:
    """Caja de entrada de texto"""
    
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        """Maneja eventos de teclado y mouse"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 15:
                    self.text += event.unicode
        
        return False
        
    def update(self, dt):
        """Actualiza cursor parpadeante"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
    def draw(self, surface, font):
        """Dibuja la caja de texto"""
        # Fondo
        color = COLORS['card_front']
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        # Borde
        border_color = COLORS['primary'] if self.active else COLORS['text']
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)
        
        # Texto
        display_text = self.text if self.text else self.placeholder
        text_color = COLORS['text'] if self.text else (*COLORS['text'][:3], 128)
        text_surf = font.render(display_text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Cursor
        if self.active and self.cursor_visible and self.text:
            cursor_x = text_rect.right + 2
            pygame.draw.line(surface, COLORS['text'], 
                           (cursor_x, self.rect.y + 10), 
                           (cursor_x, self.rect.bottom - 10), 2)