"""Lógica principal del juego Memory"""
import pygame
import random
from card import Card
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, LEVELS, CARD_MARGIN, 
                    HUD_HEIGHT, CARD_REVEAL_DELAY, MATCH_FLASH_DURATION, COLORS)
from particles import ParticleSystem


class GameState:
    """Estado del juego"""
    
    def __init__(self, level, sound_manager):
        self.level = level
        self.sound_manager = sound_manager
        self.level_config = LEVELS[level]
        self.rows = self.level_config['rows']
        self.cols = self.level_config['cols']
        
        # Estadísticas
        self.moves = 0
        self.pairs_found = 0
        self.total_pairs = (self.rows * self.cols) // 2
        self.time_elapsed = 0
        self.is_won = False
        self.paused = False
        
        # Estado de juego
        self.cards = []
        self.flipped_cards = []
        self.can_flip = True
        self.reveal_timer = 0
        
        # Partículas
        self.particles = ParticleSystem()
        
        # Inicializar tablero
        self._create_board()
        
    def _create_board(self):
        """Crea el tablero de cartas"""
        # Calcular tamaño de cartas
        available_width = SCREEN_WIDTH - (CARD_MARGIN * (self.cols + 1))
        available_height = SCREEN_HEIGHT - HUD_HEIGHT - (CARD_MARGIN * (self.rows + 1))
        
        card_width = available_width // self.cols
        card_height = available_height // self.rows
        
        # Hacer cartas cuadradas
        card_size = min(card_width, card_height)
        
        # Calcular offset para centrar
        total_width = card_size * self.cols + CARD_MARGIN * (self.cols - 1)
        total_height = card_size * self.rows + CARD_MARGIN * (self.rows - 1)
        offset_x = (SCREEN_WIDTH - total_width) // 2
        offset_y = HUD_HEIGHT + (SCREEN_HEIGHT - HUD_HEIGHT - total_height) // 2
        
        # Crear pares de cartas
        total_cards = self.rows * self.cols
        image_ids = list(range(self.total_pairs)) * 2
        random.shuffle(image_ids)
        
        # Crear cartas
        idx = 0
        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * (card_size + CARD_MARGIN)
                y = offset_y + row * (card_size + CARD_MARGIN)
                card = Card(x, y, card_size, card_size, image_ids[idx])
                self.cards.append(card)
                idx += 1
                
    def handle_click(self, pos):
        """Maneja click en el tablero"""
        if not self.can_flip or self.is_won or self.paused:
            return
            
        for card in self.cards:
            if card.contains_point(pos) and not card.is_flipped and not card.is_matched:
                if len(self.flipped_cards) < 2:
                    # Voltear carta
                    card.start_flip(True)
                    self.flipped_cards.append(card)
                    self.sound_manager.play('flip')
                    
                    # Si se voltearon 2 cartas
                    if len(self.flipped_cards) == 2:
                        self.moves += 1
                        self.can_flip = False
                        self.reveal_timer = CARD_REVEAL_DELAY
                break
                
    def update(self, dt, mouse_pos):
        """Actualiza el estado del juego"""
        if self.paused or self.is_won:
            return
            
        # Actualizar tiempo
        self.time_elapsed += dt / 1000
        
        # Actualizar cartas
        for card in self.cards:
            card.update(dt)
            card.hover = card.contains_point(mouse_pos) and not card.is_flipped and not card.is_matched
            
        # Actualizar partículas
        self.particles.update(dt)
        
        # Timer de revelación
        if self.reveal_timer > 0:
            self.reveal_timer -= dt
            
            if self.reveal_timer <= 0:
                self._check_match()
                
    def _check_match(self):
        """Verifica si las cartas volteadas coinciden"""
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            
            if card1.image_id == card2.image_id:
                # ¡Pareja encontrada!
                card1.set_matched(MATCH_FLASH_DURATION)
                card2.set_matched(MATCH_FLASH_DURATION)
                self.pairs_found += 1
                self.sound_manager.play('match')
                
                # Emitir partículas
                center_x = (card1.rect.centerx + card2.rect.centerx) // 2
                center_y = (card1.rect.centery + card2.rect.centery) // 2
                self.particles.emit(center_x, center_y, 15)
                
                # Verificar victoria
                if self.pairs_found == self.total_pairs:
                    self.is_won = True
                    self.sound_manager.play('victory')
                    # Ráfaga de partículas
                    for _ in range(5):
                        x = random.randint(100, SCREEN_WIDTH - 100)
                        y = random.randint(HUD_HEIGHT + 100, SCREEN_HEIGHT - 100)
                        self.particles.emit_burst(x, y, 30)
            else:
                # No coinciden, voltear de vuelta
                card1.start_flip(False)
                card2.start_flip(False)
                
            self.flipped_cards.clear()
            self.can_flip = True
            
    def draw(self, surface, card_images):
        """Dibuja el estado del juego"""
        # Dibujar cartas
        for card in self.cards:
            card.draw(surface, card_images)
            
        # Dibujar partículas
        self.particles.draw(surface)
        
    def get_score(self):
        """Calcula la puntuación (menor es mejor: movimientos + tiempo)"""
        return int(self.moves + self.time_elapsed)
    
    def format_time(self):
        """Formatea el tiempo como MM:SS"""
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        return f"{minutes:02d}:{seconds:02d}"