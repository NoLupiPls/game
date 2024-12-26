import pygame


class Collectible:
    def __init__(self, x, y, size, color):
        """
        Инициализация объекта, который можно собирать.
        """
        self.rect = pygame.Rect(x, y, size, size)  # Прямоугольник для коллизий
        self.color = color  # Цвет объекта
        self.collected = False  # Флаг, собран ли объект

    def check_collision(self, player_rect):
        """
        Проверяет столкновение с игроком.
        """
        if self.rect.colliderect(player_rect):
            self.collected = True

    def render(self, screen):
        """
        Отрисовывает объект, если он не собран.
        """
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)
