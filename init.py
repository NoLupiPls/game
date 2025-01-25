import pygame
import os
from core.settings import WIDTH, HEIGHT, FPS
from core.game import Game
from levels.level_parser import LevelParser


class GamePage:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game = Game(screen)
        self.running = True

    def handle_events(self, events):
        """Обработка событий в игре."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False 

    def update(self):
        """Обновление состояния игры."""

    def draw(self):
        """Отображение на экране."""
        pygame.display.flip()

    def run(self):
        """Главный игровой цикл."""
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.draw()
            self.clock.tick(FPS)
