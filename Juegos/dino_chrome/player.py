"""Clase del jugador (Dinosaurio)"""
import pygame
from settings import *
from sprites import SpriteGenerator


class Player:
    """Representa al dinosaurio jugador"""
    
    def __init__(self):
        # Sprites
        self.run_sprites = [
            SpriteGenerator.create_dino_run1(),
            SpriteGenerator.create_dino_run2()
        ]
        self.dead_sprite = SpriteGenerator.create_dino_dead()
        
        # Posición y física
        self.x = DINO_X
        self.y = DINO_GROUND_Y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_dead = False
        
        # Animación
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # segundos por frame
        
        # Rectángulo de colisión (más pequeño que el sprite para mejor jugabilidad)
        self.rect = pygame.Rect(self.x + 5, self.y + 5, DINO_WIDTH - 10, DINO_HEIGHT - 10)
    
    def jump(self):
        """Hace que el dinosaurio salte"""
        if not self.is_jumping and not self.is_dead:
            self.is_jumping = True
            self.velocity_y = DINO_JUMP_VELOCITY
    
    def update(self, delta_time):
        """Actualiza el estado del dinosaurio"""
        if self.is_dead:
            return
        
        # Aplicar gravedad
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
            
            # Aterrizar
            if self.y >= DINO_GROUND_Y:
                self.y = DINO_GROUND_Y
                self.velocity_y = 0
                self.is_jumping = False
        
        # Actualizar animación de correr
        if not self.is_jumping:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.run_sprites)
        
        # Actualizar rectángulo de colisión
        self.rect.y = int(self.y) + 5
    
    def draw(self, screen, night_mode=False):
        """Dibuja el dinosaurio"""
        if self.is_dead:
            sprite = self.dead_sprite
        else:
            sprite = self.run_sprites[self.animation_index]
        
        # Recolorear para modo noche
        if night_mode:
            colored_sprite = sprite.copy()
            pixels = pygame.surfarray.pixels3d(colored_sprite)
            # Cambiar color gris oscuro a gris claro para modo noche
            mask = (pixels[:, :, 0] == 83) & (pixels[:, :, 1] == 83) & (pixels[:, :, 2] == 83)
            pixels[mask] = [150, 150, 150]
            del pixels
            screen.blit(colored_sprite, (int(self.x), int(self.y)))
        else:
            screen.blit(sprite, (int(self.x), int(self.y)))
    
    def die(self):
        """Marca al dinosaurio como muerto"""
        self.is_dead = True
    
    def reset(self):
        """Reinicia el estado del dinosaurio"""
        self.y = DINO_GROUND_Y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_dead = False
        self.animation_index = 0
        self.animation_timer = 0
    
    def get_collision_rect(self):
        """Retorna el rectángulo de colisión"""
        return self.rect