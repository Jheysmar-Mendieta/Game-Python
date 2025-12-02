"""Memory Game - Juego de Parejas
Juego completo de memoria con múltiples niveles y base de datos
"""
import pygame
import sys
from config import *
from db import DatabaseManager
from sounds import SoundManager
from game_state import GameState
from ui import Button, Label, Panel, InputBox
from particles import BackgroundStars


class MemoryGame:
    """Clase principal del juego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memory Game - Juego de Parejas")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Managers
        self.sound_manager = SoundManager()
        self.db_manager = DatabaseManager()
        
        # Estados
        self.state = "menu"  # menu, level_select, game, pause, victory, records
        self.game_state = None
        self.selected_level = 1
        self.username = ""
        
        # Decoración
        self.bg_stars = BackgroundStars(SCREEN_WIDTH, SCREEN_HEIGHT, 40)
        
        # Imágenes de cartas
        self._generate_card_images()
        
        # UI
        self._init_ui()
        
        # Música
        self.sound_manager.play_background_music()
        
    def _generate_card_images(self):
        """Genera imágenes para las cartas"""
        self.card_images = []
        symbols = ['♠', '♣', '♥', '♦', '★', '●', '■', '▲', '◆', '♪', 
                  '☀', '☁', '☂', '☃', '✓', '✗', '⚡', '♨']
        colors_palette = [
            COLORS['primary'], COLORS['success'], COLORS['warning'],
            (255, 100, 150), (150, 100, 255), (255, 150, 50)
        ]
        
        for i, symbol in enumerate(symbols):
            # Crear superficie
            img = pygame.Surface((60, 60), pygame.SRCALPHA)
            color = colors_palette[i % len(colors_palette)]
            
            # Dibujar símbolo
            text = self.font_large.render(symbol, True, color)
            text_rect = text.get_rect(center=(30, 30))
            img.blit(text, text_rect)
            
            self.card_images.append(img)
            
    def _init_ui(self):
        """Inicializa elementos de UI"""
        # Menú principal
        cx = SCREEN_WIDTH // 2
        self.menu_buttons = [
            Button(cx - 150, 250, 300, 60, "Jugar", COLORS['primary']),
            Button(cx - 150, 330, 300, 60, "Seleccionar Nivel", COLORS['success']),
            Button(cx - 150, 410, 300, 60, "Ver Récords", COLORS['warning']),
            Button(cx - 150, 490, 300, 60, "Salir", COLORS['text'])
        ]
        
        # Input de nombre
        self.input_box = InputBox(cx - 150, 570, 300, 50, "Ingresa tu nombre...")
        
        # Botones de nivel
        self.level_buttons = []
        for i, (level, config) in enumerate(LEVELS.items()):
            btn = Button(cx - 150, 200 + i * 80, 300, 60, 
                        config['name'], COLORS['primary'])
            self.level_buttons.append(btn)
            
        # Botón volver
        self.back_button = Button(50, SCREEN_HEIGHT - 80, 120, 50, "← Volver", COLORS['text'])
        
        # Botones de pausa
        self.pause_buttons = [
            Button(cx - 150, 300, 300, 60, "Continuar", COLORS['success']),
            Button(cx - 150, 380, 300, 60, "Reiniciar", COLORS['warning']),
            Button(cx - 150, 460, 300, 60, "Menú Principal", COLORS['text'])
        ]
        
        # Botones de victoria
        self.victory_buttons = [
            Button(cx - 200, 450, 180, 60, "Siguiente Nivel", COLORS['success']),
            Button(cx - 200, 520, 180, 60, "Repetir", COLORS['warning']),
            Button(cx + 20, 450, 180, 60, "Ver Récords", COLORS['primary']),
            Button(cx + 20, 520, 180, 60, "Menú", COLORS['text'])
        ]
        
    def handle_events(self):
        """Maneja eventos de pygame"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "game":
                        self.game_state.paused = not self.game_state.paused
                        self.state = "pause" if self.game_state.paused else "game"
                        
                # Input box
                if self.state == "menu":
                    if self.input_box.handle_event(event):
                        if self.input_box.text.strip():
                            self.username = self.input_box.text.strip()
                            
            # Actualizar input box
            if self.state == "menu":
                self.input_box.handle_event(event)
                
        # Manejar estados
        if self.state == "menu":
            self._handle_menu(mouse_pos, mouse_pressed)
        elif self.state == "level_select":
            self._handle_level_select(mouse_pos, mouse_pressed)
        elif self.state == "game":
            self._handle_game(mouse_pos, mouse_pressed)
        elif self.state == "pause":
            self._handle_pause(mouse_pos, mouse_pressed)
        elif self.state == "victory":
            self._handle_victory(mouse_pos, mouse_pressed)
        elif self.state == "records":
            self._handle_records(mouse_pos, mouse_pressed)
            
        return True
        
    def _handle_menu(self, mouse_pos, mouse_pressed):
        """Maneja el menú principal"""
        for btn in self.menu_buttons:
            btn.update(mouse_pos)
            
            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.sound_manager.play('button')
                
                if btn.text == "Jugar":
                    if self.input_box.text.strip():
                        self.username = self.input_box.text.strip()
                        self.start_game()
                elif btn.text == "Seleccionar Nivel":
                    self.state = "level_select"
                elif btn.text == "Ver Récords":
                    self.state = "records"
                elif btn.text == "Salir":
                    pygame.quit()
                    sys.exit()
                    
    def _handle_level_select(self, mouse_pos, mouse_pressed):
        """Maneja selección de nivel"""
        for i, btn in enumerate(self.level_buttons):
            btn.update(mouse_pos)
            
            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.sound_manager.play('button')
                self.selected_level = i + 1
                self.state = "menu"
                
        self.back_button.update(mouse_pos)
        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            self.sound_manager.play('button')
            self.state = "menu"
            
    def _handle_game(self, mouse_pos, mouse_pressed):
        """Maneja el juego activo"""
        if mouse_pressed:
            self.game_state.handle_click(mouse_pos)
            
        # Verificar victoria
        if self.game_state.is_won and self.state == "game":
            self.state = "victory"
            # Guardar puntuación
            score = self.game_state.get_score()
            if self.username:
                self.db_manager.guardar_puntuacion(self.username, score, self.selected_level)
                
    def _handle_pause(self, mouse_pos, mouse_pressed):
        """Maneja menú de pausa"""
        for btn in self.pause_buttons:
            btn.update(mouse_pos)
            
            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.sound_manager.play('button')
                
                if btn.text == "Continuar":
                    self.game_state.paused = False
                    self.state = "game"
                elif btn.text == "Reiniciar":
                    self.start_game()
                elif btn.text == "Menú Principal":
                    self.state = "menu"
                    
    def _handle_victory(self, mouse_pos, mouse_pressed):
        """Maneja pantalla de victoria"""
        for btn in self.victory_buttons:
            btn.update(mouse_pos)
            
            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.sound_manager.play('button')
                
                if btn.text == "Siguiente Nivel":
                    if self.selected_level < len(LEVELS):
                        self.selected_level += 1
                        self.start_game()
                elif btn.text == "Repetir":
                    self.start_game()
                elif btn.text == "Ver Récords":
                    self.state = "records"
                elif btn.text == "Menú":
                    self.state = "menu"
                    
    def _handle_records(self, mouse_pos, mouse_pressed):
        """Maneja pantalla de récords"""
        self.back_button.update(mouse_pos)
        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            self.sound_manager.play('button')
            self.state = "menu"
            
    def start_game(self):
        """Inicia un nuevo juego"""
        self.game_state = GameState(self.selected_level, self.sound_manager)
        self.state = "game"
        
    def update(self, dt):
        """Actualiza la lógica del juego"""
        self.bg_stars.update(dt)
        
        if self.state == "menu":
            self.input_box.update(dt)
            
        if self.state == "game" and self.game_state:
            mouse_pos = pygame.mouse.get_pos()
            self.game_state.update(dt, mouse_pos)
            
    def draw(self):
        """Dibuja todo en pantalla"""
        # Fondo
        self.screen.fill(COLORS['background'])
        self.bg_stars.draw(self.screen)
        
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "level_select":
            self._draw_level_select()
        elif self.state == "game":
            self._draw_game()
        elif self.state == "pause":
            self._draw_pause()
        elif self.state == "victory":
            self._draw_victory()
        elif self.state == "records":
            self._draw_records()
            
        pygame.display.flip()
        
    def _draw_menu(self):
        """Dibuja menú principal"""
        # Título
        title = self.font_large.render("MEMORY GAME", True, COLORS['primary'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        
        # Sombra del título
        shadow = self.font_large.render("MEMORY GAME", True, (*COLORS['shadow'][:3], 100))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 123))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render("Juego de Parejas", True, COLORS['text'])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Nivel seleccionado
        level_text = f"Nivel seleccionado: {LEVELS[self.selected_level]['name']}"
        level_surf = self.font_small.render(level_text, True, COLORS['text'])
        level_rect = level_surf.get_rect(center=(SCREEN_WIDTH // 2, 210))
        self.screen.blit(level_surf, level_rect)
        
        # Botones
        for btn in self.menu_buttons:
            btn.draw(self.screen, self.font_medium)
            
        # Input box
        self.input_box.draw(self.screen, self.font_small)
        
    def _draw_level_select(self):
        """Dibuja selección de nivel"""
        # Título
        title = self.font_large.render("SELECCIONAR NIVEL", True, COLORS['primary'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Botones
        for btn in self.level_buttons:
            btn.draw(self.screen, self.font_medium)
            
        self.back_button.draw(self.screen, self.font_small)
        
    def _draw_game(self):
        """Dibuja el juego"""
        # HUD
        panel = Panel(0, 0, SCREEN_WIDTH, HUD_HEIGHT, COLORS['card_front'], 230)
        panel.draw(self.screen)
        
        # Información
        info_y = 20
        
        # Nivel
        level_text = f"Nivel {self.selected_level}: {LEVELS[self.selected_level]['name']}"
        level_surf = self.font_medium.render(level_text, True, COLORS['primary'])
        self.screen.blit(level_surf, (20, info_y))
        
        # Movimientos
        moves_text = f"Movimientos: {self.game_state.moves}"
        moves_surf = self.font_small.render(moves_text, True, COLORS['text'])
        self.screen.blit(moves_surf, (20, info_y + 35))
        
        # Parejas
        pairs_text = f"Parejas: {self.game_state.pairs_found}/{self.game_state.total_pairs}"
        pairs_surf = self.font_small.render(pairs_text, True, COLORS['text'])
        pairs_rect = pairs_surf.get_rect(center=(SCREEN_WIDTH // 2, info_y + 25))
        self.screen.blit(pairs_surf, pairs_rect)
        
        # Tiempo
        time_text = f"Tiempo: {self.game_state.format_time()}"
        time_surf = self.font_small.render(time_text, True, COLORS['text'])
        time_rect = time_surf.get_rect(right=SCREEN_WIDTH - 20, top=info_y)
        self.screen.blit(time_surf, time_rect)
        
        # Usuario
        if self.username:
            user_text = f"Jugador: {self.username}"
            user_surf = self.font_small.render(user_text, True, COLORS['text'])
            user_rect = user_surf.get_rect(right=SCREEN_WIDTH - 20, top=info_y + 35)
            self.screen.blit(user_surf, user_rect)
        
        # Tablero
        self.game_state.draw(self.screen, self.card_images)
        
    def _draw_pause(self):
        """Dibuja menú de pausa"""
        # Overlay semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLORS['background'][:3], 200))
        self.screen.blit(overlay, (0, 0))
        
        # Panel
        cx = SCREEN_WIDTH // 2
        panel = Panel(cx - 200, 150, 400, 400, COLORS['card_front'])
        panel.draw(self.screen)
        
        # Título
        title = self.font_large.render("PAUSA", True, COLORS['text'])
        title_rect = title.get_rect(center=(cx, 220))
        self.screen.blit(title, title_rect)
        
        # Botones
        for btn in self.pause_buttons:
            btn.draw(self.screen, self.font_medium)
            
    def _draw_victory(self):
        """Dibuja pantalla de victoria"""
        # Fondo con partículas
        if self.game_state:
            self.game_state.particles.draw(self.screen)
            
        # Panel central
        cx = SCREEN_WIDTH // 2
        panel = Panel(cx - 250, 100, 500, 500, COLORS['card_front'])
        panel.draw(self.screen)
        
        # Título
        title = self.font_large.render("¡VICTORIA!", True, COLORS['success'])
        title_rect = title.get_rect(center=(cx, 160))
        self.screen.blit(title, title_rect)
        
        # Estadísticas
        y = 240
        stats = [
            f"Nivel: {LEVELS[self.selected_level]['name']}",
            f"Tiempo: {self.game_state.format_time()}",
            f"Movimientos: {self.game_state.moves}",
            f"Puntuación: {self.game_state.get_score()}"
        ]
        
        for stat in stats:
            text = self.font_medium.render(stat, True, COLORS['text'])
            text_rect = text.get_rect(center=(cx, y))
            self.screen.blit(text, text_rect)
            y += 40
            
        # Verificar récord
        if self.username:
            is_record = self.db_manager.verificar_nuevo_record(
                self.username, self.selected_level, self.game_state.get_score()
            )
            
            if is_record:
                record_text = "¡NUEVO RÉCORD PERSONAL!"
                record_surf = self.font_medium.render(record_text, True, COLORS['warning'])
                record_rect = record_surf.get_rect(center=(cx, y + 10))
                self.screen.blit(record_surf, record_rect)
                
        # Botones
        for btn in self.victory_buttons:
            btn.draw(self.screen, self.font_small)
            
    def _draw_records(self):
        """Dibuja tabla de récords"""
        # Título
        title = self.font_large.render("RÉCORDS", True, COLORS['primary'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Tablas por nivel
        y = 150
        for level in range(1, len(LEVELS) + 1):
            # Título del nivel
            level_title = self.font_medium.render(
                f"{LEVELS[level]['name']}", True, COLORS['text']
            )
            self.screen.blit(level_title, (100, y))
            y += 40
            
            # Obtener récords
            records = self.db_manager.obtener_top_puntuaciones(level, 5)
            
            if records:
                for i, (username, score, _) in enumerate(records):
                    # Limpiar sufijo de nivel del username
                    display_name = username.split('-Nivel')[0]
                    text = f"{i+1}. {display_name}: {score} puntos"
                    text_surf = self.font_small.render(text, True, COLORS['text'])
                    self.screen.blit(text_surf, (120, y))
                    y += 30
            else:
                text = self.font_small.render("No hay récords aún", True, COLORS['text'])
                self.screen.blit(text, (120, y))
                y += 30
                
            y += 20
            
        self.back_button.draw(self.screen, self.font_small)
        
    def run(self):
        """Loop principal del juego"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS)
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            
        self.db_manager.cerrar()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = MemoryGame()
    game.run()