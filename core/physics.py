import pygame


class PhysicsEngine:
    """Обрабатывает физику объектов в игре, включая гравитацию и столкновения."""
    def __init__(self, gravity=0.5):
        self.gravity = gravity  # Сила гравитации

    def apply_gravity(self, entity):
        """Применяет гравитацию к объекту."""
        entity.velocity.y += self.gravity
        entity.rect.y += entity.velocity.y

    def check_collisions(self, entity, tiles):
        """
        Проверяет и обрабатывает столкновения объекта с блоками.
        :param entity: объект с физикой (например, игрок или враг).
        :param tiles: список прямоугольников, представляющих коллизионные блоки.
        """
        # Проверка столкновений по оси Y
        entity.rect.y += entity.velocity.y
        collisions = self.get_collisions(entity, tiles)
        for tile in collisions:
            if entity.velocity.y > 0:  # Падение
                entity.rect.bottom = tile.top
                entity.velocity.y = 0
                entity.on_ground = True
            elif entity.velocity.y < 0:  # Прыжок
                entity.rect.top = tile.bottom
                entity.velocity.y = 0

        # Проверка столкновений по оси X
        entity.rect.x += entity.velocity.x
        collisions = self.get_collisions(entity, tiles)
        for tile in collisions:
            if entity.velocity.x > 0:  # Движение вправо
                entity.rect.right = tile.left
            elif entity.velocity.x < 0:  # Движение влево
                entity.rect.left = tile.right
            entity.velocity.x = 0

    def get_collisions(self, entity, tiles):
        """Возвращает список блоков, с которыми пересекается объект."""
        return [tile for tile in tiles if entity.rect.colliderect(tile)]


class Entity:
    """Пример объекта с физикой."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def move(self, dx, dy):
        """Перемещает объект."""
        self.rect.x += dx
        self.rect.y += dy

    def jump(self, strength):
        """Заставляет объект прыгать, если он находится на земле."""
        if self.on_ground:
            self.velocity.y = -strength
            self.on_ground = False
            