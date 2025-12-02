"""Juego Arkanoid - Archivo principal"""
import pygame
import sys
from settings import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import PowerUpManager
from particles import ParticleSystem
from levels import LevelManager
from ui import UI
from sounds import SoundManager
from db import DatabaseManager


class ArkanoidGame:
    """Clase principal del juego Arkanoid"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        
        # Componentes
        self.paddle = Paddle()
        self.balls = []
        self.bricks = []
        self.powerup_manager = PowerUpManager()
        self.particle_system = ParticleSystem()
        self.level_manager = LevelManager()
        self.ui = UI()
        self.sounds = SoundManager()
        self.db = DatabaseManager()
        
        # Estados
        self.state = "menu"  # menu, playing, paused, game_over, victory, level_select, records
        self.username = "Jugador"
        
        # Datos del juego
        self.score = 0
        self.lives = INITIAL_LIVES
        self.current_level = 0
        self.best_score = self.db.obtener_mejor_puntuacion(self.username, GAME_NAME)
        self.is_record = False
        self.lives_lost_in_level = 0
        
        # Power-ups activos
        self.active_powerups = []
        
        # Control del juego
        self.use_mouse = True
    
    def start_level(self, level_index):
        """Inicia un nivel específico"""
        self.current_level = level_index
        
        # Cargar ladrillos del nivel
        self.bricks = self.level_manager.load_level(level_index)
        
        if self.bricks is None:
            print(f"Error: No se pudo cargar el nivel {level_index}")
            self.state = "menu"
            return
        
        # Reiniciar componentes
        self.paddle.reset()
        self.balls = [Ball(WINDOW_WIDTH // 2, PADDLE_Y - 30)]
        self.powerup_manager.clear()
        self.particle_system.clear()
        self.active_powerups = []
        self.lives_lost_in_level = 0
        
        self.state = "playing"
    
    def start_game(self):
        """Inicia el juego desde el nivel 1"""
        self.score = 0
        self.lives = INITIAL_LIVES
        self.start_level(0)
    
    def next_level(self):
        """Avanza al siguiente nivel"""
        # Bonus por nivel perfecto
        if self.lives_lost_in_level == 0:
            self.score += BONUS_PERFECT_LEVEL
        
        self.current_level += 1
        
        if self.current_level >= self.level_manager.get_level_count():
            # Juego completado
            self.end_game()
        else:
            self.start_level(self.current_level)
    
    def lose_life(self):
        """Pierde una vida"""
        self.lives -= 1
        self.lives_lost_in_level += 1
        self.sounds.play('life_lost')
        
        if self.lives <= 0:
            self.end_game()
        else:
            # Reiniciar pelota
            self.balls = [Ball(WINDOW_WIDTH // 2, PADDLE_Y - 30)]
            self.paddle.reset()
    
    def end_game(self):
        """Finaliza el juego"""
        # Guardar puntuación
        self.db.guardar_puntuacion(self.username, GAME_NAME, self.score)
        
        # Verificar récord
        self.is_record = self.db.verificar_nuevo_record(self.username, GAME_NAME, self.score)
        
        # Actualizar mejor puntuación
        new_best = self.db.obtener_mejor_puntuacion(self.username, GAME_NAME)
        if new_best > self.best_score:
            self.best_score = new_best
        
        if self.lives <= 0:
            self.sounds.play('game_over')
            self.state = "game_over"
        else:
            self.sounds.play('level_complete')
            self.state = "victory"
    
    def apply_powerup(self, powerup_type):
        """Aplica un power-up"""
        self.sounds.play('powerup')
        self.score += BONUS_POWERUP
        
        if powerup_type == POWERUP_EXPAND:
            self.paddle.apply_powerup(POWERUP_EXPAND)
            self.active_powerups.append("Pala Grande")
        elif powerup_type == POWERUP_SHRINK:
            self.paddle.apply_powerup(POWERUP_SHRINK)
            self.active_powerups.append("Pala Pequeña")
        elif powerup_type == POWERUP_MULTIBALL:
            # Crear pelota adicional
            if len(self.balls) > 0:
                original = self.balls[0]
                new_ball = Ball(original.x, original.y, angle=-45)
                self.balls.append(new_ball)
            self.active_powerups.append("Multi-Bola")
        elif powerup_type == POWERUP_SLOW:
            for ball in self.balls:
                ball.apply_powerup(POWERUP_SLOW)
            self.active_powerups.append("Lento")
        elif powerup_type == POWERUP_FAST:
            for ball in self.balls:
                ball.apply_powerup(POWERUP_FAST)
            self.active_powerups.append("Rápido")
        elif powerup_type == POWERUP_PIERCE:
            for ball in self.balls:
                ball.apply_powerup(POWERUP_PIERCE)
            self.active_powerups.append("Perforante")
        elif powerup_type == POWERUP_LIFE:
            self.lives += 1
            self.active_powerups.append("Vida Extra")
    
    def handle_events(self):
        """Maneja todos los eventos"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"
                
                if event.key == pygame.K_m:
                    self.use_mouse = not self.use_mouse
            
            # Menú principal
            if self.state == "menu":
                if self.ui.menu_buttons['play'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.start_game()
                elif self.ui.menu_buttons['levels'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "level_select"
                elif self.ui.menu_buttons['records'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "records"
                elif self.ui.menu_buttons['exit'].is_clicked(mouse_pos, mouse_pressed):
                    self.quit_game()
            
            # Pausa
            elif self.state == "paused":
                if self.ui.pause_buttons['continue'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "playing"
                elif self.ui.pause_buttons['restart'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.start_level(self.current_level)
                elif self.ui.pause_buttons['menu'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "menu"
            
            # Game Over
            elif self.state == "game_over":
                if self.ui.gameover_buttons['retry'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.start_game()
                elif self.ui.gameover_buttons['menu'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "menu"
            
            # Victoria
            elif self.state == "victory":
                has_next = self.current_level < self.level_manager.get_level_count() - 1
                if has_next and self.ui.victory_buttons['next'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.next_level()
                elif self.ui.victory_buttons['menu'].is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "menu"
            
            # Selección de nivel
            elif self.state == "level_select":
                if self.ui.back_button.is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "menu"
                else:
                    # Detectar click en niveles
                    levels_per_row = 3
                    for i in range(self.level_manager.get_level_count()):
                        row = i // levels_per_row
                        col = i % levels_per_row
                        x = 150 + col * 200
                        y = 150 + row * 150
                        rect = pygame.Rect(x, y, 150, 100)
                        
                        if rect.collidepoint(mouse_pos) and mouse_pressed:
                            self.sounds.play('paddle')
                            self.score = 0
                            self.lives = INITIAL_LIVES
                            self.start_level(i)
            
            # Récords
            elif self.state == "records":
                if self.ui.back_button.is_clicked(mouse_pos, mouse_pressed):
                    self.sounds.play('paddle')
                    self.state = "menu"
    
    def update(self, delta_time):
        """Actualiza el estado del juego"""
        if self.state != "playing":
            return
        
        # Actualizar pala
        mouse_x = pygame.mouse.get_pos()[0] if self.use_mouse else None
        keys = pygame.key.get_pressed() if not self.use_mouse else None
        self.paddle.update(delta_time, mouse_x, keys)
        
        # Actualizar pelotas
        for ball in self.balls[:]:
            ball.update(delta_time)
            
            # Colisión con pala
            if ball.get_rect().colliderect(self.paddle.get_rect()):
                if ball.vy > 0:  # Solo si va hacia abajo
                    ball.bounce_paddle(self.paddle.get_rect())
                    self.sounds.play('paddle')
            
            # Colisión con paredes
            prev_x = ball.x - ball.vx
            if (ball.x - ball.radius <= 0 and prev_x > ball.radius) or \
               (ball.x + ball.radius >= WINDOW_WIDTH and prev_x < WINDOW_WIDTH - ball.radius):
                self.sounds.play('wall')
            
            # Colisión con ladrillos
            for brick in self.bricks[:]:
                if brick.destroyed:
                    continue
                
                if ball.get_rect().colliderect(brick.get_rect()):
                    # Determinar lado de colisión
                    side = brick.get_collision_side(ball.get_rect(), ball.vx, ball.vy)
                    
                    # Rebotar
                    if not ball.piercing:
                        ball.bounce_brick(brick.get_rect(), side)
                    
                    # Golpear ladrillo
                    destroyed = brick.hit()
                    
                    if destroyed:
                        # Efectos
                        self.sounds.play('brick')
                        self.particle_system.create_explosion(
                            brick.x + brick.width // 2,
                            brick.y + brick.height // 2,
                            brick.color
                        )
                        
                        # Puntos
                        self.score += BRICK_POINTS.get(brick.original_type, 10)
                        
                        # Power-up
                        self.powerup_manager.spawn_powerup(
                            brick.x + brick.width // 2,
                            brick.y + brick.height // 2
                        )
                        
                        # Aumentar velocidad de pelotas
                        for b in self.balls:
                            b.increase_speed()
                    else:
                        self.sounds.play('resistant')
                        self.particle_system.create_spark(
                            brick.x + brick.width // 2,
                            brick.y + brick.height // 2,
                            brick.color
                        )
                    
                    if not ball.piercing:
                        break
            
            # Verificar si cayó
            if ball.is_below_screen():
                ball.active = False
        
        # Eliminar pelotas inactivas
        self.balls = [b for b in self.balls if b.active]
        
        # Perder vida si no quedan pelotas
        if len(self.balls) == 0:
            self.lose_life()
        
        # Actualizar power-ups
        self.powerup_manager.update(delta_time)
        collected_powerups = self.powerup_manager.check_collision(self.paddle.get_rect())
        for powerup in collected_powerups:
            self.apply_powerup(powerup)
        
        # Actualizar partículas
        self.particle_system.update(delta_time)
        
        # Verificar victoria (todos los ladrillos destruibles destruidos)
        destructible_bricks = [b for b in self.bricks 
                              if not b.destroyed and b.type != BRICK_INDESTRUCTIBLE]
        if len(destructible_bricks) == 0:
            self.end_game()
        
        # Limpiar lista de power-ups activos (solo para UI)
        self.active_powerups = [p for p in self.active_powerups[-3:]]
    
    def draw(self):
        """Dibuja todo el juego"""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "menu":
            self.ui.draw_main_menu(self.screen, mouse_pos)
        
        elif self.state == "playing" or self.state == "paused":
            # Fondo
            self.screen.fill(COLOR_BG)
            
            # Ladrillos
            for brick in self.bricks:
                brick.draw(self.screen)
            
            # Partículas
            self.particle_system.draw(self.screen)
            
            # Pala
            self.paddle.draw(self.screen)
            
            # Pelotas
            for ball in self.balls:
                ball.draw(self.screen)
            
            # Power-ups
            self.powerup_manager.draw(self.screen)
            
            # HUD
            self.ui.draw_hud(self.screen, self.score, self.lives, 
                           self.current_level, self.active_powerups)
            
            # Menú de pausa
            if self.state == "paused":
                self.ui.draw_pause_menu(self.screen, mouse_pos)
        
        elif self.state == "game_over":
            # Dibujar juego de fondo
            self.screen.fill(COLOR_BG)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.paddle.draw(self.screen)
            for ball in self.balls:
                ball.draw(self.screen)
            
            # Overlay
            self.ui.draw_game_over(self.screen, self.score, self.best_score,
                                  self.is_record, mouse_pos)
        
        elif self.state == "victory":
            # Dibujar juego de fondo
            self.screen.fill(COLOR_BG)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.paddle.draw(self.screen)
            
            # Overlay
            level_info = self.level_manager.get_current_level_info()
            has_next = self.current_level < self.level_manager.get_level_count() - 1
            self.ui.draw_victory(self.screen, self.score, level_info['name'], 
                               mouse_pos, has_next)
        
        elif self.state == "level_select":
            self.ui.draw_level_select(self.screen, self.level_manager, mouse_pos)
        
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
        print("🎮 ARKANOID INICIADO")
        print("=" * 60)
        print(f"Jugador: {self.username}")
        print(f"Mejor puntuación: {self.best_score}")
        print("\nControles:")
        print("  🖱️  MOUSE      - Mover pala (por defecto)")
        print("  ⬅️  A / ←      - Mover pala izquierda")
        print("  ➡️  D / →      - Mover pala derecha")
        print("  🔤 M           - Alternar control mouse/teclado")
        print("  ⏸️  ESC        - Pausar")
        print("\nPower-ups:")
        print("  ↔  Agrandar pala    ●● Multi-bola")
        print("  →← Reducir pala     ↓  Ralentizar")
        print("  ↑  Acelerar         ⚡ Perforante")
        print("  ♥  Vida extra")
        print("=" * 60)
        
        while True:
            delta_time = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.draw()


if __name__ == "__main__":
    game = ArkanoidGame()
    game.run()