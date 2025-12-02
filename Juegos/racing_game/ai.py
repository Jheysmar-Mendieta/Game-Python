"""Sistema de IA para coches rivales"""
import math
import random
from config import *


class AIController:
    """Controla un coche de IA"""
    
    def __init__(self, car, track, aggression=0.5):
        self.car = car
        self.track = track
        self.aggression = aggression  # 0.0 = conservadora, 1.0 = agresiva
        
        self.current_waypoint = 0
        self.reaction_timer = 0
        self.stuck_timer = 0
        self.last_position = (car.x, car.y)
        
        # Parámetros basados en agresión
        self.target_speed = AI_BASE_SPEED * (0.8 + aggression * 0.4)
        self.brake_distance = 100 * (1.5 - aggression * 0.5)
        self.overtake_probability = aggression
        
    def update(self, dt, all_cars):
        """Actualiza control de IA"""
        self.reaction_timer += dt
        
        # Reaccionar cada cierto tiempo
        if self.reaction_timer < AI_REACTION_TIME * 1000:
            return
            
        self.reaction_timer = 0
        
        # Verificar si está atascado
        self._check_stuck(dt)
        
        # Obtener waypoint objetivo
        target = self._get_target_waypoint()
        
        # Calcular dirección al objetivo
        dx = target[0] - self.car.x
        dy = target[1] - self.car.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 50:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.track.ai_path)
            
        # Calcular ángulo objetivo
        target_angle = math.degrees(math.atan2(dx, -dy))
        
        # Normalizar diferencia de ángulo
        angle_diff = target_angle - self.car.angle
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
            
        # Control de dirección
        self.car.turning_left = angle_diff < -5
        self.car.turning_right = angle_diff > 5
        
        # Control de aceleración
        current_speed = abs(self.car.speed)
        
        # Frenar en curvas cerradas
        should_brake = abs(angle_diff) > 45 or self._check_obstacles_ahead(all_cars)
        
        if should_brake:
            self.car.braking = True
            self.car.accelerating = False
        elif current_speed < self.target_speed:
            self.car.accelerating = True
            self.car.braking = False
        else:
            self.car.accelerating = False
            self.car.braking = False
            
        # Intentar adelantamientos
        if random.random() < self.overtake_probability * 0.01:
            self._attempt_overtake(all_cars)
            
    def _get_target_waypoint(self):
        """Obtiene el waypoint objetivo"""
        if not self.track.ai_path:
            return (self.car.x, self.car.y)
            
        # Mirar varios waypoints adelante según agresión
        lookahead = int(2 + self.aggression * 3)
        target_idx = (self.current_waypoint + lookahead) % len(self.track.ai_path)
        
        return self.track.ai_path[target_idx]
        
    def _check_obstacles_ahead(self, all_cars):
        """Verifica si hay obstáculos adelante"""
        for other_car in all_cars:
            if other_car == self.car:
                continue
                
            # Calcular distancia
            dx = other_car.x - self.car.x
            dy = other_car.y - self.car.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.brake_distance:
                # Verificar si está adelante
                angle_to_car = math.degrees(math.atan2(dx, -dy))
                angle_diff = abs(angle_to_car - self.car.angle)
                
                if angle_diff < 45:
                    return True
                    
        return False
        
    def _attempt_overtake(self, all_cars):
        """Intenta maniobra de adelantamiento"""
        for other_car in all_cars:
            if other_car == self.car:
                continue
                
            dx = other_car.x - self.car.x
            dy = other_car.y - self.car.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 80:
                # Intentar esquivar
                if random.random() > 0.5:
                    self.car.turning_left = True
                    self.car.turning_right = False
                else:
                    self.car.turning_right = True
                    self.car.turning_left = False
                    
    def _check_stuck(self, dt):
        """Verifica si el coche está atascado"""
        dx = self.car.x - self.last_position[0]
        dy = self.car.y - self.last_position[1]
        movement = math.sqrt(dx*dx + dy*dy)
        
        if movement < 1 and abs(self.car.speed) > 1:
            self.stuck_timer += dt
            
            if self.stuck_timer > 2000:  # Atascado por 2 segundos
                # Retroceder
                self.car.braking = True
                self.car.accelerating = False
                self.car.speed = -3
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0
            
        self.last_position = (self.car.x, self.car.y)