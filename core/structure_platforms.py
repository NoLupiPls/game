import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture, frame_duration=200):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.size = size
        if self.size > 48:
            self.size = 48
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, size, size)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.frame_duration = frame_duration

    def update_texture(self, new_texture):
        self.image = pygame.image.load(new_texture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

class End(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture, frame_duration=200):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.size = size
        if self.size > 48:
            self.size = 48
        self.image = pygame.transform.scale(self.image.convert_alpha(), (size, size))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = pygame.Rect(x, y, size, size)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.frame_duration = frame_duration

    def update_texture(self, new_texture):
        self.image = pygame.image.load(new_texture)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        self.size = size
        if self.size > 48:
            self.size = 48
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(x, y, size, size)

    def update_texture(self, new_texture):
        self.image = pygame.image.load(new_texture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
