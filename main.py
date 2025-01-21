import pygame
import os
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game
from levels.level_parser import LevelParser
from ui.menu import Menu


def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Game")  # Устанавливаем заголовок окна
    clock = pygame.time.Clock()  # Таймер для контроля FPS

    # Парсим уровень
    level_data = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
    all_sprites = level_data['all_sprites']
    blocks = level_data['blocks']
    platforms = level_data['platform']
    traps = level_data['traps']

    # Объединение всех объектов, с которыми можно взаимодействовать
    collideables = [blocks, platforms, traps]

    # Создаем объект игры
    menu = Menu(screen)
    menu_result = menu.run()

    # Главный цикл игры
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event, collideables)

        # Обновление состояния игры
        game.update(collideables)

        # Рендеринг
        screen.fill((0, 0, 0))  # Очистка экрана
        all_sprites.draw(screen)  # Отрисовка всех спрайтов
        game.draw()  # Дополнительный рендеринг игрового интерфейса

        # Обновление дисплея
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    # Завершение Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
