import pygame
import os
from core.settings import WIDTH, HEIGHT, FPS, WHITE, GOLDEN
from core.game import Game
from init import GamePage
from ui.menu import Menu
from entities.collectibles import Collectible
from levels.level_parser import LevelParser


def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно
    pygame.display.set_caption("Game")  # Устанавливаем заголовок окна
    count = 0
    levels = [os.path.join('tests', 'level.txt'), os.path.join('tests', 'level_two.txt')]
    levelparse = LevelParser.parse_level(levels[0])
    all_sprites = levelparse['all_sprites']
    collectibles = [(WIDTH // 3, HEIGHT // 2), (WIDTH // 4, HEIGHT // 2)]
    # Главный цикл игры
    def start_game():
        """Функция, которая будет вызываться при старте игры."""
        game_page = GamePage(screen)
        game_page.run()

    game = Game(screen)

    def draw_bg():
        global image_bg
        image_bg = pygame.image.load('assets/images/backgrounds/forest/background.png')
        image_bg = pygame.transform.scale(image_bg, (WIDTH, HEIGHT))
        screen.blit(image_bg, (0, 0))

    def game_lost():
        font = pygame.font.Font("assets/fonts/comic_sans_pixel.ttf", 40)
        text_surface = font.render('Game Lost', True, WHITE)
        bg = pygame.transform.scale(
            pygame.image.load('assets/images/backgrounds/death/death_background.png').convert_alpha(),
            (WIDTH, HEIGHT))
        dark = pygame.Surface((WIDTH, HEIGHT), masks=(0, 0, 0))
        dark.set_alpha(127)
        screen.blit(dark, (0, 0))
        screen.blit(bg, (0, 0))
        screen.blit(text_surface, (WIDTH // 2 - 60, HEIGHT // 2 - 30))

    def place_collectibles():
        for i in range(len(collectibles)):
            diamond = Collectible(collectibles[i][0], collectibles[i][1], 48)
            all_sprites.add(diamond)


    def game_won():
        font = pygame.font.Font("assets/fonts/comic_sans_pixel.ttf", 80)
        text_surface = font.render('Game Won', True, GOLDEN)
        screen.blit(image_bg, (0, 0))
        screen.blit(text_surface, (WIDTH // 2 - 160, HEIGHT // 2 - 30))
        coll_text_surface = font.render(f'Points collected: {game.player.collected * 1000}', True, GOLDEN)
        dash_text_surface = font.render(f'Dashes used: {game.player.dashes}', True, GOLDEN)
        screen.blit(coll_text_surface, (WIDTH // 3, HEIGHT // 1.5 - 60))
        screen.blit(dash_text_surface, (WIDTH // 3, HEIGHT // 1.3 - 60))


    # Создаем объект игры
    menu = Menu(screen, start_game)
    clock = pygame.time.Clock()
    while menu.running_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                menu.quit_game()
                menu.running_menu = False
        # Обработка ввода
        menu.handle_input(events)
        # Рисуем меню
        menu.draw()
        clock.tick(60)
    game_going = True
    place_collectibles()
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_going:
            game.player.fps = FPS
            game.player.screen = screen
            game.player.update(all_sprites)
            game.handle_event(event, [all_sprites], FPS)  # Передаем событие в игру
            # Обновляем состояние игры
            # Обновляем экран
            draw_bg()
            all_sprites.draw(screen)
            game.player.render(screen, FPS)
            game.draw_ui()
            pygame.display.flip()
            # Ограничение FPS
            clock.tick(FPS)
        if game.player.hp < 1:
            game_going = False
            pygame.display.flip()
            game_lost()
        if game.player.status == 'transfer':
            count += 1
            if count == 1:
                game.player.status = 'gaming'
                game.player.set_coords(WIDTH // 2, HEIGHT // 2)
                levelparse = LevelParser.parse_level(levels[1])
                all_sprites = levelparse['all_sprites']
                collideables = [all_sprites]
            else:
                game_going = False
                pygame.display.flip()
                game_won()
    # Завершение Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
