"""Interfaz de usuario para el juego Dino"""
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
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 3, border_radius=8)
        
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
        self.title_font = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        self.button_font = pygame.font.Font(FONT_NAME, 28)
        
        # Botones del menú principal
        button_width = 250
        button_height = 60
        button_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 200
        spacing = 80
        
        self.menu_buttons = {
            'play': Button(button_x, start_y, button_width, button_height,
                          'JUGAR', (83, 83, 83), (100, 100, 100)),
            'records': Button(button_x, start_y + spacing, button_width, button_height,
                            'RÉCORDS', (83, 83, 83), (100, 100, 100)),
            'exit': Button(button_x, start_y + spacing * 2, button_width, button_height,
                          'SALIR', (83, 83, 83), (100, 100, 100))
        }
        
        # Botones de game over
        self.gameover_buttons = {
            'retry': Button(button_x, 250, button_width, button_height,
                          'REINTENTAR', (83, 83, 83), (100, 100, 100)),
            'menu': Button(button_x, 330, button_width, button_height,
                         'MENÚ', (83, 83, 83), (100, 100, 100))
        }
        
        # Botón de récords
        self.records_buttons = {
            'back': Button(button_x, 330, button_width, button_height,
                         'VOLVER', (83, 83, 83), (100, 100, 100))
        }
        
        # Animación de parpadeo
        self.blink_timer = 0
        self.blink_visible = True
    
    def draw_score(self, screen, score, best_score, night_mode=False):
        """Dibuja la puntuación"""
        color = COLOR_NIGHT_GROUND if night_mode else COLOR_TEXT
        
        # Formatear puntuación con ceros a la izquierda
        score_text = f"HI {int(best_score):05d}  {int(score):05d}"
        text_surf = self.font.render(score_text, True, color)
        screen.blit(text_surf, (WINDOW_WIDTH - 250, 20))
    
    def draw_main_menu(self, screen, mouse_pos):
        """Dibuja el menú principal"""
        screen.fill(COLOR_DAY_BG)
        
        # Título
        title = self.title_font.render("DINO CHROME", True, (83, 83, 83))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Dibujar un pequeño dino decorativo
        from sprites import SpriteGenerator
        dino = SpriteGenerator.create_dino_run1()
        dino_rect = dino.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(dino, dino_rect)
        
        # Botones
        for button in self.menu_buttons.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_game_over(self, screen, score, best_score, is_record, mouse_pos, 
                       delta_time, night_mode=False):
        """Dibuja el overlay de game over"""
        bg_color = COLOR_NIGHT_BG if night_mode else COLOR_DAY_BG
        text_color = COLOR_NIGHT_GROUND if night_mode else COLOR_TEXT
        
        # Actualizar parpadeo
        self.blink_timer += delta_time
        if self.blink_timer >= 0.5:
            self.blink_timer = 0
            self.blink_visible = not self.blink_visible
        
        # Texto "GAME OVER" parpadeante
        if self.blink_visible:
            game_over_text = self.title_font.render("GAME OVER", True, text_color)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
            screen.blit(game_over_text, text_rect)
        
        # Puntuación
        score_text = self.button_font.render(f"Puntaje: {int(score)}", True, text_color)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 170))
        screen.blit(score_text, score_rect)
        
        # Mejor puntaje
        best_text = self.font.render(f"Mejor: {int(best_score)}", True, text_color)
        best_rect = best_text.get_rect(center=(WINDOW_WIDTH // 2, 210))
        screen.blit(best_text, best_rect)
        
        # Nuevo récord
        if is_record:
            record_text = self.button_font.render("¡NUEVO RÉCORD!", True, (255, 100, 100))
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
            
            # Efecto de sombra
            shadow_surf = self.button_font.render("¡NUEVO RÉCORD!", True, (100, 30, 30))
            shadow_rect = shadow_surf.get_rect(center=(WINDOW_WIDTH // 2 + 2, 182))
            screen.blit(shadow_surf, shadow_rect)
            screen.blit(record_text, record_rect)
        
        # Botones
        for button in self.gameover_buttons.values():
            button.update(mouse_pos)
            button.draw(screen, self.button_font)
    
    def draw_records(self, screen, records, mouse_pos):
        """Dibuja la pantalla de récords"""
        screen.fill(COLOR_DAY_BG)
        
        # Título
        title = self.button_font.render("MEJORES PUNTUACIONES", True, (83, 83, 83))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
        screen.blit(title, title_rect)
        
        # Lista de récords
        y_offset = 100
        if records:
            for i, (username, score, date) in enumerate(records[:10], 1):
                # Posición
                pos_text = self.font.render(f"{i}.", True, (83, 83, 83))
                screen.blit(pos_text, (150, y_offset))
                
                # Nombre
                name_text = self.font.render(username, True, (83, 83, 83))
                screen.blit(name_text, (200, y_offset))
                
                # Puntaje
                score_text = self.font.render(str(score), True, (100, 100, 100))
                screen.blit(score_text, (700, y_offset))
                
                y_offset += 35
        else:
            no_records = self.font.render("No hay récords aún", True, (83, 83, 83))
            no_rect = no_records.get_rect(center=(WINDOW_WIDTH // 2, 200))
            screen.blit(no_records, no_rect)
        
        # Botón volver
        self.records_buttons['back'].update(mouse_pos)
        self.records_buttons['back'].draw(screen, self.button_font)
    
    def draw_instructions(self, screen, night_mode=False):
        """Dibuja las instrucciones en el juego"""
        text_color = COLOR_NIGHT_GROUND if night_mode else COLOR_TEXT
        
        instruction = self.font.render("Presiona ESPACIO o ↑ para saltar", True, text_color)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(instruction, instruction_rect)