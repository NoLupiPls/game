import pygame, os
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game
from levels.level_parser import LevelParser


def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Celeste-like Game")  # Устанавливаем заголовок окна
    clock = pygame.time.Clock()  # Таймер для контроля FPS

    levelparse = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
    all_sprites = levelparse['all_sprites']
    blocks = levelparse['blocks']
    platforms = levelparse['platform']
    traps = levelparse['traps']
    # Создаем объект игры
    game = Game(screen)
    collideables = [blocks, platforms, traps]
    # Главный цикл игры
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event, collideables)  # Передаем событие в игру
        # Обновляем состояние игры
        # Обновляем экран
        all_sprites.draw(screen)
        pygame.display.flip()
        # Ограничиваем FPS
        clock.tick(FPS)
    # Завершаем Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
