import pygame

# размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = int(800 * 1.6), int(600 * 1.5)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GAME_RESULTS: str = 'chart/game_results.json'