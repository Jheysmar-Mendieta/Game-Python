"""Juego Dino Chrome - Archivo principal"""
import pygame
import sys
from settings import *
from player import Player
from obstacles import ObstacleManager
from background import Ground, CloudManager
from ui import UI
from sounds import SoundManager
from db import DatabaseManager


class DinoGame:
    """Clase principal del juego Dino Chrome"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dino Chrome")
        self.clock = pygame.time.Clock()
        
        # Componentes del juego
        self.player = Player()
        self.obstacle_manager = ObstacleManager()
        self.ground = Ground()
        self.cloud_manager = CloudManager()
        self.ui = UI()
        self.sounds = SoundManager()
        self.db = DatabaseManager()
        
        # Estados del juego
        self.state = "menu"  # menu, playing, game_over, records
        self.username = "Jugador"
        
        # Puntuación
        self.score = 0
        self.best_score = self.db.obtener_mejor_puntuacion(self.username, GAME_NAME)
        self.is_record = False
        self.last_checkpoint = 0
        
        # Modo noche
        self.night_mode = False
        self.night_mode_timer = 0
        self.night_mode_active = False
        
        # Control de inicio
        self.game_started = False
    
    def handle_events(self):
        """Maneja todos los eventos"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            
            # Menú principal
            if self.state == "menu":
                if self.ui.menu_buttons['play'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('jump')
                    self.start_game()
                elif self.ui.menu_buttons['records'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('jump')
                    self.state = "records"
                elif self.ui.menu_buttons['exit'].is_clicked(mouse_pos, mouse_pressed):
                    self.quit_game()
            
            # Game Over
            elif self.state == "game_over":
                if self.ui.gameover_buttons['retry'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('jump')
                    self.start_game()
                elif self.ui.gameover_buttons['menu'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('jump')
                    self.state = "menu"
            
            # Récords
            elif self.state == "records":
                if self.ui.records_buttons['back'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('jump')
                    self.state = "menu"
            
            # Jugando
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        if not self.game_started:
                            self.game_started = True
                        else:
                            self.player.jump()
                            self.sounds.play('jump')
    
    def start_game(self):
        """Inicia una nueva partida"""
        self.player.reset()
        self.obstacle_manager.reset()
        self.ground.reset()
        self.cloud_manager.reset()
        
        self.score = 0
        self.last_checkpoint = 0
        self.night_mode = False
        self.night_mode_timer = 0
        self.night_mode_active = False
        self.game_started = False
        self.is_record = False
        
        self.state = "playing"
    
    def end_game(self):
        """Finaliza la partida"""
        self.sounds.play('crash')
        
        # Guardar puntuación
        self.db.guardar_puntuacion(self.username, GAME_NAME, int(self.score))
        
        # Verificar récord
        self.is_record = self.db.verificar_nuevo_record(self.username, GAME_NAME, int(self.score))
        
        # Actualizar mejor puntuación
        new_best = self.db.obtener_mejor_puntuacion(self.username, GAME_NAME)
        if new_best > self.best_score:
            self.best_score = new_best
        
        self.state = "game_over"
    
    def update(self, delta_time):
        """Actualiza el estado del juego"""
        if self.state == "playing" and self.game_started:
            # Actualizar jugador
            self.player.update(delta_time)
            
            # Actualizar obstáculos
            self.obstacle_manager.update(delta_time)
            
            # Actualizar fondo
            self.ground.update(self.obstacle_manager.speed)
            self.cloud_manager.update(delta_time, self.night_mode)
            
            # Actualizar puntuación
            self.score += SCORE_INCREMENT
            
            # Checkpoint cada 100 puntos
            current_checkpoint = int(self.score) // CHECKPOINT_SCORE
            if current_checkpoint > self.last_checkpoint:
                self.last_checkpoint = current_checkpoint
                self.sounds.play('checkpoint')
            
            # Activar/desactivar modo noche
            if int(self.score) % NIGHT_MODE_SCORE < NIGHT_MODE_DURATION:
                if not self.night_mode_active:
                    self.night_mode = True
                    self.night_mode_active = True
                    self.cloud_manager.switch_mode(True)
            else:
                if self.night_mode_active:
                    self.night_mode = False
                    self.night_mode_active = False
                    self.cloud_manager.switch_mode(False)
            
            # Verificar colisiones
            if self.obstacle_manager.check_collision(self.player.get_collision_rect()):
                self.player.die()
                self.end_game()
    
    def draw(self):
        """Dibuja todo el juego"""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "menu":
            self.ui.draw_main_menu(self.screen, mouse_pos)
        
        elif self.state == "playing":
            # Fondo
            bg_color = COLOR_NIGHT_BG if self.night_mode else COLOR_DAY_BG
            self.screen.fill(bg_color)
            
            # Nubes/estrellas
            self.cloud_manager.draw(self.screen)
            
            # Piso
            self.ground.draw(self.screen, self.night_mode)
            
            # Obstáculos
            self.obstacle_manager.draw(self.screen, self.night_mode)
            
            # Jugador
            self.player.draw(self.screen, self.night_mode)
            
            # Puntuación
            self.ui.draw_score(self.screen, self.score, self.best_score, self.night_mode)
            
            # Instrucciones al inicio
            if not self.game_started:
                self.ui.draw_instructions(self.screen, self.night_mode)
        
        elif self.state == "game_over":
            # Dibujar el juego congelado de fondo
            bg_color = COLOR_NIGHT_BG if self.night_mode else COLOR_DAY_BG
            self.screen.fill(bg_color)
            
            self.cloud_manager.draw(self.screen)
            self.ground.draw(self.screen, self.night_mode)
            self.obstacle_manager.draw(self.screen, self.night_mode)
            self.player.draw(self.screen, self.night_mode)
            self.ui.draw_score(self.screen, self.score, self.best_score, self.night_mode)
            
            # Overlay de game over
            self.ui.draw_game_over(self.screen, self.score, self.best_score,
                                  self.is_record, mouse_pos,
                                  self.clock.get_time() / 1000.0, self.night_mode)
        
        elif self.state == "records":
            records = self.db.obtener_top_puntuaciones(GAME_NAME, 10)
            self.ui.draw_records(self.screen, records, mouse_pos)
        
        pygame.display.flip()
    
    def quit_game(self):
        """Cierra el juego"""
        self.db.cerrar()
        pygame.quit()
        sys.exit()
    
    def run(self):
        """Loop principal del juego"""
        print("=" * 60)
        print("🦖 DINO CHROME INICIADO")
        print("=" * 60)
        print(f"Jugador: {self.username}")
        print(f"Mejor puntuación: {self.best_score}")
        print("\nControles:")
        print("  🔼 ESPACIO / ↑  - Saltar")
        print("\nCaracterísticas:")
        print("  • Modo noche automático cada 700 puntos")
        print("  • Aumento gradual de velocidad")
        print("  • Sonido de checkpoint cada 100 puntos")
        print("=" * 60)
        
        while True:
            delta_time = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.draw()


if __name__ == "__main__":
    game = DinoGame()
    game.run()