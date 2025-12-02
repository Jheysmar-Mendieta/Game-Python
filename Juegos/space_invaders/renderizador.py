"""Clase que maneja todo el renderizado visual del juego"""
import pygame
from config import *

class Renderizador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.fuente_grande = pygame.font.Font(None, 70)
        self.fuente_mediana = pygame.font.Font(None, 40)
        self.fuente_pequeña = pygame.font.Font(None, 30)
    
    def limpiar_pantalla(self):
        """Limpia la pantalla con el color de fondo"""
        self.ventana.fill(NEGRO)
    
    def dibujar_jugador(self, jugador):
        """Dibuja el jugador (nave espacial)"""
        # Cuerpo principal (triángulo)
        puntos = [
            (jugador.x + jugador.ancho // 2, jugador.y),  # Punta
            (jugador.x, jugador.y + jugador.alto),  # Esquina izquierda
            (jugador.x + jugador.ancho, jugador.y + jugador.alto)  # Esquina derecha
        ]
        pygame.draw.polygon(self.ventana, CYAN, puntos)
        pygame.draw.polygon(self.ventana, BLANCO, puntos, 2)
        
        # Cabina
        cabina_x = jugador.x + jugador.ancho // 2 - 8
        cabina_y = jugador.y + 10
        pygame.draw.rect(self.ventana, AZUL, (cabina_x, cabina_y, 16, 12))
    
    def dibujar_alien(self, alien):
        """Dibuja un alien"""
        # Diferentes formas según el tipo
        if alien.tipo == 0:  # Alien tipo 1 (más puntos)
            color = MAGENTA
        elif alien.tipo == 1:  # Alien tipo 2 (puntos medios)
            color = AMARILLO
        else:  # Alien tipo 3 (menos puntos)
            color = VERDE
        
        # Cuerpo
        pygame.draw.rect(self.ventana, color, 
                        (alien.x + 8, alien.y + 8, alien.ancho - 16, alien.alto - 16))
        
        # Antenas
        pygame.draw.rect(self.ventana, color, (alien.x + 5, alien.y, 6, 10))
        pygame.draw.rect(self.ventana, color, (alien.x + alien.ancho - 11, alien.y, 6, 10))
        
        # Ojos
        pygame.draw.circle(self.ventana, BLANCO, (alien.x + 15, alien.y + 15), 4)
        pygame.draw.circle(self.ventana, BLANCO, (alien.x + alien.ancho - 15, alien.y + 15), 4)
        pygame.draw.circle(self.ventana, NEGRO, (alien.x + 15, alien.y + 15), 2)
        pygame.draw.circle(self.ventana, NEGRO, (alien.x + alien.ancho - 15, alien.y + 15), 2)
    
    def dibujar_disparo(self, disparo):
        """Dibuja un disparo"""
        pygame.draw.rect(self.ventana, BLANCO, 
                        (disparo.x, disparo.y, disparo.ancho, disparo.alto))
    
    def dibujar_barrera(self, barrera):
        """Dibuja una barrera"""
        color = barrera.get_color()
        pygame.draw.rect(self.ventana, color, 
                        (barrera.x, barrera.y, barrera.ancho, barrera.alto))
        # Borde
        pygame.draw.rect(self.ventana, VERDE_OSCURO, 
                        (barrera.x, barrera.y, barrera.ancho, barrera.alto), 2)
    
    def mostrar_texto(self, texto, x, y, fuente=None, color=BLANCO):
        """Muestra texto en una posición específica"""
        if fuente is None:
            fuente = self.fuente_mediana
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(x, y))
        self.ventana.blit(superficie, rect)
    
    def dibujar_hud(self, puntuacion, vidas, nivel):
        """Dibuja el HUD con puntuación, vidas y nivel"""
        # Puntuación
        self.ventana.blit(self.fuente_pequeña.render(f"SCORE: {puntuacion}", True, BLANCO), (10, 10))
        
        # Vidas
        self.ventana.blit(self.fuente_pequeña.render(f"LIVES: {vidas}", True, BLANCO), (10, 40))
        
        # Nivel
        self.ventana.blit(self.fuente_pequeña.render(f"LEVEL: {nivel}", True, BLANCO), 
                         (ANCHO - 150, 10))
    
    def dibujar_pantalla_inicio(self):
        """Dibuja la pantalla de inicio"""
        self.limpiar_pantalla()
        self.mostrar_texto("SPACE INVADERS", ANCHO // 2, ALTO // 2 - 100, 
                          self.fuente_grande, VERDE)
        self.mostrar_texto("Flechas ← → para mover", ANCHO // 2, ALTO // 2, 
                          self.fuente_pequeña)
        self.mostrar_texto("ESPACIO para disparar", ANCHO // 2, ALTO // 2 + 40, 
                          self.fuente_pequeña)
        self.mostrar_texto("Presiona ESPACIO para comenzar", ANCHO // 2, ALTO // 2 + 100, 
                          self.fuente_pequeña, AMARILLO)
    
    def dibujar_pantalla_game_over(self, puntuacion, nivel):
        """Dibuja la pantalla de Game Over"""
        self.mostrar_texto("GAME OVER", ANCHO // 2, ALTO // 2 - 80, 
                          self.fuente_grande, ROJO)
        self.mostrar_texto(f"Puntuación Final: {puntuacion}", ANCHO // 2, ALTO // 2 - 10, 
                          self.fuente_mediana)
        self.mostrar_texto(f"Nivel Alcanzado: {nivel}", ANCHO // 2, ALTO // 2 + 30, 
                          self.fuente_mediana)
    
    def dibujar_pantalla_nivel_completado(self, nivel):
        """Dibuja la pantalla de nivel completado"""
        self.limpiar_pantalla()
        self.mostrar_texto("¡NIVEL COMPLETADO!", ANCHO // 2, ALTO // 2 - 40, 
                          self.fuente_grande, VERDE)
        self.mostrar_texto(f"Nivel {nivel}", ANCHO // 2, ALTO // 2 + 20, 
                          self.fuente_mediana, AMARILLO)
        self.mostrar_texto("Preparando siguiente nivel...", ANCHO // 2, ALTO // 2 + 70, 
                          self.fuente_pequeña)
    
    def dibujar_pantalla_ingreso_nombre(self, nombre_actual):
        """Dibuja la pantalla para ingresar nombre (estilo arcade)"""
        self.limpiar_pantalla()
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
        self.mostrar_texto("Guardando puntuación...", ANCHO // 2, ALTO // 2, 
                          self.fuente_mediana, AMARILLO)
    
    def actualizar(self):
        """Actualiza la pantalla"""
        pygame.display.update()