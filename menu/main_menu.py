import pygame

from config.ini import (
    WHITE,
    BLACK,
    SCREEN,
)


# Инициализация Pygame
pygame.init()


class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def display_menu(self):
        SCREEN.fill(WHITE)
        self.draw_text("Начать игру", 100, 100)
        self.draw_text("Чарт", 100, 150)
        self.draw_text("Выйти из игры", 100, 200)
        pygame.display.update()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        SCREEN.blit(text_surface, (x, y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 100 <= y <= 130:  # Диапазон для кнопки "Начать игру"
                return 'name_entry'
            elif 150 <= y <= 180:  # Диапазон для кнопки "Чарт"
                return 'leaderboard'
            elif 200 <= y <= 230:  # Диапазон для кнопки "Выйти из игры"
                return 'exit'
        return None
