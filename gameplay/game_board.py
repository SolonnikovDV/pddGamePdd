import pygame
import random

from config.ini import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
)


class GameBoard:
    def __init__(self, difficulty, player_name, score):
        self.difficulty = difficulty
        self.player_name = player_name
        self.current_score = score
        self.node_radius = 20  # Увеличенный размер нод
        self.current_node = 0  # Начинаем с первой ноды

        # Инициализация нод должна происходить перед их использованием
        self.nodes = self.generate_nodes()
        self.node_colors = [(200, 200, 200)] * len(self.nodes)  # Все ноды серые изначально
        self.node_colors[self.current_node] = (0, 255, 0)  # Доступная нода зеленая

        # Инициализируем текст и прямоугольник для кнопки "Выход"
        self.font = pygame.font.Font(None, 36)
        self.exit_text = 'Выход'
        self.exit_text_surface = self.font.render(self.exit_text, True, BLACK)
        text_width, text_height = self.exit_text_surface.get_size()
        self.exit_button_rect = pygame.Rect(
            SCREEN_WIDTH - text_width - 20,  # 20 пикселей отступа от правого края
            SCREEN_HEIGHT - text_height - 20,  # 20 пикселей отступа от нижнего края
            text_width + 10,  # 10 пикселей дополнительного пространства по ширине
            text_height  # Высота текста
        )
        self.current_node = 0  # Индекс текущей ноды в стеке
        self.current_score = score  # Используем self.current_score вместо self.score

        self.is_game_over = False  # атрибут для отслеживания завершения игры

        self.save_results_button_rect = pygame.Rect(
            SCREEN_WIDTH - text_width - 20,
            SCREEN_HEIGHT - text_height - 20,
            text_width + 10,
            text_height
        )


    def generate_nodes(self):
        # Генерация нод в зависимости от сложности
        if self.difficulty == 'Легкий':
            num_nodes = 6
        elif self.difficulty == 'Средний':
            num_nodes = 9
        elif self.difficulty == 'Тяжелый':
            num_nodes = 12
        else:
            num_nodes = 6  # Значение по умолчанию

        spacing = SCREEN_WIDTH // (num_nodes + 1)
        nodes = []
        for i in range(num_nodes):
            x = spacing * (i + 1)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            nodes.append((x, y))
        return nodes

    def draw(self, screen):
        screen.fill(WHITE)

        # Рисуем ноды и линии между ними
        for index, node in enumerate(self.nodes):
            pygame.draw.circle(screen, self.node_colors[index], node, self.node_radius)
            if index < len(self.nodes) - 1:
                pygame.draw.line(screen, BLACK, self.nodes[index], self.nodes[index + 1])

        # Рисуем информацию о игроке и текущий счет
        self.draw_text(f"Игрок: {self.player_name}", 10, 10, screen)
        self.draw_text(f"Сложность: {self.difficulty}", 10, 50, screen)
        self.draw_text(f"Очки: {self.current_score}", SCREEN_WIDTH - 150, 10, screen)

        # Рисуем кнопку "Выход"
        pygame.draw.rect(screen, (200, 200, 200), self.exit_button_rect)
        self.draw_text(self.exit_text, self.exit_button_rect.x + 5, self.exit_button_rect.y + 5, screen)

        # Рисуем кнопку "Сохранить результаты"
        pygame.draw.rect(screen, (200, 200, 200), self.save_results_button_rect)
        self.draw_text("Далее", self.save_results_button_rect.x + 5, self.save_results_button_rect.y + 5,
                       screen)

        pygame.display.update()

    def draw_text(self, text, x, y, screen):
        text_surface = self.font.render(text, True, BLACK)
        screen.blit(text_surface, (x, y))

    def display_player_info(self, screen):
        font = pygame.font.Font(None, 36)
        player_info = f"Игрок: {self.player_name}, Сложность: {self.difficulty}"
        score_info = f"Очки: {self.current_score}"
        screen.blit(font.render(player_info, True, BLACK), (10, 10))
        screen.blit(font.render(score_info, True, BLACK), (SCREEN_WIDTH - 150, 10))

    def draw_exit_button(self, screen):
        # Рисуем текст кнопки "Выход" в правом нижнем углу экрана
        screen.blit(self.exit_text_surface, (self.exit_button_rect.x + 5, self.exit_button_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.is_game_over:
                for i, node in enumerate(self.nodes):
                    if self.node_contains_point(node, event.pos):
                        if i == self.current_node:  # Проверяем, что кликнули на доступную ноду
                            return 'open_game_field', i
                if self.exit_button_rect.collidepoint(event.pos):
                    return 'exit'
            elif self.save_results_button_rect.collidepoint(event.pos):
                if self.save_results_button_rect.collidepoint(event.pos):
                    return 'save_results'
                self.is_game_over = False  # Сбрасываем флаг завершения игры
                return 'save_results'
        return None

    def node_contains_point(self, node, point):
        # Проверка, находится ли точка в пределах ноды
        node_rect = pygame.Rect(node[0] - self.node_radius, node[1] - self.node_radius, self.node_radius * 2,
                                self.node_radius * 2)
        return node_rect.collidepoint(point)

    def update_node_colors(self):
        for i in range(len(self.node_colors)):
            if i < self.current_node:
                self.node_colors[i] = (0, 200, 0)  # Пройденные ноды
            elif i == self.current_node:
                self.node_colors[i] = (0, 255, 0)  # Текущая доступная нода
            else:
                self.node_colors[i] = (200, 200, 200)  # Недоступные ноды

        # Проверяем, завершил ли игрок все ноды
        if self.current_node == len(self.nodes):
            self.is_game_over = True

    def game_over_screen(self, screen):
        # Получение размеров текста для центрирования
        congrat_text = "Поздравляем!"
        score_text = f"Вы набрали {self.current_score} очков"
        save_text = "Нажмите Сохранить, чтобы сохранить результаты"

        congrat_size = self.font.size(congrat_text)
        score_size = self.font.size(score_text)
        save_size = self.font.size(save_text)

        # Отображение экрана поздравления с завершением игры
        self.draw_text(congrat_text, (SCREEN_WIDTH - congrat_size[0]) // 2, 50, screen)
        self.draw_text(score_text, (SCREEN_WIDTH - score_size[0]) // 2, 100, screen)
        self.draw_text(save_text, (SCREEN_WIDTH - save_size[0]) // 2, 150, screen)

        # Получение размеров текста для кнопки "Сохранить результаты"
        save_button_text = "Сохранить результаты"
        save_button_size = self.font.size(save_button_text)

        # Рассчитываем координаты x и y для кнопки, чтобы центрировать ее
        save_button_x = (SCREEN_WIDTH - save_button_size[0] - 10) // 2  # 10 - это дополнительный отступ в кнопке
        save_button_y = self.save_results_button_rect.y

        # Обновляем положение кнопки
        self.save_results_button_rect.x = save_button_x
        self.save_results_button_rect.y = save_button_y

        # Рисуем кнопку "Сохранить результаты"
        pygame.draw.rect(screen, (200, 200, 200), self.save_results_button_rect)
        self.draw_text(save_button_text, save_button_x + 5, save_button_y + 5, screen)

        pygame.display.update()

        pygame.display.update()

    pygame.display.update()
