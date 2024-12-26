import pygame
import sys


class Platform(object):
    def __init__(self, texture, rect):
        self.texture = texture
        self.rect = rect
        self.image = pygame.image.load(texture)

    def draw(self, screen):
        resize = pygame.transform.scale(self.texture, self.rect)
        pygame.draw.rect(screen, resize, self.rect)


class Character(object):
    def __init__(self, texture, rect, speed):
        self.rect = rect
        self.texture = texture
        (self.dx, self.dy) = speed
        self.is_falling = True

    def update(self, platforms):
        self.is_falling = True
        for platform in platforms:
            if self.is_on(platform):
                self.rect.bottom = platform.rect.top
                self.dy = 0
                self.is_falling = False

        if self.is_falling:
            self.gravity()
        self.rect.x += self.dx
        self.rect.y += self.dy

    def is_on(self, platform):
        return (pygame.Rect(self.rect.x, self.rect.y + self.dy,
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dy > 0)

    def left(self):
        self.dx = -5

    def right(self):
        self.dx = 5

    def stop_x(self):
        self.dx = 0

    def jump(self):
        if self.dy == 0:
            self.dy = -25

    def gravity(self):
        self.dy += 5


def key_down(event, character):
    if event.key == pygame.K_LEFT:
        character.left()
    elif event.key == pygame.K_RIGHT:
        character.right()
    elif event.key == pygame.K_UP:
        character.jump()

def key_up(event, character):
    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
        character.stop_x()

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("PyPlatformer")
    hero = Character((255, 255, 0), pygame.Rect(100, 0, 20, 20), (0, 0))
    platform1 = Platform((0, 255, 255), pygame.Rect(100, 100, 100, 10))
    platform2 = Platform((0, 255, 255), pygame.Rect(150, 150, 100, 10))
    platforms = (platform1, platform2)
    clock = pygame.time.Clock()
    heros = (hero, )
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_down(event, hero)
            elif event.type == pygame.KEYUP:
                key_up(event, hero)

        screen.fill((0, 0, 0))
        hero.update(platforms)
        [platform.draw(screen) for platform in platforms]
        [_.draw(screen) for _ in heros]
        pygame.display.update()


main()
