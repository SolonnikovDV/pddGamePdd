import pygame
import sys
import json
import os
from datetime import datetime

from gameplay.game_board import GameBoard
from gameplay.game_field import GameField
from menu.main_menu import MainMenu
from menu.player_name_entry import PlayerNameEntry
from menu.difficulty_selection import DifficultySelection
from chart.results_screen import ResultsScreen
from config.ini import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    SCREEN, GAME_RESULTS,
)

def main():
    pygame.init()
    pygame.display.set_caption("Игра")

    main_menu = MainMenu()
    name_entry = PlayerNameEntry()
    difficulty_selection = DifficultySelection()
    game_board = None
    results_screen = ResultsScreen()
    current_screen = 'menu'
    player_name = None
    difficulty = None
    current_game_field = None
    current_score = 0  # Текущий счет
    game_over = False  # переменная для отслеживания завершения игры

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_screen == 'menu':
                action = main_menu.handle_event(event)
                if action == 'name_entry':
                    current_screen = 'name_entry'
                elif action == 'leaderboard':
                    current_screen = 'results'
                elif action == 'exit':
                    pygame.quit()
                    sys.exit()
                main_menu.display_menu()

            elif current_screen == 'name_entry':
                name = name_entry.handle_event(event)
                if name is not None:
                    player_name = name
                    current_screen = 'difficulty_selection'
                name_entry.display_screen()

            elif current_screen == 'difficulty_selection':
                selected_difficulty = difficulty_selection.handle_event(event)
                if selected_difficulty is not None:
                    difficulty = selected_difficulty
                    current_screen = 'game_board'
                    SCREEN.fill(WHITE)  # Очистка экрана
                    game_board = GameBoard(difficulty, player_name, current_score)
                difficulty_selection.display_screen()

            elif current_screen == 'game_board':
                if game_board is not None:
                    game_board.draw(SCREEN)
                    action = game_board.handle_event(event)
                    if action and action[0] == 'open_game_field':
                        current_screen = 'game_field'
                        current_game_field = GameField(game_board.player_name,
                                                       game_board.difficulty,
                                                       game_board.current_score)
                        current_game_field.current_question_index = action[1]
                    elif action == 'exit':
                        current_screen = 'menu'
                        game_board = None
                    elif action == 'save_results':
                        game_over = True  # Устанавливаем флаг завершения игры

            elif current_screen == 'game_field':
                if current_game_field is not None:
                    answer_result = current_game_field.handle_event(event)
                    if answer_result == 'correct':
                        current_screen = 'game_board'
                        game_board.current_score = current_game_field.get_current_score()
                        game_board.current_node += 1  # Переход к следующей ноде
                        game_board.update_node_colors()  # Обновление цветов нод

                    elif answer_result == 'incorrect':
                        pass

                    elif answer_result == 'end_game':
                        # Переход в чарт после окончания игры
                        current_screen = 'results'
                        results_screen.update_results()  # Обновляем результаты в чарте
                        results_screen.highlight_player_name(player_name)  # Подсвечиваем имя игрока
                    else:
                        current_game_field.display_screen()

            elif current_screen == 'results':
                action = results_screen.handle_event(event)

                if action:
                    current_screen = action
                results_screen.display_screen()

        if game_over:
            # Отображаем экран поздравления
            game_board.game_over_screen(SCREEN)
            pygame.display.update()

            # Обработка событий для экрана поздравления
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_board.save_results_button_rect.collidepoint(event.pos):
                        # Сохранение результатов игрока
                        save_game_results(game_board.player_name, game_board.current_score)
                        current_screen = 'results'
                        results_screen.update_results()
                        results_screen.highlight_player_name(game_board.player_name)
                        game_over = False  # Сбрасываем флаг завершения игры
                elif event.type == pygame.KEYDOWN:
                    # Возвращение в главное меню после завершения игры
                    current_screen = 'menu'
                    game_board = None

        pygame.display.update()


def save_game_results(player_name, score):
    results_file = GAME_RESULTS
    results = []

    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)

    # Добавляем результат с текущей датой и временем
    result_entry = {"player_name": player_name, "score": score, "creation_date": str(datetime.now())}
    results.append(result_entry)

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)


if __name__ == "__main__":
    main()