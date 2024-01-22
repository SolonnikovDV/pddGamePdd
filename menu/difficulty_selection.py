import pygame

from config.ini import (
    WHITE,
    BLACK,
    SCREEN,
)


class DifficultySelection:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.difficulties = ["Легкий", "Средний", "Тяжелый"]
        self.selected_difficulty = None

    def display_screen(self):
        SCREEN.fill(WHITE)
        y = 100
        for difficulty in self.difficulties:
            self.draw_text(difficulty, 100, y)
            y += 50
        pygame.display.update()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        SCREEN.blit(text_surface, (x, y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, difficulty in enumerate(self.difficulties):
                if 100 <= y <= 100 + 50 * (i + 1):
                    return difficulty
        return None
