"""Clase que maneja todo el renderizado visual del juego"""
import pygame
from config import *

class Renderizador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.fuente_grande = pygame.font.Font(None, 60)
        self.fuente_mediana = pygame.font.Font(None, 40)
        self.fuente_pequeña = pygame.font.Font(None, 30)
        self.fuente_mini = pygame.font.Font(None, 24)
    
    def limpiar_pantalla(self):
        """Limpia la pantalla con el color de fondo"""
        self.ventana.fill(NEGRO)
    
    def dibujar_cuadricula(self):
        """Dibuja una cuadrícula sutil de fondo"""
        for i in range(0, ANCHO, TAM):
            pygame.draw.line(self.ventana, GRIS_OSCURO, (i, 0), (i, ALTO))
        for i in range(0, ALTO, TAM):
            pygame.draw.line(self.ventana, GRIS_OSCURO, (0, i), (ANCHO, i))
    
    def dibujar_serpiente(self, serpiente):
        """Dibuja la serpiente con efecto visual"""
        cuerpo = serpiente.get_cuerpo()
        for i, (x, y) in enumerate(cuerpo):
            if i == len(cuerpo) - 1:  # Cabeza
                pygame.draw.rect(self.ventana, VERDE, (x, y, TAM, TAM))
                pygame.draw.rect(self.ventana, VERDE_OSCURO, (x, y, TAM, TAM), 2)
            else:  # Cuerpo
                pygame.draw.rect(self.ventana, VERDE_OSCURO, (x, y, TAM, TAM))
                pygame.draw.rect(self.ventana, VERDE, (x, y, TAM, TAM), 2)
    
    def dibujar_manzana_veneno(self, manzana):
        """Dibuja la manzana buena"""
        x, y = manzana.get_posicion()
        pygame.draw.circle(self.ventana, VERDE, (x + TAM//2, y + TAM//2), TAM//2)
        pygame.draw.circle(self.ventana, VERDE_OSCURO, (x + TAM//2, y + TAM//2), TAM//2, 2)
    
    def dibujar_manzana(self, manzana):
        """Dibuja la manzana venenosa (roja)"""
        x, y = manzana.get_posicion()
        pygame.draw.circle(self.ventana, ROJO, (x + TAM//2, y + TAM//2), TAM//2)
        pygame.draw.circle(self.ventana, (150, 0, 0), (x + TAM//2, y + TAM//2), TAM//2, 2)
    
    def dibujar_obstaculos(self, obstaculos):
        """Dibuja los obstáculos del modo laberinto"""
        for x, y in obstaculos:
            pygame.draw.rect(self.ventana, MORADO, (x, y, TAM, TAM))
            pygame.draw.rect(self.ventana, (100, 0, 150), (x, y, TAM, TAM), 2)
    
    def mostrar_texto(self, texto, x, y, fuente=None, color=BLANCO):
        """Muestra texto en una posición específica"""
        if fuente is None:
            fuente = self.fuente_mediana
        superficie = fuente.render(texto, True, color)
        self.ventana.blit(superficie, (x, y))
    
    def dibujar_menu_modos(self, mejores_puntajes):
        """Dibuja el menú de selección de modos"""
        self.limpiar_pantalla()
        
        # Título
        self.mostrar_texto("SNAKE GAME", ANCHO//2 - 150, 30, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto("Selecciona un Modo de Juego", ANCHO//2 - 180, 100, 
                          self.fuente_mediana, BLANCO)
        
        # Dibujar cada modo como un botón
        y_pos = 160
        x_izq = 50
        x_der = ANCHO // 2 + 50
        
        modos_lista = list(MODOS_JUEGO.items())
        
        for i, (key, modo) in enumerate(modos_lista):
            # Alternar entre izquierda y derecha
            x = x_izq if i % 2 == 0 else x_der
            if i % 2 == 0 and i > 0:
                y_pos += 120
            
            # Cuadro del modo
            ancho_cuadro = 330
            alto_cuadro = 100
            pygame.draw.rect(self.ventana, modo['color'], 
                           (x, y_pos, ancho_cuadro, alto_cuadro), 3)
            
            # Número de tecla
            self.mostrar_texto(f"[{i+1}]", x + 10, y_pos + 10, 
                             self.fuente_mediana, modo['color'])
            
            # Nombre del modo con ícono
            self.mostrar_texto(f"{modo['icono']} {modo['nombre']}", 
                             x + 70, y_pos + 10, 
                             self.fuente_mediana, BLANCO)
            
            # Descripción (color gris claro)
            color_desc = (120, 120, 120)
            self.mostrar_texto(modo['descripcion'], x + 10, y_pos + 50, 
                             self.fuente_mini, color_desc)
            
            # Mejor puntaje si existe
            if key in mejores_puntajes:
                self.mostrar_texto(f"Mejor: {mejores_puntajes[key]}", 
                                 x + 10, y_pos + 73, 
                                 self.fuente_mini, AMARILLO)
        
        # Instrucciones
        self.mostrar_texto("Presiona el número del modo que quieras jugar", 
                          ANCHO//2 - 220, ALTO - 40, 
                          self.fuente_pequeña, AZUL)
    
    def dibujar_hud_modo(self, puntaje, mejor_puntaje, nombre_modo):
        """Dibuja el HUD con nombre del modo"""
        self.mostrar_texto(f"Modo: {nombre_modo}", 10, 10, self.fuente_pequeña, CYAN)
        self.mostrar_texto(f"Puntaje: {puntaje}", 10, 40, self.fuente_mediana)
        self.mostrar_texto(f"Mejor: {mejor_puntaje}", 10, 75, self.fuente_mediana)
        self.mostrar_texto("P = Puntajes", ANCHO - 160, 10, self.fuente_mini, AZUL)
    
    def dibujar_hud_tiempo(self, puntaje, mejor_puntaje, tiempo, nombre_modo):
        """Dibuja el HUD para modo contra reloj"""
        self.mostrar_texto(f"Modo: {nombre_modo}", 10, 10, self.fuente_pequeña, NARANJA)
        self.mostrar_texto(f"Tiempo: {tiempo}s", ANCHO//2 - 80, 10, 
                          self.fuente_grande, ROJO if tiempo <= 10 else AMARILLO)
        self.mostrar_texto(f"Puntaje: {puntaje}", 10, 50, self.fuente_mediana)
        self.mostrar_texto(f"Mejor: {mejor_puntaje}", 10, 85, self.fuente_mediana)
    
    def dibujar_tabla_puntajes(self, puntajes, nombre_modo):
        """Dibuja la tabla con los 10 mejores puntajes del modo"""
        self.limpiar_pantalla()
        
        # Título
        self.mostrar_texto(f"TOP 10 - {nombre_modo.upper()}", ANCHO//2 - 180, 30, 
                          self.fuente_grande, AMARILLO)
        
        pygame.draw.line(self.ventana, AMARILLO, (100, 90), (ANCHO - 100, 90), 3)
        
        # Encabezados
        y_inicio = 120
        self.mostrar_texto("POS", 100, y_inicio, self.fuente_mediana, AZUL)
        self.mostrar_texto("JUGADOR", 200, y_inicio, self.fuente_mediana, AZUL)
        self.mostrar_texto("PUNTOS", 450, y_inicio, self.fuente_mediana, AZUL)
        self.mostrar_texto("FECHA", 570, y_inicio, self.fuente_mediana, AZUL)
        
        pygame.draw.line(self.ventana, AZUL, (100, y_inicio + 35), 
                        (ANCHO - 100, y_inicio + 35), 2)
        
        # Mostrar puntajes
        y_pos = y_inicio + 50
        
        if not puntajes:
            self.mostrar_texto("No hay puntajes registrados aún", 
                              ANCHO//2 - 180, ALTO//2, 
                              self.fuente_mediana, BLANCO)
        else:
            for i, (username, score, fecha) in enumerate(puntajes, 1):
                if i == 1:
                    color = (255, 215, 0)  # Oro
                elif i == 2:
                    color = (192, 192, 192)  # Plata
                elif i == 3:
                    color = (205, 127, 50)  # Bronce
                else:
                    color = BLANCO
                
                fecha_str = str(fecha).split()[0] if fecha else "N/A"
                
                self.mostrar_texto(f"{i}.", 110, y_pos, self.fuente_pequeña, color)
                self.mostrar_texto(username, 200, y_pos, self.fuente_pequeña, color)
                self.mostrar_texto(str(score), 450, y_pos, self.fuente_pequeña, color)
                self.mostrar_texto(fecha_str, 570, y_pos, self.fuente_pequeña, color)
                
                y_pos += 35
        
        pygame.draw.line(self.ventana, BLANCO, (100, ALTO - 80), 
                        (ANCHO - 100, ALTO - 80), 2)
        self.mostrar_texto("Presiona ESC o P para cerrar", 
                          ANCHO//2 - 160, ALTO - 50, 
                          self.fuente_pequeña, VERDE)
    
    def dibujar_pantalla_game_over_modo(self, puntaje, mejor_puntaje, nombre_modo):
        """Dibuja la pantalla de Game Over con el modo"""
        self.limpiar_pantalla()
        self.mostrar_texto("GAME OVER", ANCHO//2 - 120, ALTO//2 - 100, 
                          self.fuente_grande, ROJO)
        self.mostrar_texto(f"Modo: {nombre_modo}", ANCHO//2 - 80, ALTO//2 - 40, 
                          self.fuente_pequeña, CYAN)
        self.mostrar_texto(f"Puntaje: {puntaje}", ANCHO//2 - 80, ALTO//2, 
                          self.fuente_mediana)
        self.mostrar_texto(f"Mejor: {mejor_puntaje}", ANCHO//2 - 80, ALTO//2 + 40, 
                          self.fuente_mediana)
        
        self.mostrar_texto("ESPACIO = Jugar otra vez", 
                          ANCHO//2 - 170, ALTO//2 + 100, 
                          self.fuente_pequeña, AZUL)
        self.mostrar_texto("ESC = Menú principal", 
                          ANCHO//2 - 140, ALTO//2 + 130, 
                          self.fuente_pequeña, AZUL)
    
    def dibujar_pantalla_ingreso_nombre(self, nombre_actual):
        """Dibuja la pantalla para ingresar nombre"""
        self.limpiar_pantalla()
        self.mostrar_texto("NUEVO RECORD!", ANCHO//2 - 140, ALTO//2 - 120, 
                          self.fuente_grande, AMARILLO)
        self.mostrar_texto("Ingresa tus iniciales:", ANCHO//2 - 140, ALTO//2 - 40, 
                          self.fuente_mediana)
        
        nombre_display = nombre_actual + "_" * (3 - len(nombre_actual))
        self.mostrar_texto(nombre_display, ANCHO//2 - 45, ALTO//2 + 20, 
                          self.fuente_grande, VERDE)
        
        self.mostrar_texto("(A-Z para escribir, ENTER para confirmar)", 
                          ANCHO//2 - 220, ALTO//2 + 100, self.fuente_pequeña, AZUL)
    
    def dibujar_pantalla_guardando(self):
        """Muestra mensaje de guardando"""
        self.limpiar_pantalla()
        self.mostrar_texto("Guardando puntuación...", ANCHO//2 - 150, ALTO//2, 
                          self.fuente_mediana, AMARILLO)
    
    def actualizar(self):
        """Actualiza la pantalla"""
        pygame.display.update()