import pygame
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game


def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Game")  # Устанавливаем заголовок окна
    clock = pygame.time.Clock()  # Таймер для контроля FPS

    # Создаем объект игры
    game = Game(screen)

    # Главный цикл игры
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)  # Передаем событие в игру

        # Обновляем состояние игры
        game.update()

        # Рисуем объекты
        game.render()

        # Обновляем экран
        pygame.display.flip()

        # Ограничиваем FPS
        clock.tick(FPS)

    # Завершаем Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
