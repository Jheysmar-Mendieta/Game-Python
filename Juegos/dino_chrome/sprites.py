"""Sprites y gráficos del juego Dino"""
import pygame
from settings import *


class SpriteGenerator:
    """Genera todos los sprites del juego usando píxeles"""
    
    @staticmethod
    def create_dino_run1():
        """Crea el primer cuadro del dinosaurio corriendo"""
        surface = pygame.Surface((DINO_WIDTH, DINO_HEIGHT), pygame.SRCALPHA)
        pixels = [
            "          ████████████████          ",
            "          ██████████████████        ",
            "          ████████████████████      ",
            "          ██████████████████████    ",
            "          ████████████████████████  ",
            "          ██████████                ",
            "          ████████████████████████  ",
            "          ████████████████████████  ",
            "          ████████████████████████  ",
            "          ████████████████████      ",
            "          ████████████████          ",
            "          ██████████████            ",
            "          ████████████              ",
            "      ██  ██████████                ",
            "    ████  ████████                  ",
            "  ████████████████                  ",
            "  ██████████████                    ",
            "    ██████████                      ",
            "    ████████                        ",
            "      ████                          ",
            "      ████                          ",
            "      ████                          ",
            "      ████                          ",
            "      ██                            ",
        ]
        
        for y, row in enumerate(pixels):
            for x, char in enumerate(row):
                if char == '█':
                    surface.set_at((x, y * 2), (83, 83, 83))
                    surface.set_at((x, y * 2 + 1), (83, 83, 83))
        
        return surface
    
    @staticmethod
    def create_dino_run2():
        """Crea el segundo cuadro del dinosaurio corriendo"""
        surface = pygame.Surface((DINO_WIDTH, DINO_HEIGHT), pygame.SRCALPHA)
        pixels = [
            "          ████████████████          ",
            "          ██████████████████        ",
            "          ████████████████████      ",
            "          ██████████████████████    ",
            "          ████████████████████████  ",
            "          ██████████                ",
            "          ████████████████████████  ",
            "          ████████████████████████  ",
            "          ████████████████████████  ",
            "          ████████████████████      ",
            "          ████████████████          ",
            "          ██████████████            ",
            "          ████████████              ",
            "      ██  ██████████                ",
            "    ████  ████████                  ",
            "  ████████████████                  ",
            "  ██████████████                    ",
            "    ██████████                      ",
            "    ████████                        ",
            "      ████                          ",
            "        ████                        ",
            "        ████                        ",
            "          ████                      ",
            "          ██                        ",
        ]
        
        for y, row in enumerate(pixels):
            for x, char in enumerate(row):
                if char == '█':
                    surface.set_at((x, y * 2), (83, 83, 83))
                    surface.set_at((x, y * 2 + 1), (83, 83, 83))
        
        return surface
    
    @staticmethod
    def create_dino_dead():
        """Crea el sprite del dinosaurio muerto"""
        surface = pygame.Surface((DINO_WIDTH, DINO_HEIGHT), pygame.SRCALPHA)
        pixels = [
            "          ████████████████          ",
            "          ██████████████████        ",
            "          ████████████████████      ",
            "          ██████████████████████    ",
            "    ██    ████████████████████████  ",
            "  ████    ██████████                ",
            "  ████    ████████████████████████  ",
            "    ██    ████████████████████████  ",
            "          ████████████████████████  ",
            "          ████████████████████      ",
            "          ████████████████          ",
            "          ██████████████            ",
            "          ████████████              ",
            "      ██  ██████████                ",
            "    ████  ████████                  ",
            "  ████████████████                  ",
            "  ██████████████                    ",
            "    ██████████                      ",
            "    ████████                        ",
            "      ████                          ",
            "      ████                          ",
            "      ████                          ",
            "      ████                          ",
            "      ██                            ",
        ]
        
        for y, row in enumerate(pixels):
            for x, char in enumerate(row):
                if char == '█':
                    surface.set_at((x, y * 2), (83, 83, 83))
                    surface.set_at((x, y * 2 + 1), (83, 83, 83))
        
        return surface
    
    @staticmethod
    def create_cactus_small():
        """Crea un cactus pequeño"""
        surface = pygame.Surface((CACTUS_SMALL_WIDTH, CACTUS_SMALL_HEIGHT), pygame.SRCALPHA)
        
        # Patrón del cactus pequeño
        for y in range(CACTUS_SMALL_HEIGHT):
            for x in range(CACTUS_SMALL_WIDTH):
                # Cuerpo principal
                if 6 <= x <= 10:
                    pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
                # Brazos
                if y > 10 and y < 20:
                    if x == 4 or x == 5:
                        pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
                    if x == 11 or x == 12:
                        pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
        
        return surface
    
    @staticmethod
    def create_cactus_large():
        """Crea un cactus grande"""
        surface = pygame.Surface((CACTUS_LARGE_WIDTH, CACTUS_LARGE_HEIGHT), pygame.SRCALPHA)
        
        # Patrón del cactus grande
        for y in range(CACTUS_LARGE_HEIGHT):
            for x in range(CACTUS_LARGE_WIDTH):
                # Cuerpo principal
                if 9 <= x <= 15:
                    pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
                # Brazos
                if 15 < y < 30:
                    if 5 <= x <= 8:
                        pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
                    if 16 <= x <= 19:
                        pygame.draw.rect(surface, (83, 83, 83), (x, y, 1, 1))
        
        return surface
    
    @staticmethod
    def create_cloud():
        """Crea una nube"""
        surface = pygame.Surface((CLOUD_WIDTH, CLOUD_HEIGHT), pygame.SRCALPHA)
        
        # Patrón de nube simple
        pygame.draw.ellipse(surface, (200, 200, 200), (0, 4, 15, 10))
        pygame.draw.ellipse(surface, (200, 200, 200), (10, 0, 18, 14))
        pygame.draw.ellipse(surface, (200, 200, 200), (25, 4, 15, 10))
        pygame.draw.ellipse(surface, (200, 200, 200), (8, 6, 30, 8))
        
        return surface
    
    @staticmethod
    def create_star():
        """Crea una estrella para el modo noche"""
        surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        
        # Estrella simple (cruz)
        pygame.draw.rect(surface, (255, 255, 255), (1, 0, 2, 4))
        pygame.draw.rect(surface, (255, 255, 255), (0, 1, 4, 2))
        
        return surface