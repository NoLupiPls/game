import pygame
import os
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game
from levels.level_parser import LevelParser

class GamePage:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.levelparse = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
        self.all_sprites = self.levelparse['all_sprites']
        self.blocks = self.levelparse['blocks']
        self.platforms = self.levelparse['platform']
        self.traps = self.levelparse['traps']
        self.game = Game(screen)
        self.collideables = [self.blocks, self.platforms, self.traps]
        self.running = True

    def handle_events(self, events):
        """Обработка событий в игре."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            self.game.handle_event(event, self.collideables)  # Передаем событие в игру

    def update(self):
        """Обновление состояния игры."""
        self.all_sprites.update()

    def draw(self):
        """Отображение на экране."""
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Главный игровой цикл."""
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.draw()
            self.clock.tick(FPS)
