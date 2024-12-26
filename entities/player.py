import pygame
from core.settings import PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, GRAVITY, MAX_FALL_SPEED, JUMP_POWER, WIDTH, HEIGHT


class Player:
    def __init__(self, x, y):
        """
        Инициализация игрока.
        """
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)  # Прямоугольник игрока
        self.color = PLAYER_COLOR  # Цвет игрока
        self.speed = PLAYER_SPEED  # Скорость игрока
        self.velocity_x = 0        # Горизонтальная скорость
        self.velocity_y = 0        # Вертикальная скорость
        self.on_ground = False     # Флаг, находится ли игрок на земле

    def handle_input(self, keys):
        """
        Обработка ввода от клавиатуры.
        """
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = JUMP_POWER  # Прыжок

    def apply_gravity(self):
        """
        Применение гравитации.
        """
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

    def update(self, tiles):
        """
        Обновление положения игрока и проверка столкновений.
        """
        # Обновляем горизонтальное положение
        self.rect.x += self.velocity_x
        self.check_horizontal_collisions(tiles)

        # Обновляем вертикальное положение
        self.rect.y += self.velocity_y
        self.apply_gravity()
        self.check_vertical_collisions(tiles)

        # Ограничиваем игрока в пределах экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH - self.rect.width

    def check_horizontal_collisions(self, tiles):
        """
        Проверка горизонтальных столкновений с тайлами.
        """
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_x > 0:  # Движение вправо
                    self.rect.right = tile.left
                elif self.velocity_x < 0:  # Движение влево
                    self.rect.left = tile.right

    def check_vertical_collisions(self, tiles):
        """
        Проверка вертикальных столкновений с тайлами.
        """
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_y > 0:  # Падение
                    self.rect.bottom = tile.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Прыжок
                    self.rect.top = tile.bottom
                    self.velocity_y = 0

        # Если не касается плиток, сбрасываем флаг on_ground
        if not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False

    def render(self, screen):
        """
        Отрисовка игрока.
        """
        pygame.draw.rect(screen, self.color, self.rect)
