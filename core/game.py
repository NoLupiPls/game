import pygame
from core.settings import BACKGROUND_COLOR, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, WIDTH, HEIGHT


class Game:
    def __init__(self, screen):
        """
        Инициализация класса Game.
        """
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        # Игрок
        self.player = {
            "x": WIDTH // 2,
            "y": HEIGHT // 2,
            "width": PLAYER_SIZE,
            "height": PLAYER_SIZE,
            "color": PLAYER_COLOR,
            "speed": PLAYER_SPEED,
            "velocity_x": 0,
            "velocity_y": 0,
            "on_ground": False
        }

    def handle_event(self, event):
        """
        Обработка событий.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player["velocity_x"] = -self.player["speed"]
            if event.key == pygame.K_RIGHT:
                self.player["velocity_x"] = self.player["speed"]
            if event.key == pygame.K_SPACE and self.player["on_ground"]:
                self.player["velocity_y"] = -15  # Прыжок

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.player["velocity_x"] = 0

    def apply_gravity(self):
        """
        Применяем гравитацию к игроку.
        """
        if not self.player["on_ground"]:
            self.player["velocity_y"] += 1  # Сила гравитации
            if self.player["velocity_y"] > 10:  # Ограничение скорости падения
                self.player["velocity_y"] = 10

    def check_collisions(self):
        """
        Проверка столкновений игрока с землей (упрощенная версия).
        """
        if self.player["y"] + self.player["height"] >= HEIGHT:  # Нижняя граница экрана
            self.player["y"] = HEIGHT - self.player["height"]
            self.player["velocity_y"] = 0
            self.player["on_ground"] = True
        else:
            self.player["on_ground"] = False

    def update_player(self):
        """
        Обновляем положение игрока.
        """
        self.player["x"] += self.player["velocity_x"]
        self.player["y"] += self.player["velocity_y"]

        # Ограничиваем движение игрока в пределах экрана
        if self.player["x"] < 0:
            self.player["x"] = 0
        if self.player["x"] + self.player["width"] > WIDTH:
            self.player["x"] = WIDTH - self.player["width"]

    def update(self):
        """
        Основное обновление состояния игры.
        """
        self.apply_gravity()
        self.update_player()
        self.check_collisions()

    def render(self):
        """
        Отрисовка объектов игры.
        """
        # Заливаем экран фоновым цветом
        self.screen.fill(BACKGROUND_COLOR)

        # Рисуем игрока
        pygame.draw.rect(
            self.screen,
            self.player["color"],
            (self.player["x"], self.player["y"], self.player["width"], self.player["height"]),
        )
