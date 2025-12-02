"""Clase para representar un vehículo en el juego"""
import pygame
import math
from config import *


class Car:
    """Representa un coche de carreras"""
    
    def __init__(self, x, y, color, is_player=True):
        self.x = x
        self.y = y
        self.angle = 0  # Ángulo en grados
        self.speed = 0
        self.color = color
        self.is_player = is_player
        
        # Física
        self.velocity_x = 0
        self.velocity_y = 0
        self.drift_angle = 0
        
        # Dimensiones
        self.width = 20
        self.height = 32
        
        # Estado
        self.is_offtrack = False
        self.is_drifting = False
        self.collision_cooldown = 0
        
        # Carrera
        self.lap = 1
        self.checkpoint_passed = 0
        self.lap_times = []
        self.current_lap_time = 0
        self.total_time = 0
        self.position = 1
        self.finished = False
        
        # Controles (para jugador)
        self.accelerating = False
        self.braking = False
        self.turning_left = False
        self.turning_right = False
        
        # Sprite
        self._generate_sprite()
        
    def _generate_sprite(self):
        """Genera el sprite del coche"""
        self.original_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Cuerpo principal
        pygame.draw.rect(self.original_surface, self.color, 
                        (2, 4, self.width-4, self.height-8))
        
        # Ventanas
        pygame.draw.rect(self.original_surface, (100, 150, 200), 
                        (4, 8, self.width-8, 8))
        pygame.draw.rect(self.original_surface, (100, 150, 200), 
                        (4, self.height-16, self.width-8, 8))
        
        # Luces delanteras
        pygame.draw.circle(self.original_surface, (255, 255, 200), (5, 3), 3)
        pygame.draw.circle(self.original_surface, (255, 255, 200), (self.width-5, 3), 3)
        
        # Luces traseras
        pygame.draw.circle(self.original_surface, (255, 50, 50), (5, self.height-3), 2)
        pygame.draw.circle(self.original_surface, (255, 50, 50), (self.width-5, self.height-3), 2)
        
        self.surface = self.original_surface.copy()
        
    def update(self, dt, track):
        """Actualiza física y estado del coche"""
        if self.finished:
            return
            
        # Actualizar timer
        self.current_lap_time += dt / 1000
        self.total_time += dt / 1000
        
        # Cooldown de colisión
        if self.collision_cooldown > 0:
            self.collision_cooldown -= dt
            
        # Aplicar controles (si es jugador)
        if self.is_player:
            self._apply_controls(dt)
        
        # Aplicar física
        self._apply_physics(dt)
        
        # Verificar límites de pista
        self._check_track_bounds(track)
        
        # Actualizar sprite rotado
        self._update_sprite()
        
    def _apply_controls(self, dt):
        """Aplica los controles del jugador"""
        # Aceleración
        if self.accelerating:
            self.speed += CAR_ACCELERATION
        elif self.braking:
            self.speed -= CAR_DECELERATION * 2
        else:
            # Fricción natural
            if self.speed > 0:
                self.speed -= CAR_DECELERATION
            elif self.speed < 0:
                self.speed += CAR_DECELERATION
                
        # Límites de velocidad
        self.speed = max(CAR_MIN_SPEED, min(CAR_MAX_SPEED, self.speed))
        
        # Giro (solo si hay velocidad)
        if abs(self.speed) > 0.5:
            turn_amount = CAR_TURN_SPEED * (abs(self.speed) / CAR_MAX_SPEED)
            
            if self.turning_left:
                self.angle -= turn_amount
            if self.turning_right:
                self.angle += turn_amount
                
    def _apply_physics(self, dt):
        """Aplica física de movimiento"""
        # Calcular dirección de movimiento
        angle_rad = math.radians(self.angle)
        
        # Velocidad basada en dirección
        target_vx = self.speed * math.sin(angle_rad)
        target_vy = -self.speed * math.cos(angle_rad)
        
        # Inercia y derrape
        drift_factor = CAR_DRIFT_FACTOR if self.is_drifting else 0.7
        self.velocity_x = self.velocity_x * drift_factor + target_vx * (1 - drift_factor)
        self.velocity_y = self.velocity_y * drift_factor + target_vy * (1 - drift_factor)
        
        # Fricción adicional si está fuera de pista
        if self.is_offtrack:
            self.velocity_x *= (1 - OFFTRACK_FRICTION)
            self.velocity_y *= (1 - OFFTRACK_FRICTION)
            self.speed *= (1 - OFFTRACK_FRICTION)
        else:
            # Fricción normal
            self.velocity_x *= (1 - CAR_FRICTION)
            self.velocity_y *= (1 - CAR_FRICTION)
            
        # Actualizar posición
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Detectar derrape
        velocity_angle = math.degrees(math.atan2(self.velocity_x, -self.velocity_y))
        angle_diff = abs(self.angle - velocity_angle)
        self.is_drifting = angle_diff > 15 and abs(self.speed) > SMOKE_SPEED_THRESHOLD
        
    def _check_track_bounds(self, track):
        """Verifica si el coche está en la pista"""
        grid_x = int(self.x / TILE_SIZE)
        grid_y = int(self.y / TILE_SIZE)
        
        if 0 <= grid_y < len(track.grid) and 0 <= grid_x < len(track.grid[0]):
            tile = track.grid[grid_y][grid_x]
            self.is_offtrack = tile not in [1, 2]  # 1=pista, 2=checkpoint
        else:
            self.is_offtrack = True
            
    def _update_sprite(self):
        """Actualiza el sprite rotado"""
        self.surface = pygame.transform.rotate(self.original_surface, -self.angle)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
    def handle_collision(self, normal_x, normal_y):
        """Maneja colisión con rebote"""
        if self.collision_cooldown > 0:
            return
            
        # Reducir velocidad
        self.speed *= COLLISION_SPEED_REDUCTION
        
        # Rebote simple
        dot = self.velocity_x * normal_x + self.velocity_y * normal_y
        self.velocity_x -= 2 * dot * normal_x
        self.velocity_y -= 2 * dot * normal_y
        
        # Aplicar rebote
        self.x += self.velocity_x * 2
        self.y += self.velocity_y * 2
        
        self.collision_cooldown = 200
        
    def pass_checkpoint(self, checkpoint_id):
        """Registra paso por checkpoint"""
        if checkpoint_id == self.checkpoint_passed + 1 or \
           (checkpoint_id == 0 and self.checkpoint_passed == 2):
            self.checkpoint_passed = checkpoint_id
            
            # Si completó todos los checkpoints, nueva vuelta
            if checkpoint_id == 0 and self.checkpoint_passed == 0:
                self.complete_lap()
                
    def complete_lap(self):
        """Completa una vuelta"""
        if self.current_lap_time > 1:  # Mínimo 1 segundo por vuelta
            self.lap_times.append(self.current_lap_time)
            self.current_lap_time = 0
            self.lap += 1
            
            if self.lap > MAX_LAPS:
                self.finished = True
                
    def get_best_lap(self):
        """Obtiene el mejor tiempo de vuelta"""
        if self.lap_times:
            return min(self.lap_times)
        return 0
        
    def get_speed_kmh(self):
        """Obtiene velocidad en km/h"""
        return abs(self.speed) * 10
        
    def draw(self, surface, camera_x, camera_y):
        """Dibuja el coche"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Sombra
        shadow_surf = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 80))
        shadow_rect = shadow_surf.get_rect(center=(screen_x + 3, screen_y + 3))
        surface.blit(shadow_surf, shadow_rect)
        
        # Coche
        screen_rect = self.surface.get_rect(center=(screen_x, screen_y))
        surface.blit(self.surface, screen_rect)
        
    def get_collision_rect(self):
        """Obtiene rectángulo de colisión"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)