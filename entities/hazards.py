import pygame


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, x + size, y + size)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, x + size, y + size)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
