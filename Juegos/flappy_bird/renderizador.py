"""Clase que maneja todo el renderizado visual del juego"""
import pygame
import math
from config import *

class Renderizador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.fuente_grande = pygame.font.Font(None, 70)
        self.fuente_mediana = pygame.font.Font(None, 50)
        self.fuente_pequeña = pygame.font.Font(None, 30)
        self.altura_suelo = 50
    
    def limpiar_pantalla(self):
        """Limpia la pantalla con el color del cielo"""
        self.ventana.fill(CIELO)
    
    def dibujar_suelo(self):
        """Dibuja el suelo"""
        pygame.draw.rect(self.ventana, SUELO, 
                        (0, ALTO - self.altura_suelo, ANCHO, self.altura_suelo))
        # Línea de pasto
        pygame.draw.line(self.ventana, VERDE, 
                        (0, ALTO - self.altura_suelo), 
                        (ANCHO, ALTO - self.altura_suelo), 3)
    
    def dibujar_pajaro(self, pajaro):
        """Dibuja el pájaro con efecto de rotación"""
        # Cuerpo (círculo amarillo)
        pygame.draw.circle(self.ventana, AMARILLO, 
                          (int(pajaro.x), int(pajaro.y)), pajaro.radio)
        pygame.draw.circle(self.ventana, (200, 150, 0), 
                          (int(pajaro.x), int(pajaro.y)), pajaro.radio, 2)
        
        # Ojo
        ojo_x = pajaro.x + 5
        ojo_y = pajaro.y - 3
        pygame.draw.circle(self.ventana, BLANCO, (int(ojo_x), int(ojo_y)), 4)
        pygame.draw.circle(self.ventana, NEGRO, (int(ojo_x), int(ojo_y)), 2)
        
        # Pico
        if pajaro.vivo:
            pico_puntos = [
                (pajaro.x + pajaro.radio, pajaro.y),
                (pajaro.x + pajaro.radio + 8, pajaro.y - 3),
                (pajaro.x + pajaro.radio + 8, pajaro.y + 3)
            ]
            pygame.draw.polygon(self.ventana, (255, 100, 0), pico_puntos)
    
    def dibujar_tubo(self, tubo):
        """Dibuja un tubo"""
        # Tubo superior
        pygame.draw.rect(self.ventana, VERDE, tubo.get_rect_superior())
        pygame.draw.rect(self.ventana, VERDE_OSCURO, tubo.get_rect_superior(), 3)
        
        # Borde superior del tubo
        borde_superior = pygame.Rect(tubo.x - 5, tubo.y_hueco - 20, tubo.ancho + 10, 20)
        pygame.draw.rect(self.ventana, VERDE, borde_superior)
        pygame.draw.rect(self.ventana, VERDE_OSCURO, borde_superior, 3)
        
        # Tubo inferior
        pygame.draw.rect(self.ventana, VERDE, tubo.get_rect_inferior())
        pygame.draw.rect(self.ventana, VERDE_OSCURO, tubo.get_rect_inferior(), 3)
        
        # Borde inferior del tubo
        borde_inferior = pygame.Rect(tubo.x - 5, tubo.y_hueco + tubo.altura_hueco, 
                                     tubo.ancho + 10, 20)
        pygame.draw.rect(self.ventana, VERDE, borde_inferior)
        pygame.draw.rect(self.ventana, VERDE_OSCURO, borde_inferior, 3)
    
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
    
    def dibujar_puntuacion(self, puntuacion):
        """Dibuja la puntuación actual"""
        self.mostrar_texto(str(puntuacion), ANCHO // 2, 50, self.fuente_grande)
    
    def dibujar_pantalla_inicio(self):
        """Dibuja la pantalla de inicio"""
        self.limpiar_pantalla()
        self.dibujar_suelo()
        
        self.mostrar_texto("FLAPPY BIRD", ANCHO // 2, ALTO // 2 - 80, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto("Presiona ESPACIO para saltar", ANCHO // 2, ALTO // 2, 
                          self.fuente_pequeña, BLANCO)
        self.mostrar_texto("Presiona ESPACIO para empezar", ANCHO // 2, ALTO // 2 + 50, 
                          self.fuente_pequeña, AZUL)
    
    def dibujar_pantalla_game_over(self, puntuacion, mejor_puntuacion):
        """Dibuja la pantalla de Game Over"""
        self.mostrar_texto("GAME OVER", ANCHO // 2, ALTO // 2 - 100, 
                          self.fuente_grande, ROJO)
        self.mostrar_texto(f"Puntuación: {puntuacion}", ANCHO // 2, ALTO // 2 - 30, 
                          self.fuente_mediana)
        self.mostrar_texto(f"Mejor: {mejor_puntuacion}", ANCHO // 2, ALTO // 2 + 10, 
                          self.fuente_mediana)
    
    def dibujar_pantalla_ingreso_nombre(self, nombre_actual):
        """Dibuja la pantalla para ingresar nombre (estilo arcade)"""
        self.limpiar_pantalla()
        self.dibujar_suelo()
        
        self.mostrar_texto("¡NUEVO RECORD!", ANCHO // 2, ALTO // 2 - 100, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto("Tus iniciales:", ANCHO // 2, ALTO // 2 - 30, 
                          self.fuente_mediana)
        
        # Mostrar el nombre con espacios para las 3 letras
        nombre_display = nombre_actual + "_" * (3 - len(nombre_actual))
        self.mostrar_texto(nombre_display, ANCHO // 2, ALTO // 2 + 30, 
                          self.fuente_grande, VERDE)
        
        self.mostrar_texto("A-Z para escribir, ENTER confirmar", ANCHO // 2, ALTO // 2 + 100, 
                          self.fuente_pequeña, AZUL)
    
    def dibujar_pantalla_guardando(self):
        """Muestra mensaje de guardando"""
        self.limpiar_pantalla()
        self.dibujar_suelo()
        self.mostrar_texto("Guardando...", ANCHO // 2, ALTO // 2, 
                          self.fuente_mediana, AMARILLO)
    
    def get_altura_suelo(self):
        """Retorna la altura del suelo"""
        return ALTO - self.altura_suelo
    
    def actualizar(self):
        """Actualiza la pantalla"""
        pygame.display.update()