import pygame
import os
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game
from init import GamePage
from ui.menu import Menu
from levels.level_parser import LevelParser
from ui.menu import Menu





def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Game")  # Устанавливаем заголовок окна
    clock = pygame.time.Clock()  # Таймер для контроля FPS

    levelparse = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
    all_sprites = levelparse['all_sprites']

    blocks = levelparse['blocks']
    platforms = levelparse['platform']
    traps = levelparse['traps']
    # Создаем объект игры

    collideables = [blocks]
    # Главный цикл игры
    def start_game():
        """Функция, которая будет вызываться при старте игры."""
        game_page = GamePage(screen)
        game_page.run()

    game = Game(screen)

    # Создаем объект игры
    #menu = Menu(screen, start_game)
    #menu_result = menu.run()
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.handle_event(event, collideables, FPS)  # Передаем событие в игру
        game.player.render(screen, FPS)
        game.aaaaaaaa(collideables)
        # Обновляем состояние игры
        # Обновляем экран
        all_sprites.draw(screen)
        game.player.render(screen, FPS)
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    # Завершение Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
