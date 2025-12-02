"""Clase que maneja todo el renderizado visual del juego con sprites"""
import pygame
import math
from config import *

class Renderizador:
    def __init__(self, ventana, sprite_manager):
        self.ventana = ventana
        self.sprite_manager = sprite_manager
        self.fuente_grande = pygame.font.Font(None, 70)
        self.fuente_mediana = pygame.font.Font(None, 40)
        self.fuente_pequeña = pygame.font.Font(None, 30)
        self.fondo = sprite_manager.get_sprite('fondo')
    
    def limpiar_pantalla(self, camara=None):
        """Limpia la pantalla con el fondo"""
        if camara:
            # Efecto parallax - el fondo se mueve más lento
            offset = int(camara.offset_x * 0.3) % ANCHO
            self.ventana.blit(self.fondo, (-offset, 0))
            if offset > 0:
                self.ventana.blit(self.fondo, (ANCHO - offset, 0))
        else:
            self.ventana.blit(self.fondo, (0, 0))
    
    def dibujar_sonic(self, sonic, camara):
        """Dibuja a Sonic con sprites"""
        x_pantalla = camara.aplicar(sonic.x)
        
        # Parpadeo si es invencible
        if sonic.invencible and sonic.tiempo_invencible % 10 < 5:
            return
        
        sprite = sonic.get_sprite_actual()
        self.ventana.blit(sprite, (x_pantalla, sonic.y))
        
        # Indicador de velocidad (partículas)
        if abs(sonic.velocidad_x) > 4 and sonic.en_suelo:
            for i in range(3):
                particula_x = x_pantalla + (sonic.ancho if sonic.mirando_derecha else 0)
                particula_y = sonic.y + sonic.alto - 5
                offset_x = (-10 - i * 5) if sonic.mirando_derecha else (10 + i * 5)
                alpha = 150 - i * 50
                s = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(s, (*CYAN[:3], alpha), (3, 3), 3)
                self.ventana.blit(s, (particula_x + offset_x, particula_y))
    
    def dibujar_plataforma(self, plataforma, camara):
        """Dibuja una plataforma con tiles"""
        x_pantalla = camara.aplicar(plataforma.x)
        
        # Solo dibujar si está visible en pantalla
        if -plataforma.ancho < x_pantalla < ANCHO:
            # Determinar si es plataforma flotante o suelo
            es_suelo = plataforma.y >= ALTO - 100
            
            if es_suelo:
                # Suelo con pasto y tierra
                tile_pasto = self.sprite_manager.get_sprite('pasto')
                tile_tierra = self.sprite_manager.get_sprite('tierra')
                
                # Capa de pasto
                for x in range(0, plataforma.ancho, 20):
                    self.ventana.blit(tile_pasto, (x_pantalla + x, plataforma.y))
                
                # Capas de tierra
                for y in range(20, plataforma.alto, 20):
                    for x in range(0, plataforma.ancho, 20):
                        self.ventana.blit(tile_tierra, (x_pantalla + x, plataforma.y + y))
            else:
                # Plataforma flotante de piedra
                tile_piedra = self.sprite_manager.get_sprite('piedra')
                for y in range(0, plataforma.alto, 20):
                    for x in range(0, plataforma.ancho, 20):
                        self.ventana.blit(tile_piedra, (x_pantalla + x, plataforma.y + y))
                
                # Borde brillante
                pygame.draw.rect(self.ventana, (150, 150, 150), 
                               (x_pantalla, plataforma.y, plataforma.ancho, plataforma.alto), 2)
    
    def dibujar_anillo(self, anillo, camara):
        """Dibuja un anillo con animación de sprite"""
        x_pantalla = camara.aplicar(anillo.x)
        
        if -50 < x_pantalla < ANCHO + 50:
            frames = self.sprite_manager.get_sprite('anillo')
            frame_index = (anillo.angulo // 45) % len(frames)
            sprite = frames[frame_index]
            
            # Centrar el sprite
            self.ventana.blit(sprite, (x_pantalla - 15, anillo.y - 15))
            
            # Efecto de brillo
            if frame_index in [0, 4]:
                s = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 100, 50), (20, 20), 20)
                self.ventana.blit(s, (x_pantalla - 20, anillo.y - 20))
    
    def dibujar_enemigo(self, enemigo, camara):
        """Dibuja un enemigo con sprite"""
        x_pantalla = camara.aplicar(enemigo.x)
        
        if -50 < x_pantalla < ANCHO + 50:
            sprite = self.sprite_manager.get_sprite('enemigo')
            
            # Voltear sprite según dirección
            if enemigo.direccion < 0:
                sprite = pygame.transform.flip(sprite, True, False)
            
            self.ventana.blit(sprite, (x_pantalla - 5, enemigo.y - 10))
    
    def mostrar_texto(self, texto, x, y, fuente=None, color=BLANCO):
        """Muestra texto en una posición específica"""
        if fuente is None:
            fuente = self.fuente_mediana
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(x, y))
        
        # Sombra
        sombra = fuente.render(texto, True, NEGRO)
        self.ventana.blit(sombra, (rect.x + 2, rect.y + 2))
        self.ventana.blit(superficie, rect)
    
    def dibujar_hud(self, anillos, tiempo, nivel):
        """Dibuja el HUD con información del juego"""
        # Fondo semitransparente para el HUD
        hud_bg = pygame.Surface((ANCHO, 80), pygame.SRCALPHA)
        pygame.draw.rect(hud_bg, (0, 0, 0, 120), (0, 0, ANCHO, 80))
        self.ventana.blit(hud_bg, (0, 0))
        
        # Icono de anillo
        anillo_icon = self.sprite_manager.get_sprite('anillo')[0]
        anillo_pequeño = pygame.transform.scale(anillo_icon, (20, 20))
        self.ventana.blit(anillo_pequeño, (10, 15))
        
        # Anillos
        self.ventana.blit(self.fuente_pequeña.render(f"× {anillos}", True, AMARILLO), (35, 10))
        
        # Tiempo
        minutos = tiempo // 60
        segundos = tiempo % 60
        tiempo_color = ROJO if tiempo > 180 else BLANCO
        self.ventana.blit(self.fuente_pequeña.render(f"TIME: {minutos}:{segundos:02d}", True, tiempo_color), 
                         (10, 40))
        
        # Nivel
        self.ventana.blit(self.fuente_pequeña.render(f"ZONE {nivel}", True, CYAN), 
                         (ANCHO - 150, 10))
    
    def dibujar_pantalla_inicio(self):
        """Dibuja la pantalla de inicio"""
        self.limpiar_pantalla()
        
        # Logo de Sonic con efecto
        self.mostrar_texto("SONIC", ANCHO // 2, ALTO // 2 - 100, 
                          self.fuente_grande, AZUL_SONIC)
        self.mostrar_texto("THE HEDGEHOG", ANCHO // 2, ALTO // 2 - 40, 
                          self.fuente_mediana, CYAN)
        
        # Preview de Sonic
        sonic_preview = self.sprite_manager.get_sprite('sonic_idle')
        sonic_grande = pygame.transform.scale(sonic_preview, (80, 80))
        self.ventana.blit(sonic_grande, (ANCHO // 2 - 40, ALTO // 2 - 10))
        
        # Instrucciones
        self.mostrar_texto("← → para mover", ANCHO // 2, ALTO // 2 + 80, 
                          self.fuente_pequeña)
        self.mostrar_texto("ESPACIO para saltar", ANCHO // 2, ALTO // 2 + 110, 
                          self.fuente_pequeña)
        
        # Mensaje parpadeante
        if pygame.time.get_ticks() % 1000 < 500:
            self.mostrar_texto("Presiona ESPACIO para comenzar", ANCHO // 2, ALTO // 2 + 150, 
                              self.fuente_pequeña, AMARILLO)
    
    def dibujar_pantalla_game_over(self, anillos, tiempo, nivel):
        """Dibuja la pantalla de Game Over"""
        # Overlay oscuro
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, ANCHO, ALTO))
        self.ventana.blit(overlay, (0, 0))
        
        self.mostrar_texto("GAME OVER", ANCHO // 2, ALTO // 2 - 80, 
                          self.fuente_grande, ROJO)
        self.mostrar_texto(f"Anillos: {anillos}", ANCHO // 2, ALTO // 2 - 10, 
                          self.fuente_mediana, AMARILLO)
        self.mostrar_texto(f"Tiempo: {tiempo // 60}:{tiempo % 60:02d}", ANCHO // 2, ALTO // 2 + 30, 
                          self.fuente_mediana)
        self.mostrar_texto(f"Zona: {nivel}", ANCHO // 2, ALTO // 2 + 70, 
                          self.fuente_mediana)
    
    def dibujar_pantalla_nivel_completado(self, nivel):
        """Dibuja la pantalla de nivel completado"""
        self.limpiar_pantalla()
        self.mostrar_texto("ZONE COMPLETE!", ANCHO // 2, ALTO // 2 - 40, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto(f"Zona {nivel}", ANCHO // 2, ALTO // 2 + 20, 
                          self.fuente_mediana, CYAN)
        
        # Sonic celebrando
        sonic_preview = self.sprite_manager.get_sprite('sonic_idle')
        sonic_grande = pygame.transform.scale(sonic_preview, (60, 60))
        self.ventana.blit(sonic_grande, (ANCHO // 2 - 30, ALTO // 2 + 60))
    
    def dibujar_pantalla_ingreso_nombre(self, nombre_actual):
        """Dibuja la pantalla para ingresar nombre"""
        self.limpiar_pantalla()
        self.mostrar_texto("¡NUEVO RECORD!", ANCHO // 2, ALTO // 2 - 100, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto("Tus iniciales:", ANCHO // 2, ALTO // 2 - 30, 
                          self.fuente_mediana)
        
        nombre_display = nombre_actual + "_" * (3 - len(nombre_actual))
        self.mostrar_texto(nombre_display, ANCHO // 2, ALTO // 2 + 30, 
                          self.fuente_grande, AZUL_SONIC)
        
        self.mostrar_texto("A-Z para escribir, ENTER confirmar", ANCHO // 2, ALTO // 2 + 100, 
                          self.fuente_pequeña, CYAN)
    
    def dibujar_pantalla_guardando(self):
        """Muestra mensaje de guardando"""
        self.limpiar_pantalla()
        self.mostrar_texto("Guardando...", ANCHO // 2, ALTO // 2, 
                          self.fuente_mediana, AMARILLO)
    
    def actualizar(self):
        """Actualiza la pantalla"""
        pygame.display.update()