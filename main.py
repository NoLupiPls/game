from entities.player import Player
from entities.hazards import *
from entities.platform import *
from levels.level_parser import LevelParser
from core.settings import WIDTH, HEIGHT, FPS, DIFFICULTY
import os
import time
from ui.menu import main_menu_gui
import core.settings


def main():
    j = main_menu_gui()
    while core.settings.DIFFICULTY is None:
        j = main_menu_gui()
        import core.settings
        time.sleep(16)
    DIFFICULTY = core.settings.DIFFICULTY
    player = Player(0, 0, DIFFICULTY)
    levelparse = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
    all_sprites = levelparse['all_sprites']
    blocks = levelparse['blocks']
    platforms = levelparse['platform']
    traps = levelparse['traps']
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Game")  # Устанавливаем заголовок окна
    clock = pygame.time.Clock()  # Таймер для контроля FPS

    # Создаем объект игры

    # Главный цикл игры
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ...  # call pause menu
        pygame.display.flip()
        clock.tick(FPS)
        all_sprites.update()
        blocks.update()
        platforms.update()
        traps.update()
        player.update(platforms)
        pygame.display.update()
    pygame.quit()

main()