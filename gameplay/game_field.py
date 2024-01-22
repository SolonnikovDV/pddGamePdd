import pygame
import os
import json

from config.ini import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    SCREEN, GAME_RESULTS
)

from scripts.game_scripts import game_script_1, images_path_1



class GameField:
    def __init__(self, player_name, difficulty, current_score):
        self.font = pygame.font.Font(None, 36)
        self.player_name = player_name
        self.difficulty = difficulty
        self.score = 0
        self.questions = self.load_questions(difficulty)  # Загрузка вопросов с учетом сложности
        self.current_question_index = 0
        self.correct_answers = game_script_1
        self.is_answered = False
        self.attempts = 0
        self.score = current_score  # Используем текущий счет
        self.images_paths = images_path_1

    def display_screen(self):
        SCREEN.fill(WHITE)
        self.draw_text(f"Игрок: {self.player_name}", 10, 10)
        self.draw_text(f"Сложность: {self.difficulty}", 10, 50)
        self.draw_text(f"Очки: {self.score}", SCREEN_WIDTH - 150, 10)

        question, answers = self.questions[self.current_question_index]
        self.draw_text(question, 100, 150)

        # Загрузка и увеличение изображения в 5 раз
        image_path = self.images_paths.get(question)
        if image_path:
            question_image = self.load_image(image_path)
            original_size = question_image.get_size()
            scaled_size = (original_size[0] * 1, original_size[1] * 1)
            question_image = pygame.transform.scale(question_image, scaled_size)
            SCREEN.blit(question_image, (300, 150))  # Адаптируйте положение в соответствии с новым размером

        for i, answer in enumerate(answers):
            self.draw_text(answer, 100, 200 + i * 50)

        pygame.display.update()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        SCREEN.blit(text_surface, (x, y))

    def load_questions(self, difficulty):
        # Извлекаем подмножество вопросов в зависимости от сложности
        num_questions = {'Легкий': 6, 'Средний': 9, 'Тяжелый': 12}.get(difficulty, 6)
        return [("Вопрос " + str(i+1), ["Ответ 1", "Ответ 2", "Ответ 3"]) for i in range(num_questions)]

    def load_image(self, path):
        return pygame.image.load(path)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.is_answered:
            x, y = pygame.mouse.get_pos()
            question, answers = self.questions[self.current_question_index]
            for i, answer in enumerate(answers):
                answer_rect = pygame.Rect(100, 200 + i * 50, 200, 30)
                if answer_rect.collidepoint(x, y):
                    self.attempts += 1
                    if i == self.correct_answers[question] - 1:
                        self.show_popup("Верно")
                        if self.attempts == 1:  # Если ответ верный с первой попытки
                            self.score += self.get_score_increment()
                        self.is_answered = True
                        return 'correct'
                    else:
                        self.show_popup("Неверно")
                        self.show_popup("Давай еще раз")
                        return 'incorrect'

            if self.is_answered:
                if self.current_question_index < len(self.questions) - 1:
                    self.current_question_index += 1
                else:
                    self.end_game()  # Завершаем игру
                    return 'end_game'

            return None

    def get_score_increment(self):
        # Здесь логика для определения количества очков за правильный ответ в зависимости от сложности
        if self.difficulty == 'Легкий':
            return 1
        elif self.difficulty == 'Средний':
            return 2
        elif self.difficulty == 'Тяжелый':
            return 3
        else:
            return 0

    def get_current_score(self):
        return self.score

    def show_popup(self, message):
        # Всплывающее окно с сообщением
        popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)
        pygame.draw.rect(SCREEN, (200, 200, 200), popup_rect)
        self.draw_text(message, popup_rect.x + 20, popup_rect.y + 20)
        pygame.display.update()
        pygame.time.wait(1000)  # Задержка, чтобы пользователь увидел сообщение

    def process_answer(self, answer_index):
        # Здесь должна быть логика для проверки правильности ответа
        # Например, увеличение счета и переход к следующему вопросу
        self.score += 1  # Пример добавления очков
        self.current_question_index += 1  # Переход к следующему вопросу

        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            self.end_game()  # Вызов end_game, если это был последний вопрос

    def display_congratulations_window(self):
        popup_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(SCREEN, (200, 200, 200), popup_rect)
        self.draw_text("Поздравляем с завершением игры!", popup_rect.x + 20, popup_rect.y + 20)
        self.draw_text(f"Ваш счет: {self.score}", popup_rect.x + 20, popup_rect.y + 60)

        # Кнопка "ОК"
        ok_button_rect = pygame.Rect(popup_rect.x + 70, popup_rect.y + popup_rect.height - 50, 60, 30)
        pygame.draw.rect(SCREEN, (100, 100, 100), ok_button_rect)
        self.draw_text("ОК", ok_button_rect.x + 15, ok_button_rect.y + 5)

        pygame.display.update()

        return ok_button_rect

    def end_game(self):
        print(f"Игра окончена, ваш счет: {self.score}")
        save_game_results(self.player_name, self.score)  # Сохраняем результаты
        self.display_congratulations_window()  # Показываем окно поздравления
        return 'end_game'


def save_game_results(player_name, score):
    results_file = GAME_RESULTS
    results = []

    # Загрузка существующих результатов
    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)

    # Добавление нового результата
    results.append({"player_name": player_name, "score": score})

    # Сохранение обновленных результатов
    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)