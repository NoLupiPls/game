import pygame
from core.settings import BACKGROUND_COLOR, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, WIDTH, HEIGHT
from entities.player import Player
import ui.pause_menu


class Game:
    def __init__(self, screen):
        """
        Инициализация класса Game.
        """
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        # Игрок
        self.player = Player(WIDTH // 2, HEIGHT // 2,)

    def handle_event(self, event, cldb):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            if keys[pygame.K_ESCAPE]:
                ui.pause_menu.main(self.screen)
        """
        Основное обновление состояния игры.
        """
        background = pygame.Surface((WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))
        for i in cldb:
            print(i)
            self.player.update(i)
        self.player.render(self.screen)
