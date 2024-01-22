import pygame
import json
import os

from config.ini import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    SCREEN,
    GAME_RESULTS,
)


class ResultsScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.results = self.load_results()

    def load_results(self):
        results_file = GAME_RESULTS
        if os.path.exists(results_file):
            with open(results_file, 'r') as file:
                results = json.load(file)

            # Проверяем наличие ключа "creation_date" в каждом результате
            for result in results:
                result.setdefault('creation_date', '')  # Если ключа нет, устанавливаем пустую строку

            # Сортировка результатов
            sorted_results = sorted(results, key=lambda x: (-x["score"], x["creation_date"]))
            return sorted_results
        return []

    def display_screen(self):
        SCREEN.fill(WHITE)
        self.draw_text("Результаты", SCREEN_WIDTH // 2 - 50, 50)

        y = 100
        for result in self.results:
            result_text = f"{result['player_name']}: {result['score']}"
            highlight = result.get('highlight', False)
            if highlight:
                # Отображаем выделенное имя игрока другим цветом или стилем
                self.draw_text_highlighted(result_text, SCREEN_WIDTH // 2 - 50, y)
            else:
                self.draw_text(result_text, SCREEN_WIDTH // 2 - 50, y)
            y += 30

        self.draw_text("Нажмите любую клавишу для возврата в меню", SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 50)
        pygame.display.update()

    def draw_text_highlighted(self, text, x, y):
        # Метод для отображения выделенного текста
        text_surface = self.font.render(text, True, BLACK)  # Измените цвет или стиль, если требуется
        SCREEN.blit(text_surface, (x, y))

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        SCREEN.blit(text_surface, (x, y))

    # метод перегрузки результатов
    def update_results(self):
        self.results = self.load_results()

    def highlight_player_name(self, player_name):
        for result in self.results:
            if result['player_name'] == player_name:
                result['highlight'] = True
            else:
                result.pop('highlight', None)  # Убираем подсветку для других имен

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            return 'menu'
        return None
