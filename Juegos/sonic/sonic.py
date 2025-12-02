"""Clase que maneja la lógica de Sonic con animaciones"""
import pygame
from config import *

class Sonic:
    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.ancho = SONIC_ANCHO
        self.alto = SONIC_ALTO
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.en_suelo = False
        self.mirando_derecha = True
        self.vivo = True
        self.invencible = False
        self.tiempo_invencible = 0
        
        # Coyote time - permite saltar justo después de caer
        self.coyote_time = 0
        self.coyote_time_max = 6  # frames
        
        # Animación
        self.sprite_manager = sprite_manager
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 5
    
    def mover_izquierda(self):
        """Acelera hacia la izquierda"""
        self.velocidad_x -= ACELERACION
        self.mirando_derecha = False
    
    def mover_derecha(self):
        """Acelera hacia la derecha"""
        self.velocidad_x += ACELERACION
        self.mirando_derecha = True
    
    def saltar(self):
        """Hace que Sonic salte"""
        # Permite saltar si está en el suelo O dentro del coyote time
        if self.en_suelo or self.coyote_time > 0:
            self.velocidad_y = FUERZA_SALTO
            self.en_suelo = False
            self.coyote_time = 0
    
    def actualizar(self, plataformas):
        """Actualiza la física de Sonic"""
        # Aplicar fricción
        self.velocidad_x *= FRICCION
        
        # Limitar velocidad máxima
        if self.velocidad_x > VELOCIDAD_MAXIMA:
            self.velocidad_x = VELOCIDAD_MAXIMA
        elif self.velocidad_x < -VELOCIDAD_MAXIMA:
            self.velocidad_x = -VELOCIDAD_MAXIMA
        
        # Aplicar gravedad
        if not self.en_suelo:
            self.velocidad_y += GRAVEDAD
        
        # Limitar velocidad de caída
        if self.velocidad_y > 20:
            self.velocidad_y = 20
        
        # Actualizar posición horizontal
        self.x += self.velocidad_x
        
        # Colisiones horizontales
        rect_sonic = self.get_rect()
        for plataforma in plataformas:
            if rect_sonic.colliderect(plataforma.get_rect()):
                if self.velocidad_x > 0:  # Moviendo a la derecha
                    self.x = plataforma.x - self.ancho
                elif self.velocidad_x < 0:  # Moviendo a la izquierda
                    self.x = plataforma.x + plataforma.ancho
                self.velocidad_x = 0
        
        # Actualizar posición vertical
        self.y += self.velocidad_y
        
        # Guardar estado anterior del suelo
        estaba_en_suelo = self.en_suelo
        self.en_suelo = False
        
        # Colisiones verticales - MEJORADO
        rect_sonic = self.get_rect()
        for plataforma in plataformas:
            plat_rect = plataforma.get_rect()
            if rect_sonic.colliderect(plat_rect):
                if self.velocidad_y > 0:  # Cayendo
                    # Verificar que realmente está cayendo sobre la plataforma
                    if self.y < plataforma.y:
                        self.y = plataforma.y - self.alto
                        self.velocidad_y = 0
                        self.en_suelo = True
                elif self.velocidad_y < 0:  # Subiendo
                    # Golpear desde abajo
                    if self.y > plataforma.y:
                        self.y = plataforma.y + plataforma.alto
                        self.velocidad_y = 0
        
        # Actualizar coyote time
        if self.en_suelo:
            self.coyote_time = self.coyote_time_max
        elif estaba_en_suelo and not self.en_suelo:
            # Justo salió de una plataforma, activar coyote time
            self.coyote_time = self.coyote_time_max
        elif self.coyote_time > 0:
            self.coyote_time -= 1
        
        # Verificar caída al vacío
        if self.y > ALTO:
            self.vivo = False
        
        # Actualizar invencibilidad
        if self.invencible:
            self.tiempo_invencible -= 1
            if self.tiempo_invencible <= 0:
                self.invencible = False
        
        # Actualizar animación
        self.actualizar_animacion()
    
    def actualizar_animacion(self):
        """Actualiza el frame de animación"""
        if abs(self.velocidad_x) > 1 and self.en_suelo:
            self.contador_animacion += 1
            if self.contador_animacion >= self.velocidad_animacion:
                self.contador_animacion = 0
                self.frame_actual = (self.frame_actual + 1) % 4
        else:
            self.frame_actual = 0
            self.contador_animacion = 0
    
    def get_sprite_actual(self):
        """Obtiene el sprite actual según el estado"""
        if not self.en_suelo:
            sprite = self.sprite_manager.get_sprite('sonic_jump')
        elif abs(self.velocidad_x) > 1:
            sprites = self.sprite_manager.get_sprite('sonic_run')
            sprite = sprites[self.frame_actual]
        else:
            sprite = self.sprite_manager.get_sprite('sonic_idle')
        
        # Voltear sprite si mira a la izquierda
        if not self.mirando_derecha:
            sprite = pygame.transform.flip(sprite, True, False)
        
        return sprite
    
    def activar_invencibilidad(self):
        """Activa invencibilidad temporal"""
        self.invencible = True
        self.tiempo_invencible = 120  # 2 segundos a 60 FPS
    
    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def morir(self):
        """Marca a Sonic como muerto"""
        self.vivo = False