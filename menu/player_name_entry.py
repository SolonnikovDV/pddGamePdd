import pygame

from config.ini import (
    WHITE,
    BLACK,
    SCREEN,
)

class PlayerNameEntry:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.name = ""

    def display_screen(self):
        SCREEN.fill(WHITE)
        self.draw_text("Введите имя игрока", 100, 50)
        self.draw_text(self.name, 100, 100)
        pygame.display.update()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        SCREEN.blit(text_surface, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.name
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                self.name += event.unicode
        return None
