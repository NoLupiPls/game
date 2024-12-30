import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture, frame_duration=200):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.size = size
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, x + size, y + size)
        self.frame_duration = frame_duration

    def update_texture(self, new_texture):
        self.image = pygame.image.load(new_texture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, x + size, y + size)

    def update_texture(self, new_texture):
        self.image = pygame.image.load(new_texture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
