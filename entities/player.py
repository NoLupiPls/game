import pygame
from core.settings import PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, GRAVITY, MAX_FALL_SPEED, JUMP_POWER, WIDTH, HEIGHT, RED
from entities.hazards import Spike, Lava


class Player:
    def __init__(self, x, y, difficulty='easy'):
        """
        Инициализация игрока.
        """
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)  # Прямоугольник игрока
        self.color = PLAYER_COLOR  # Цвет игрока
        self.speed = PLAYER_SPEED  # Скорость игрока
        self.velocity_x = 0        # Горизонтальная скорость
        self.velocity_y = 0        # Вертикальная скорость
        self.on_ground = False     # Флаг, находится ли игрок на земле
        self.damage_inflictable = True # Флаг, может ли игрок получать урон
        self.hp = 0                # Здоровье игрока
        self.can_dash = True
        self.is_dashing = False
        self.last_dash_tick = 0
        self.dashes = 0            # Счёт использованных рывков
        if difficulty == 'hard':
            self.hp = 1
        elif difficulty == 'medium':
            self.hp = 2
        elif difficulty == 'easy':
            self.hp = 3
        else:
            raise ValueError('Передана неверная сложность в выборе')

    def handle_input(self, keys):
        """
        Обработка ввода от клавиатуры.
        """
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_d] or keys[pygame.K_a]):
            if pygame.time.get_ticks() > self.last_dash_tick + 5000:
                print(pygame.time.get_ticks())
                self.can_dash = True
                if self.can_dash:
                    self.dash_tick = pygame.time.get_ticks() + 1500
                    self.can_dash = False
                    self.rect.x += 20
                    self.rect.y -= 20
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
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
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT:
            self.rect.y = HEIGHT // 2
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH // 2
        if self.rect.x < 0:
            self.rect.x = WIDTH // 2

    def check_horizontal_collisions(self, tiles):
        """
        Проверка горизонтальных столкновений с тайлами.
        """
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_x > 0:  # Движение вправо
                    self.rect.right = tile.rect.left
                elif self.velocity_x < 0:  # Движение влево
                    self.rect.left = tile.rect.right

    def traps_collisions(self, traps):
        """
        Проверка столкновений с шипами и лавой.
        """
        for trap in traps:
            if self.rect.colliderect(trap):
                if type(trap) is Spike:
                    self.hp -= 1
                    if self.damage_inflictable:
                        current_tick_invul = pygame.time.get_ticks()
                        self.damage_inflictable = False
                    else:
                        current_tick = pygame.time.get_ticks()
                        if current_tick >= current_tick_invul + 3000:
                            self.damage_inflictable = True
                elif type(trap) is Lava:
                    self.hp -= 1
                    self.speed -= 2
                    if self.damage_inflictable:
                        current_tick_invul = pygame.time.get_ticks()
                        self.damage_inflictable = False
                    else:
                        current_tick = pygame.time.get_ticks()
                        if current_tick >= current_tick_invul + 3000:
                            self.damage_inflictable = True
                            self.speed += 2

    def check_vertical_collisions(self, tiles):
        """
        Проверка вертикальных столкновений с тайлами.
        """
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_y > 0:  # Падение
                    self.rect.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Прыжок
                    self.rect.top = tile.rect.bottom
                    self.velocity_y = 0

        # Если не касается плиток, сбрасываем флаг on_ground
        if not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False

    def render(self, screen):
        """
        Отрисовка игрока.
        """
        pygame.draw.rect(screen, self.color, self.rect)
