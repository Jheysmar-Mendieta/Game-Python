"""Sistema de niveles del juego"""
import json
from settings import *
from brick import Brick


class LevelManager:
    """Gestiona la carga y creación de niveles"""
    
    # Definición de niveles predefinidos
    # 0 = vacío, 1 = normal, 2 = resistente, 3 = fuerte, 9 = indestructible
    LEVELS = [
        # Nivel 1: Introducción
        {
            'name': 'Inicio',
            'difficulty': 'Fácil',
            'layout': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        },
        # Nivel 2: Pirámide
        {
            'name': 'Pirámide',
            'difficulty': 'Fácil',
            'layout': [
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 2, 2, 1, 1, 0, 0],
                [0, 1, 1, 2, 2, 2, 2, 1, 1, 0],
                [1, 1, 2, 2, 3, 3, 2, 2, 1, 1],
            ]
        },
        # Nivel 3: Fortaleza
        {
            'name': 'Fortaleza',
            'difficulty': 'Media',
            'layout': [
                [9, 0, 1, 1, 1, 1, 1, 1, 0, 9],
                [9, 0, 2, 2, 2, 2, 2, 2, 0, 9],
                [9, 0, 1, 1, 3, 3, 1, 1, 0, 9],
                [9, 0, 2, 2, 2, 2, 2, 2, 0, 9],
                [9, 0, 1, 1, 1, 1, 1, 1, 0, 9],
            ]
        },
        # Nivel 4: Laberinto
        {
            'name': 'Laberinto',
            'difficulty': 'Media',
            'layout': [
                [2, 2, 0, 2, 2, 2, 2, 0, 2, 2],
                [2, 0, 0, 0, 2, 2, 0, 0, 0, 2],
                [0, 0, 3, 0, 0, 0, 0, 3, 0, 0],
                [2, 0, 0, 0, 2, 2, 0, 0, 0, 2],
                [2, 2, 0, 2, 2, 2, 2, 0, 2, 2],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
        },
        # Nivel 5: Desafío
        {
            'name': 'Desafío',
            'difficulty': 'Difícil',
            'layout': [
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                [9, 3, 3, 3, 3, 3, 3, 3, 3, 9],
                [9, 3, 2, 2, 2, 2, 2, 2, 3, 9],
                [9, 3, 2, 1, 1, 1, 1, 2, 3, 9],
                [9, 3, 2, 1, 0, 0, 1, 2, 3, 9],
                [9, 3, 2, 1, 1, 1, 1, 2, 3, 9],
                [9, 3, 2, 2, 2, 2, 2, 2, 3, 9],
                [9, 3, 3, 3, 3, 3, 3, 3, 3, 9],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            ]
        },
    ]
    
    def __init__(self):
        self.current_level = 0
    
    def load_level(self, level_index):
        """Carga un nivel y retorna lista de ladrillos"""
        if level_index < 0 or level_index >= len(self.LEVELS):
            return None
        
        self.current_level = level_index
        level_data = self.LEVELS[level_index]
        layout = level_data['layout']
        
        bricks = []
        
        for row_idx, row in enumerate(layout):
            for col_idx, brick_type in enumerate(row):
                if brick_type == 0:
                    continue
                
                # Calcular posición
                x = BRICK_OFFSET_LEFT + col_idx * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP + row_idx * (BRICK_HEIGHT + BRICK_PADDING)
                
                # Obtener color según nivel y tipo
                color = self.get_brick_color(level_index, brick_type)
                
                brick = Brick(x, y, brick_type, color)
                bricks.append(brick)
        
        return bricks
    
    def get_brick_color(self, level_index, brick_type):
        """Obtiene el color de un ladrillo según el nivel y tipo"""
        # Color base según nivel
        base_color = BRICK_COLORS.get(level_index + 1, (200, 100, 100))
        
        # Ajustar según tipo
        if brick_type == BRICK_INDESTRUCTIBLE:
            return (80, 80, 80)
        elif brick_type == BRICK_STRONG:
            return tuple(min(c + 40, 255) for c in base_color)
        elif brick_type == BRICK_RESISTANT:
            return base_color
        else:  # BRICK_NORMAL
            return tuple(max(c - 40, 0) for c in base_color)
    
    def get_level_count(self):
        """Retorna el número total de niveles"""
        return len(self.LEVELS)
    
    def get_level_info(self, level_index):
        """Obtiene información de un nivel"""
        if level_index < 0 or level_index >= len(self.LEVELS):
            return None
        return self.LEVELS[level_index]
    
    def get_current_level_info(self):
        """Obtiene información del nivel actual"""
        return self.get_level_info(self.current_level)