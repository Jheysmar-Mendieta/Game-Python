"""Juego Snake con múltiples modos"""
import pygame
import time
from config import *
from serpiente import Serpiente
from manzana import Manzana
from renderizador import Renderizador
from db import DatabaseManager


class Juego:
    """Clase principal que maneja la lógica del juego"""
    
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.renderizador = Renderizador(self.ventana)
        self.db = DatabaseManager()
        self.jugando = True
        self.mostrando_puntajes = False
        self.modo_actual = None
        self.mejores_puntajes = {}  # Guardará el mejor puntaje de cada modo
    
    def cargar_mejores_puntajes(self):
        """Carga los mejores puntajes de cada modo"""
        for key, modo in MODOS_JUEGO.items():
            # Obtenemos todos los puntajes de Snake y filtramos por modo
            top = self.db.obtener_top_puntuaciones("Snake", 100)
            # Filtrar solo los que corresponden a este modo
            puntajes_modo = [p for p in top if p[0].endswith(f"-{modo['nombre']}")]
            if puntajes_modo:
                self.mejores_puntajes[key] = puntajes_modo[0][1]
            else:
                self.mejores_puntajes[key] = 0
    
    def menu_modos(self):
        """Muestra el menú de selección de modos"""
        self.cargar_mejores_puntajes()
        seleccionando = True
        
        while seleccionando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                
                if evento.type == pygame.KEYDOWN:
                    # Teclas 1-6 para seleccionar modo
                    if evento.key == pygame.K_1:
                        return 'clasico'
                    elif evento.key == pygame.K_2:
                        return 'velocidad'
                    elif evento.key == pygame.K_3:
                        return 'portal'
                    elif evento.key == pygame.K_4:
                        return 'laberinto'
                    elif evento.key == pygame.K_5:
                        return 'veneno'
                    elif evento.key == pygame.K_6:
                        return 'tiempo'
            
            self.renderizador.dibujar_menu_modos(self.mejores_puntajes)
            self.renderizador.actualizar()
            self.clock.tick(FPS)
        
        return None
    
    def nueva_partida(self, modo):
        """Inicializa una nueva partida según el modo"""
        self.modo_actual = modo
        x = ANCHO // 2
        y = ALTO // 2
        self.serpiente = Serpiente(x, y)
        self.manzana = Manzana()
        self.puntaje = 0
        self.fps_actual = FPS
        
        # Variables específicas del modo
        self.manzana_veneno = None
        self.obstaculos = []
        self.tiempo_inicio = None
        self.tiempo_restante = 60
        
        # Configurar según el modo
        if modo == 'veneno':
            self.manzana_veneno = Manzana()
            self.manzana_veneno.generar_nueva_posicion(
                self.serpiente.get_cuerpo() + [self.manzana.get_posicion()]
            )
        
        elif modo == 'laberinto':
            self.generar_obstaculos()
        
        elif modo == 'tiempo':
            self.tiempo_inicio = time.time()
    
    def generar_obstaculos(self):
        """Genera obstáculos aleatorios para el modo laberinto"""
        import random
        self.obstaculos = []
        num_obstaculos = 15
        
        for _ in range(num_obstaculos):
            while True:
                x = random.randrange(0, ANCHO, TAM)
                y = random.randrange(0, ALTO, TAM)
                pos = (x, y)
                
                # Verificar que no esté en la serpiente o manzana
                if (pos not in self.serpiente.get_cuerpo() and 
                    pos != self.manzana.get_posicion() and
                    pos not in self.obstaculos):
                    self.obstaculos.append(pos)
                    break
    
    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                # Tecla P para mostrar puntajes
                if evento.key == pygame.K_p:
                    self.mostrar_tabla_puntajes()
                    
                elif evento.key == pygame.K_UP:
                    self.serpiente.cambiar_direccion(0, -TAM)
                elif evento.key == pygame.K_DOWN:
                    self.serpiente.cambiar_direccion(0, TAM)
                elif evento.key == pygame.K_LEFT:
                    self.serpiente.cambiar_direccion(-TAM, 0)
                elif evento.key == pygame.K_RIGHT:
                    self.serpiente.cambiar_direccion(TAM, 0)
        
        return True
    
    def mostrar_tabla_puntajes(self):
        """Muestra una ventana con los 10 mejores puntajes del modo actual"""
        self.mostrando_puntajes = True
        
        nombre_modo = MODOS_JUEGO[self.modo_actual]['nombre']
        # Obtener todos los puntajes de Snake y filtrar por modo
        todos_puntajes = self.db.obtener_top_puntuaciones("Snake", 100)
        # Filtrar solo los del modo actual y limpiar el nombre
        top_puntajes = []
        for username, score, fecha in todos_puntajes:
            if username.endswith(f"-{nombre_modo}"):
                # Remover el sufijo del modo para mostrar solo iniciales
                username_limpio = username.replace(f"-{nombre_modo}", "")
                top_puntajes.append((username_limpio, score, fecha))
        
        # Limitar a top 10
        top_puntajes = top_puntajes[:10]
        
        while self.mostrando_puntajes:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                    self.mostrando_puntajes = False
                    return
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_p:
                        self.mostrando_puntajes = False
            
            self.renderizador.dibujar_tabla_puntajes(top_puntajes, nombre_modo)
            self.renderizador.actualizar()
            self.clock.tick(FPS)
    
    def actualizar_logica(self):
        """Actualiza la lógica del juego según el modo"""
        self.serpiente.mover()
        
        # Modo contra reloj: actualizar tiempo
        if self.modo_actual == 'tiempo':
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            self.tiempo_restante = max(0, 60 - int(tiempo_transcurrido))
            if self.tiempo_restante <= 0:
                return False
        
        # Verificar colisiones según el modo
        if self.modo_actual == 'portal':
            # En modo portal, teletransportar en los bordes
            cabeza = list(self.serpiente.get_cabeza())
            if cabeza[0] < 0:
                cabeza[0] = ANCHO - TAM
            elif cabeza[0] >= ANCHO:
                cabeza[0] = 0
            if cabeza[1] < 0:
                cabeza[1] = ALTO - TAM
            elif cabeza[1] >= ALTO:
                cabeza[1] = 0
            
            self.serpiente.cuerpo[-1] = tuple(cabeza)
        else:
            # En otros modos, colisión con borde = game over
            if self.serpiente.colisiona_con_borde():
                return False
        
        # Colisión consigo misma
        if self.serpiente.colisiona_consigo_misma():
            return False
        
        # Modo laberinto: colisión con obstáculos
        if self.modo_actual == 'laberinto':
            if self.serpiente.get_cabeza() in self.obstaculos:
                return False
        
        # Verificar si come manzana
        if self.serpiente.get_cabeza() == self.manzana.get_posicion():
            self.puntaje += 1
            self.serpiente.crecer()
            
            # Modo velocidad: aumentar FPS
            if self.modo_actual == 'velocidad':
                self.fps_actual = min(FPS + self.puntaje * 2, 30)
            
            # Generar nueva manzana
            posiciones_ocupadas = self.serpiente.get_cuerpo().copy()
            if self.modo_actual == 'veneno' and self.manzana_veneno:
                posiciones_ocupadas.append(self.manzana_veneno.get_posicion())
            if self.modo_actual == 'laberinto':
                posiciones_ocupadas.extend(self.obstaculos)
            
            self.manzana.generar_nueva_posicion(posiciones_ocupadas)
        
        # Modo veneno: verificar colisión con manzana venenosa
        if self.modo_actual == 'veneno' and self.manzana_veneno:
            if self.serpiente.get_cabeza() == self.manzana_veneno.get_posicion():
                return False  # Game over al comer manzana roja
        
        return True
    
    def renderizar(self):
        """Renderiza todos los elementos del juego según el modo"""
        self.renderizador.limpiar_pantalla()
        self.renderizador.dibujar_cuadricula()
        
        # Dibujar manzanas
        self.renderizador.dibujar_manzana(self.manzana)
        if self.modo_actual == 'veneno' and self.manzana_veneno:
            self.renderizador.dibujar_manzana_veneno(self.manzana_veneno)
        
        # Dibujar obstáculos
        if self.modo_actual == 'laberinto':
            self.renderizador.dibujar_obstaculos(self.obstaculos)
        
        # Dibujar serpiente
        self.renderizador.dibujar_serpiente(self.serpiente)
        
        # Dibujar HUD
        nombre_modo = MODOS_JUEGO[self.modo_actual]['nombre']
        mejor_puntaje = self.mejores_puntajes.get(self.modo_actual, 0)
        
        if self.modo_actual == 'tiempo':
            self.renderizador.dibujar_hud_tiempo(
                self.puntaje, mejor_puntaje, self.tiempo_restante, nombre_modo
            )
        else:
            self.renderizador.dibujar_hud_modo(
                self.puntaje, mejor_puntaje, nombre_modo
            )
        
        self.renderizador.actualizar()
    
    def pedir_nombre(self):
        """Pide al jugador que ingrese su nombre (3 letras estilo arcade)"""
        nombre = ""
        ingresando = True
        
        while ingresando:
            self.renderizador.dibujar_pantalla_ingreso_nombre(nombre)
            self.renderizador.actualizar()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and len(nombre) == 3:
                        return nombre.upper()
                    
                    elif evento.key == pygame.K_BACKSPACE and len(nombre) > 0:
                        nombre = nombre[:-1]
                    
                    elif len(nombre) < 3:
                        if evento.unicode.isalpha():
                            nombre += evento.unicode.upper()
        
        return None
    
    def game_over(self):
        """Maneja la pantalla de game over y guarda puntuación si corresponde"""
        nombre_modo = MODOS_JUEGO[self.modo_actual]['nombre']
        mejor_puntaje = self.mejores_puntajes.get(self.modo_actual, 0)
        
        # Actualizar mejor puntaje local
        if self.puntaje > mejor_puntaje:
            self.mejores_puntajes[self.modo_actual] = self.puntaje
        
        # Si hay puntuación, pedir nombre y guardar
        if self.puntaje > 0:
            nombre = self.pedir_nombre()
            
            if nombre:
                self.renderizador.dibujar_pantalla_guardando()
                self.renderizador.actualizar()
                pygame.time.delay(500)
                
                # Guardar con el nombre del modo como sufijo para diferenciarlo
                username_con_modo = f"{nombre}-{nombre_modo}"
                self.db.guardar_puntuacion(username_con_modo, "Snake", self.puntaje)
        
        # Mostrar pantalla de game over
        self.renderizador.dibujar_pantalla_game_over_modo(
            self.puntaje, 
            self.mejores_puntajes.get(self.modo_actual, 0),
            nombre_modo
        )
        self.renderizador.actualizar()
        
        # Esperar decisión del jugador
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False, False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        return True, True  # Reiniciar mismo modo
                    elif evento.key == pygame.K_ESCAPE:
                        return True, False  # Volver al menú
        
        return False, False
    
    def ejecutar(self):
        """Loop principal del juego"""
        while self.jugando:
            # Mostrar menú de modos
            modo = self.menu_modos()
            
            if modo is None:
                break
            
            # Jugar en el modo seleccionado
            self.nueva_partida(modo)
            
            partida_activa = True
            while partida_activa:
                if not self.manejar_eventos():
                    self.jugando = False
                    break
                
                if not self.actualizar_logica():
                    partida_activa = False
                
                self.renderizar()
                self.clock.tick(self.fps_actual if self.modo_actual == 'velocidad' else FPS)
            
            if self.jugando:
                continuar, mismo_modo = self.game_over()
                self.jugando = continuar
                
                if mismo_modo and continuar:
                    # Reiniciar el mismo modo sin volver al menú
                    pass
                elif not mismo_modo:
                    # Volver al menú de modos
                    continue
        
        self.db.cerrar()
        pygame.quit()


if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()