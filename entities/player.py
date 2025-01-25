import pygame
from core.settings import PLAYER_SIZE_X, PLAYER_SIZE_Y, PLAYER_COLOR, PLAYER_SPEED, GRAVITY, MAX_FALL_SPEED, JUMP_POWER, WIDTH, HEIGHT, RED
from entities.hazards import Spike, Lava
from itertools import cycle


class Player:
    def __init__(self, x, y, difficulty='easy'):
        """
        Инициализация игрока.
        """
        self.difficulty = difficulty
        running_animation = [pygame.image.load("assets/images/player/run/{}.png".format(name)).convert()
                                  for name in ('0', '1', '2', '3', '4', '5', '6', '7', '8',
                                               '9', '10', '11', '12', '13', '14', '15')]

        self.running_animation = cycle(running_animation)
        self.run_frame_duration = 1 / 8

        idle_animation = [pygame.image.load("assets/images/player/idle/{}.png".format(name)).convert()
                                  for name in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')]

        self.idle_animation = cycle(idle_animation)
        self.idle_frame_duration = 1 / 5

        dash_animation = [pygame.image.load("assets/images/player/dash/{}.png".format(name)).convert()
                                  for name in ('0', '1', '2', '3', '4', '5', '6')]
        self.dash_animation = cycle(dash_animation)
        self.dash_frame_duration = 1 / 8
        self.rect = pygame.Rect(x, y, PLAYER_SIZE_X, PLAYER_SIZE_Y)  # Прямоугольник игрока
        self.color = PLAYER_COLOR  # Цвет игрока
        self.speed = PLAYER_SPEED  # Скорость игрока
        self.velocity_x = 0        # Горизонтальная скорость
        self.velocity_y = 0        # Вертикальная скорость
        self.image = pygame.image.load("assets/images/player/idle/0.png")
        self.image_run = pygame.image.load("assets/images/player/run/0.png")
        self.on_ground = True     # Флаг, находится ли игрок на земле
        self.damage_inflictable = True # Флаг, может ли игрок получать урон
        self.hp = 0                # Здоровье игрока
        self.can_dash = True
        self.is_dashing = False
        self.facing = 'l'
        self.timer = 0
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
            self.facing = 'l'
        elif keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing = 'r'
        else:
            self.velocity_x = 0
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_d] or keys[pygame.K_a]):
            if pygame.time.get_ticks() > self.last_dash_tick + 3000:
                self.can_dash = True
                if self.can_dash:
                    self.last_dash_tick = pygame.time.get_ticks() + 1500
                    self.can_dash = False
                    self.is_dashing = True
                    if self.facing == 'l':
                        self.velocity_x = -30
                        self.velocity_y = -30
                        self.on_ground = False
                    if self.facing == 'r':
                        self.velocity_x = 30
                        self.velocity_y = -30
                        self.on_ground = False
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y -= JUMP_POWER  # Прыжок

    def apply_gravity(self):
        """
        Применение гравитации.
        """
        if self.on_ground is False:
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
                if self.velocity_x > 0:
                    if self.rect.y - PLAYER_SIZE_Y >= tile.rect.y: # Движение вправо
                        self.rect.right = tile.rect.left
                elif self.velocity_x < 0:  # Движение влево
                    if (self.rect.y - PLAYER_SIZE_Y >= tile.rect.y
                            and ((tile.rect.x, tile.rect.y) != (self.rect.x, self.rect.y))):
                        self.rect.left = tile.rect.right
                    tile.update_texture('assets/images/debug_block/debug_block.png')
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

    def check_vertical_collisions(self, tiles):
        """
        Проверка вертикальных столкновений с тайлами.
        """
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_y >= 0:  # Падение
                    self.rect.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_dashing = False
                elif self.velocity_y < 0:  # Прыжок
                    self.rect.top = tile.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = False

        # Если не касается плиток, сбрасываем флаг on_ground
        if not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False

    def render(self, screen, fps):
        """
        Отрисовка игрока.
        """
        dt = 1 / fps
        self.timer += dt
        if self.velocity_x:
            if self.is_dashing:
                while self.timer >= self.dash_frame_duration:
                    self.timer -= self.dash_frame_duration
                    self.image = next(self.dash_animation)
                    if self.facing == 'l':
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.image = pygame.transform.scale(self.image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
                    screen.blit(self.image, self.rect)
                else:
                    screen.blit(self.image, self.rect)
            else:
                while self.timer >= self.run_frame_duration:
                    self.timer -= self.run_frame_duration
                    self.image_run = next(self.running_animation)
                    if self.facing == 'l':
                        self.image_run = pygame.transform.flip(self.image_run, True, False)
                    self.image_run = pygame.transform.scale(self.image_run, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
                    screen.blit(self.image_run, self.rect)
                else:
                    screen.blit(self.image_run, self.rect)
        else:
            while self.timer >= self.idle_frame_duration:
                self.timer -= self.idle_frame_duration
                self.image = next(self.idle_animation)
                self.image = pygame.transform.scale(self.image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
                screen.blit(self.image, self.rect)
            else:
                screen.blit(self.image, self.rect)