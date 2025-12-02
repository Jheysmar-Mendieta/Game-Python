"""Racing Game - Juego de Carreras Top-Down
Juego completo de carreras con IA, física realista y múltiples pistas
"""
import pygame
import sys
from config import *
from db import DatabaseManager
from car import Car
from track import Track
from ai import AIController
from particles import ParticleSystem
from sounds import SoundManager


class Camera:
    """Cámara que sigue al jugador"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        
    def update(self, target_x, target_y, track_width, track_height):
        """Actualiza posición de la cámara"""
        # Centrar en el objetivo con suavizado
        target_cam_x = target_x - self.width // 2
        target_cam_y = target_y - self.height // 2
        
        self.x += (target_cam_x - self.x) * CAMERA_SMOOTHNESS
        self.y += (target_cam_y - self.y) * CAMERA_SMOOTHNESS
        
        # Limitar a los bordes de la pista
        self.x = max(0, min(self.x, track_width - self.width))
        self.y = max(0, min(self.y, track_height - self.height))


class RacingGame:
    """Clase principal del juego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Game - Top-Down")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Managers
        self.sound_manager = SoundManager()
        self.db_manager = DatabaseManager()
        
        # Estado del juego
        self.state = "menu"  # menu, track_select, race, pause, results
        self.mode = "quick_race"  # quick_race, time_trial, championship
        
        # Carrera
        self.track = None
        self.player_car = None
        self.ai_cars = []
        self.ai_controllers = []
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particles = ParticleSystem()
        
        # UI
        self.username = ""
        self.selected_track = 'track1'
        self.num_opponents = 3
        
        # Iniciar música
        self.sound_manager.play_background_music()
        
    def start_race(self):
        """Inicia una carrera"""
        # Crear pista
        self.track = Track(self.selected_track)
        
        # Crear jugador
        spawn = self.track.spawn_points[0]
        self.player_car = Car(spawn[0], spawn[1], CAR_COLORS[0], is_player=True)
        
        # Crear rivales IA
        self.ai_cars = []
        self.ai_controllers = []
        
        for i in range(min(self.num_opponents, len(self.track.spawn_points) - 1)):
            spawn = self.track.spawn_points[i + 1]
            ai_car = Car(spawn[0], spawn[1], CAR_COLORS[i + 1], is_player=False)
            self.ai_cars.append(ai_car)
            
            # Crear controlador IA con diferentes niveles de agresión
            aggression = 0.5 + (i * 0.1)
            controller = AIController(ai_car, self.track, aggression)
            self.ai_controllers.append(controller)
            
        # Limpiar partículas
        self.particles.clear()
        
        # Cambiar estado
        self.state = "race"
        
    def handle_events(self):
        """Maneja eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "race":
                        self.state = "pause"
                    elif self.state == "pause":
                        self.state = "race"
                    elif self.state in ["menu", "track_select", "results"]:
                        self.state = "menu"
                        
        # Controles del jugador
        if self.state == "race" and self.player_car:
            keys = pygame.key.get_pressed()
            self.player_car.accelerating = keys[pygame.K_UP] or keys[pygame.K_w]
            self.player_car.braking = keys[pygame.K_DOWN] or keys[pygame.K_s]
            self.player_car.turning_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            self.player_car.turning_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            
        return True
        
    def update(self, dt):
        """Actualiza la lógica del juego"""
        if self.state == "race":
            self._update_race(dt)
            
    def _update_race(self, dt):
        """Actualiza la carrera"""
        all_cars = [self.player_car] + self.ai_cars
        
        # Actualizar jugador
        self.player_car.update(dt, self.track)
        
        # Verificar colisiones y checkpoints para jugador
        self.track.check_collision(self.player_car)
        checkpoint = self.track.check_checkpoint(self.player_car)
        if checkpoint is not None and checkpoint == 0:
            self.sound_manager.play('lap_complete')
            
        # Actualizar IA
        for i, ai_car in enumerate(self.ai_cars):
            self.ai_controllers[i].update(dt, all_cars)
            ai_car.update(dt, self.track)
            self.track.check_collision(ai_car)
            self.track.check_checkpoint(ai_car)
            
        # Actualizar posiciones
        self._update_positions(all_cars)
        
        # Generar partículas
        for car in all_cars:
            if car.is_drifting:
                self.particles.emit_smoke(car.x, car.y, car.angle, car.speed)
            if car.is_offtrack:
                self.particles.emit_dust(car.x, car.y)
            if car.collision_cooldown > 0 and car.collision_cooldown > dt * 5:
                self.particles.emit_sparks(car.x, car.y)
                if car == self.player_car:
                    self.sound_manager.play('crash')
                    
        self.particles.update(dt)
        
        # Actualizar cámara
        self.camera.update(
            self.player_car.x, self.player_car.y,
            self.track.width * TILE_SIZE,
            self.track.height * TILE_SIZE
        )
        
        # Sonido de motor
        speed_factor = abs(self.player_car.speed) / CAR_MAX_SPEED
        self.sound_manager.play_engine(speed_factor)
        
        # Verificar fin de carrera
        if self.player_car.finished:
            self._finish_race()
            
    def _update_positions(self, cars):
        """Actualiza posiciones de los coches"""
        # Ordenar por progreso (vuelta + checkpoint)
        def get_progress(car):
            return car.lap * 100 + car.checkpoint_passed * 30 - car.current_lap_time
            
        sorted_cars = sorted(cars, key=get_progress, reverse=True)
        
        for i, car in enumerate(sorted_cars):
            car.position = i + 1
            
    def _finish_race(self):
        """Finaliza la carrera"""
        self.sound_manager.play('victory')
        self.sound_manager.stop_engine()
        
        # Guardar puntuación (tiempo total)
        if self.username:
            score = int(self.player_car.total_time)
            self.db_manager.guardar_puntuacion(
                self.username, score, self.selected_track
            )
            
        self.state = "results"
        
    def draw(self):
        """Dibuja todo en pantalla"""
        self.screen.fill(COLORS['background'])
        
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "track_select":
            self._draw_track_select()
        elif self.state == "race":
            self._draw_race()
        elif self.state == "pause":
            self._draw_pause()
        elif self.state == "results":
            self._draw_results()
            
        pygame.display.flip()
        
    def _draw_menu(self):
        """Dibuja menú principal"""
        # Título
        title = self.font_large.render("RACING GAME", True, COLORS['white'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        
        shadow = self.font_large.render("RACING GAME", True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 124))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font_small.render("Top-Down Racing", True, COLORS['white'])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Opciones
        options = [
            "Presiona ESPACIO para comenzar",
            f"Pista: {TRACKS[self.selected_track]['name']}",
            f"Rivales: {self.num_opponents}",
            "",
            "Controles:",
            "WASD / Flechas - Conducir",
            "ESC - Pausa"
        ]
        
        y = 280
        for i, opt in enumerate(options):
            if i == 0:
                color = COLORS['yellow']
                font = self.font_medium
            elif i < 3:
                color = COLORS['green']
                font = self.font_small
            else:
                color = COLORS['white']
                font = self.font_tiny
                
            text = font.render(opt, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50 if i < 3 else 30
            
        # Input de nombre
        input_text = "Nombre: " + (self.username if self.username else "___")
        input_surf = self.font_small.render(input_text, True, COLORS['white'])
        input_rect = input_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(input_surf, input_rect)
        
        # Cambiar opciones
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.username:
                self.username = "Player"
            self.start_race()
        elif keys[pygame.K_TAB]:
            tracks = list(TRACKS.keys())
            idx = tracks.index(self.selected_track)
            self.selected_track = tracks[(idx + 1) % len(tracks)]
            pygame.time.wait(200)
        elif keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.num_opponents = min(5, self.num_opponents + 1)
            pygame.time.wait(200)
        elif keys[pygame.K_MINUS]:
            self.num_opponents = max(1, self.num_opponents - 1)
            pygame.time.wait(200)
            
        # Capturar nombre
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key not in [pygame.K_SPACE, pygame.K_TAB, pygame.K_ESCAPE]:
                    if len(self.username) < 12 and event.unicode.isprintable():
                        self.username += event.unicode
                        
    def _draw_race(self):
        """Dibuja la carrera"""
        # Dibujar pista
        self.track.draw(self.screen, self.camera.x, self.camera.y)
        
        # Dibujar partículas
        self.particles.draw(self.screen, self.camera.x, self.camera.y)
        
        # Dibujar coches (primero IA, luego jugador)
        for car in self.ai_cars:
            car.draw(self.screen, self.camera.x, self.camera.y)
        self.player_car.draw(self.screen, self.camera.x, self.camera.y)
        
        # HUD
        self._draw_hud()
        
    def _draw_hud(self):
        """Dibuja HUD de carrera"""
        # Panel superior
        hud_surf = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
        hud_surf.fill((*COLORS['black'], 180))
        self.screen.blit(hud_surf, (0, 0))
        
        # Posición
        pos_text = f"{self.player_car.position}/{len(self.ai_cars) + 1}"
        pos_surf = self.font_large.render(pos_text, True, COLORS['yellow'])
        self.screen.blit(pos_surf, (20, 20))
        
        # Vuelta
        lap_text = f"Vuelta {self.player_car.lap}/{MAX_LAPS}"
        lap_surf = self.font_small.render(lap_text, True, COLORS['white'])
        self.screen.blit(lap_surf, (20, 85))
        
        # Velocidad
        speed_text = f"{int(self.player_car.get_speed_kmh())} km/h"
        speed_surf = self.font_medium.render(speed_text, True, COLORS['green'])
        speed_rect = speed_surf.get_rect(right=SCREEN_WIDTH - 20, top=20)
        self.screen.blit(speed_surf, speed_rect)
        
        # Tiempo
        time_text = f"Tiempo: {self._format_time(self.player_car.total_time)}"
        time_surf = self.font_small.render(time_text, True, COLORS['white'])
        time_rect = time_surf.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(time_surf, time_rect)
        
        # Mejor vuelta
        best_lap = self.player_car.get_best_lap()
        if best_lap > 0:
            best_text = f"Mejor: {self._format_time(best_lap)}"
            best_surf = self.font_tiny.render(best_text, True, COLORS['yellow'])
            best_rect = best_surf.get_rect(center=(SCREEN_WIDTH // 2, 65))
            self.screen.blit(best_surf, best_rect)
            
        # Vuelta actual
        current_text = f"Actual: {self._format_time(self.player_car.current_lap_time)}"
        current_surf = self.font_tiny.render(current_text, True, COLORS['white'])
        current_rect = current_surf.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(current_surf, current_rect)
        
    def _draw_pause(self):
        """Dibuja menú de pausa"""
        # Dibujar carrera de fondo
        self._draw_race()
        
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLORS['black'], 180))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        pause_text = self.font_large.render("PAUSA", True, COLORS['yellow'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Opciones
        options = [
            "ESC - Continuar",
            "R - Reiniciar",
            "M - Menú Principal"
        ]
        
        y = SCREEN_HEIGHT // 2 + 50
        for opt in options:
            text = self.font_small.render(opt, True, COLORS['white'])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50
            
        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.start_race()
        elif keys[pygame.K_m]:
            self.sound_manager.stop_engine()
            self.state = "menu"
            
    def _draw_results(self):
        """Dibuja pantalla de resultados"""
        # Panel central
        panel_width = 600
        panel_height = 500
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((*COLORS['black'], 220))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Título
        if self.player_car.position == 1:
            title_text = "¡VICTORIA!"
            title_color = COLORS['yellow']
        else:
            title_text = "CARRERA TERMINADA"
            title_color = COLORS['white']
            
        title = self.font_large.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 60))
        self.screen.blit(title, title_rect)
        
        # Estadísticas
        stats = [
            f"Posición Final: {self.player_car.position}º",
            f"Tiempo Total: {self._format_time(self.player_car.total_time)}",
            f"Mejor Vuelta: {self._format_time(self.player_car.get_best_lap())}",
            f"Pista: {TRACKS[self.selected_track]['name']}"
        ]
        
        y = panel_y + 150
        for stat in stats:
            text = self.font_small.render(stat, True, COLORS['white'])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50
            
        # Opciones
        options = [
            "ESPACIO - Nueva Carrera",
            "M - Menú Principal"
        ]
        
        y = panel_y + panel_height - 100
        for opt in options:
            text = self.font_tiny.render(opt, True, COLORS['green'])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 35
            
        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.start_race()
        elif keys[pygame.K_m]:
            self.state = "menu"
            
    def _format_time(self, seconds):
        """Formatea tiempo en MM:SS.ms"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 100)
        return f"{minutes:02d}:{secs:02d}.{millis:02d}"
        
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
    game = RacingGame()
    game.run()