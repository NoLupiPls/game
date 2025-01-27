import pygame
from core.settings import BACKGROUND_COLOR, PLAYER_COLOR, PLAYER_SPEED, WIDTH, HEIGHT
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

        self.sound_settings = {
            "Громкость музыки": 50,
            "Громкость звуков": 50
        }
        self.graphics_settings = {
            "Режим экрана": "Оконный",
            "Разрешение": "1920x1080",
            "Кол-во кадров": "60"
        }

        # Игрок
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        self.sound_settings = {
            "Громкость музыки": 50,
            "Громкость звуков": 50
        }
        self.graphics_settings = {
            "Режим экрана": "Оконный",
            "Разрешение": "1920x1080",
            "Кол-во кадров": "60"
        }

    def draw_ui(self):
        heart = pygame.image.load('assets/images/ui/heart/sprite_heart0.png')
        depleted_heart = pygame.image.load('assets/images/ui/heart/sprite_heart1.png')
        heart = pygame.transform.scale(heart, (WIDTH // 28, HEIGHT // 14))
        depleted_heart = pygame.transform.scale(depleted_heart, (WIDTH // 28, HEIGHT // 14))
        if self.player.difficulty == 'easy':
            if self.player.hp == 3:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))
                self.screen.blit(heart, (WIDTH // 4, HEIGHT // 1.3))
                self.screen.blit(heart, (WIDTH // 5, HEIGHT // 1.3))
            if self.player.hp == 2:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))
                self.screen.blit(heart, (WIDTH // 4, HEIGHT // 1.3))
                self.screen.blit(depleted_heart, (WIDTH // 5, HEIGHT // 1.3))
            if self.player.hp == 1:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))
                self.screen.blit(depleted_heart,(WIDTH // 4, HEIGHT // 1.3))
                self.screen.blit(depleted_heart, (WIDTH // 5, HEIGHT // 1.3))
        elif self.player.difficulty == 'medium':
            if self.player.hp == 2:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))
                self.screen.blit(heart, (WIDTH // 4, HEIGHT // 1.3))
            if self.player.hp == 1:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))
                self.screen.blit(depleted_heart, (WIDTH // 4, HEIGHT // 1.3))
        elif self.player.difficulty == 'hard':
            if self.player.hp == 1:
                self.screen.blit(heart, (WIDTH // 3.33, HEIGHT // 1.3))

    def handle_event(self, event, cldb, fps):
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
            self.player.update(i)
        self.player.render(self.screen, fps)

    def apply_settings(self, sound_settings, graphics_settings):
        """Применение настроек к текущей игре."""
        # Сохраняем новые настройки
        self.sound_settings = sound_settings
        self.graphics_settings = graphics_settings

        # Применяем звуковые и графические настройки
        self.apply_sound_settings()
        self.apply_graphics_settings()

    def apply_sound_settings(self):
        """Применение звуковых настроек."""
        pygame.mixer.music.set_volume(self.sound_settings["Громкость музыки"] / 100)
        # Если в игре есть звуковые эффекты, можно их также настроить
        # Для этого используется pygame.mixer.Sound и выставляется громкость на аналогичное значение.

    def apply_graphics_settings(self):
        """Применение графических настроек (например, изменение разрешения или режима окна)."""
        if self.graphics_settings["Режим экрана"] == "Полноэкранный":
            pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()))

        # Применить разрешение
        resolution = self.graphics_settings["Разрешение"].split("x")
        width, height = int(resolution[0]), int(resolution[1])
        pygame.display.set_mode((width, height))

        # Применить частоту кадров

        pygame.time.Clock().tick(int(self.graphics_settings["Кол-во кадров"]))
