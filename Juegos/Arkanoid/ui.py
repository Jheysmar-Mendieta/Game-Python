"""Interfaz de usuario para Arkanoid"""
import pygame
from settings import *


class Button:
    """Clase para botones interactivos"""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
    
    def update(self, mouse_pos):
        """Actualiza el estado del botón"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
    
    def draw(self, screen, font):
        """Dibuja el botón"""
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        # Botón
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3, border_radius=10)
        
        # Texto
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        """Verifica si fue clickeado"""
        return self.is_hovered and mouse_pressed


class UI:
    """Maneja toda la interfaz de usuario"""
    
    def __init__(self):
        # Fuentes
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_small = pygame.font.Font(FONT_NAME, 18)
        self.title_font = pygame.font.Font(FONT_NAME, FONT_TITLE)
        self.button_font = pygame.font.Font(FONT_NAME, 28)
        
        # Botones del menú principal
        button_width = 250
        button_height = 60
        button_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 220
        spacing = 75
        
        self.menu_buttons = {
            'play': Button(button_x, start_y, button_width, button_height,
                          'JUGAR', (100, 150, 255), (120, 170, 255)),
            'levels': Button(button_x, start_y + spacing, button_width, button_height,
                           'NIVELES', (100, 150, 255), (120, 170, 255)),
            'records': Button(button_x, start_y + spacing * 2, button_width, button_height,
                            'RÉCORDS', (100, 150, 255), (120, 170, 255)),
            'exit': Button(button_x, start_y + spacing * 3, button_width, button_height,
                          'SALIR', (255, 100, 100), (255, 120, 120))
        }
        
        # Botones de pausa
        self.pause_buttons = {
            'continue': Button(button_x, 200, button_width, button_height,
                             'CONTINUAR', (100, 255, 100), (120, 255, 120)),
            'restart': Button(button_x, 280, button_width, button_height,
                            'REINICIAR', (255, 200, 100), (255, 220, 120)),
            'menu': Button(button_x, 360, button_width, button_height,
                         'MENÚ', (255, 100, 100), (255, 120, 120))
        }
        
        # Botones de game over
        self.gameover_buttons = {
            'retry': Button(button_x, 350, button_width, button_height,
                          'REINTENTAR', (100, 255, 100), (120, 255, 120)),
            'menu': Button(button_x, 430, button_width, button_height,
                         'MENÚ', (255, 100, 100), (255, 120, 120))
        }
        
        # Botones de victoria
        self.victory_buttons = {
            'next': Button(button_x, 350, button_width, button_height,
                         'SIGUIENTE', (100, 255, 100), (120, 255, 120)),
            'menu': Button(button_x, 430, button_width, button_height,
                         'MENÚ', (255, 100, 100), (255, 120, 120))
        }
        
        # Botón de volver (récords/niveles)
        self.back_button = Button(button_x, 500, button_width, button_height,
                                 'VOLVER', (100, 150, 255), (120, 170, 255))
    
    def draw_hud(self, screen, score, lives, level, powerups_active):
        """Dibuja el HUD durante el juego"""
        # Puntuación
        score_text = self.font.render(f"PUNTOS: {score}", True, COLOR_WHITE)
        screen.blit(score_text, (20, 20))
        
        # Vidas
        lives_text = self.font.render(f"VIDAS: {lives}", True, COLOR_WHITE)
        screen.blit(lives_text, (20, 50))
        
        # Nivel
        level_text = self.font.render(f"NIVEL: {level + 1}", True, COLOR_WHITE)
        level_rect = level_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
        screen.blit(level_text, level_rect)
        
        # Power-ups activos
        if powerups_active:
            y_offset = 50
            for powerup in powerups_active:
                powerup_text = self.font_small.render(f"• {powerup}", True, COLOR_YELLOW)
                powerup_rect = powerup_text.get_rect(topright=(WINDOW_WIDTH - 20, y_offset))
                screen.blit(powerup_text, powerup_rect)
                y_offset += 25
    
    def draw_main_menu(self, screen, mouse_pos):
        """Dibuja el menú principal"""
        screen.fill(COLOR_BG)
        
        # Título con efecto de brillo
        title = self.title_font.render("ARKANOID", True, (100, 200, 255))
        title_shadow = self.title_font.render("ARKANOID", True, (50, 100, 150))
        
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font.render("Rompe todos los ladrillos", True, COLOR_WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 170))
        screen.blit(subtitle, subtitle_rect)
        
        # Botones
        for button in self.menu_buttons.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_pause_menu(self, screen, mouse_pos):
        """Dibuja el menú de pausa"""
        # Overlay semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("PAUSA", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        screen.blit(title, title_rect)
        
        # Botones
        for button in self.pause_buttons.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_game_over(self, screen, score, best_score, is_record, mouse_pos):
        """Dibuja la pantalla de game over"""
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("GAME OVER", True, COLOR_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Puntuación
        score_text = self.button_font.render(f"Puntuación: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 230))
        screen.blit(score_text, score_rect)
        
        # Mejor puntuación
        best_text = self.font.render(f"Mejor: {best_score}", True, COLOR_WHITE)
        best_rect = best_text.get_rect(center=(WINDOW_WIDTH // 2, 280))
        screen.blit(best_text, best_rect)
        
        # Nuevo récord
        if is_record:
            record_text = self.button_font.render("¡NUEVO RÉCORD!", True, COLOR_YELLOW)
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, 260))
            screen.blit(record_text, record_rect)
        
        # Botones
        for button in self.gameover_buttons.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_victory(self, screen, score, level_name, mouse_pos, has_next_level):
        """Dibuja la pantalla de victoria"""
        # Overlay dorado
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 20))
        screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("¡NIVEL COMPLETADO!", True, COLOR_YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Nombre del nivel
        level_text = self.button_font.render(level_name, True, COLOR_WHITE)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
        screen.blit(level_text, level_rect)
        
        # Puntuación
        score_text = self.button_font.render(f"Puntos: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 280))
        screen.blit(score_text, score_rect)
        
        # Botones
        buttons_to_show = self.victory_buttons if has_next_level else {'menu': self.victory_buttons['menu']}
        for button in buttons_to_show.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_level_select(self, screen, level_manager, mouse_pos):
        """Dibuja la selección de niveles"""
        screen.fill(COLOR_BG)
        
        # Título
        title = self.title_font.render("SELECCIONAR NIVEL", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Grid de niveles
        levels_per_row = 3
        level_count = level_manager.get_level_count()
        
        for i in range(level_count):
            row = i // levels_per_row
            col = i % levels_per_row
            
            x = 150 + col * 200
            y = 150 + row * 150
            
            # Rectángulo del nivel
            rect = pygame.Rect(x, y, 150, 100)
            
            # Color según dificultad
            level_info = level_manager.get_level_info(i)
            if level_info['difficulty'] == 'Fácil':
                color = (100, 255, 100)
            elif level_info['difficulty'] == 'Media':
                color = (255, 200, 100)
            else:
                color = (255, 100, 100)
            
            # Hover effect
            if rect.collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)
            
            # Número de nivel
            level_text = self.button_font.render(str(i + 1), True, (255, 255, 255))
            level_text_rect = level_text.get_rect(center=(rect.centerx, rect.centery - 15))
            screen.blit(level_text, level_text_rect)
            
            # Nombre del nivel
            name_text = self.font_small.render(level_info['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(rect.centerx, rect.centery + 15))
            screen.blit(name_text, name_rect)
        
        # Botón volver
        self.back_button.update(mouse_pos)
        self.back_button.draw(screen, self.button_font)
    
    def draw_records(self, screen, records, mouse_pos):
        """Dibuja la pantalla de récords"""
        screen.fill(COLOR_BG)
        
        # Título
        title = self.button_font.render("MEJORES PUNTUACIONES", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Lista de récords
        y_offset = 120
        if records:
            for i, (username, score, date) in enumerate(records[:10], 1):
                # Posición
                pos_text = self.font.render(f"{i}.", True, COLOR_WHITE)
                screen.blit(pos_text, (150, y_offset))
                
                # Nombre
                name_text = self.font.render(username, True, COLOR_WHITE)
                screen.blit(name_text, (200, y_offset))
                
                # Puntuación
                score_text = self.font.render(str(score), True, COLOR_YELLOW)
                screen.blit(score_text, (550, y_offset))
                
                y_offset += 40
        else:
            no_records = self.font.render("No hay récords aún", True, COLOR_WHITE)
            no_rect = no_records.get_rect(center=(WINDOW_WIDTH // 2, 250))
            screen.blit(no_records, no_rect)
        
        # Botón volver
        self.back_button.update(mouse_pos)
        self.back_button.draw(screen, self.button_font)