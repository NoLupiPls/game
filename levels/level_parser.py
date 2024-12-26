import pygame
from entities.collectibles import Collectible


class LevelParser:
    def __init__(self, tile_size):
        """
        Инициализация парсера уровня.
        """
        self.tile_size = tile_size

    def parse_level_file(self, filepath):
        """
        Читает файл уровня и преобразует его в игровые объекты.
        """
        platforms = []
        collectibles = []

        try:
            with open(filepath, "r") as file:
                lines = file.readlines()

            for row, line in enumerate(lines):
                for col, char in enumerate(line.strip()):
                    x = col * self.tile_size
                    y = row * self.tile_size

                    # Создаем объекты в зависимости от символа
                    if char == "#":  # Символ платформы
                        platforms.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
                    elif char == "C":  # Символ собираемого объекта
                        collectibles.append(Collectible(x + self.tile_size // 4, y + self.tile_size // 4, self.tile_size // 2, (255, 255, 0)))
        except FileNotFoundError:
            print(f"Ошибка: файл уровня '{filepath}' не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке уровня: {e}")

        return platforms, collectibles
    