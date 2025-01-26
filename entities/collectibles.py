import pygame
from itertools import cycle


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        """
        Инициализация объекта, который можно собирать.
        """
        super().__init__()
        self.size = size
        self.timer = 0
        self.count = 0
        self.image = pygame.image.load("assets/images/collectibles/diamond/sprite_diamond0.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, size, size)  # Прямоугольник для коллизий
        self.collected = False  # Флаг, собран ли объект
        self.pu_frame_duration = 1 / 7

        pick_up_animation = [pygame.image.load(
            "assets/images/collectibles/diamond/collect/sprite_diamond_collect{}.png".format(name)).convert()
                             for name in ('02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                                          '15', '16', '17', '18', '19', '20', '21', '22', '23', '24')]
        self.pick_up_animation = cycle(pick_up_animation)

        idle_animation = [pygame.image.load("assets/images/collectibles/diamond/sprite_diamond{}.png"
                                            .format(name)).convert() for name in ('0', '1', '2')]
        self.idle_animation = cycle(idle_animation)
        self.idle_frame_duration = 1 / 3

    def render(self, screen, fps):
        """
        Отрисовывает объект, если он не собран.
        """
        dt = 1 / fps
        self.timer += dt


        if not self.collected:
            while self.timer >= self.idle_frame_duration:
                self.timer -= self.idle_frame_duration
                self.image = next(self.idle_animation)
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.image.set_colorkey((0, 0, 0))
                self.image = self.image.convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)
                screen.blit(self.image, self.rect)
            else:
                self.image.set_colorkey((0, 0, 0))
                self.image = self.image.convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)
                screen.blit(self.image, self.rect)
        elif self.collected and self.count <= 23:
            while self.timer >= self.pu_frame_duration:
                self.timer -= self.pu_frame_duration
                self.image = next(self.pick_up_animation)
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.image.set_colorkey((0, 0, 0))
                self.image = self.image.convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)
                screen.blit(self.image, self.rect)
                self.count += 1
            else:
                self.image.set_colorkey((0, 0, 0))
                self.image = self.image.convert_alpha()
                self.mask = pygame.mask.from_surface(self.image.convert_alpha())
                screen.blit(self.image, self.rect)
        else:
            self.image = pygame.Surface([640, 480], pygame.SRCALPHA, 32)
            self.image = self.image.convert_alpha()
            screen.blit(self.image, self.rect)
