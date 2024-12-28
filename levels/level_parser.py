import pygame
from core.block import Block
from core.platform import Platform
from traps import Spike

class LevelParser:
    TILE_SIZE = 16  # Размер каждого блока в пикселях
    SCREEN_WIDTH = 40  # Количество блоков по ширине
    SCREEN_HEIGHT = 22  # Количество блоков по высоте

    SYMBOLS = {
        "G": "dirt",          # Грязь
        "I": "ice",           # Лёд
        "L": "ladder",         # Каркас
        "B": "stone_brick",   # Каменный кирпич
        "S": "spike",         # Шипы
        "W": "wood_platform",  # Деревянная платформа
        "P": "stone_platform", # Каменная платформа
    }

    TEXTURE_PATHS = {
        # Блоки
        "dirt": {
            "default": "assets/blocks/dirt/dirt.png",
            "vertical": "assets/blocks/dirt/dirt_vertical.png",
            "horizontal": "assets/blocks/dirt/dirt_horizontal.png",
            "top": "assets/blocks/dirt/dirt_top.png",
            "bottom": "assets/blocks/dirt/dirt_bottom.png",
            "isolated": "assets/blocks/dirt/dirt_isolated.png",
            "black": "assets/blocks/dirt/dirt_black.png",
            "top_bottom_left": "assets/blocks/dirt/dirt_atbl.png",
            "top_bottom_right": "assets/blocks/dirt/dirt_atbr.png",
            "top_left_right": "assets/blocks/dirt/dirt_black.png",
            "bottom_left_right": "assets/blocks/dirt/dirt_ablr.png",
            "angle_top_left": "assets/blocks/dirt/dirt_atl.png",
            "angle_top_right": "assets/blocks/dirt/dirt_atr.png",
            "angle_bottom_left": "assets/blocks/dirt/dirt_abl.png",
            "angle_bottom_right": "assets/blocks/dirt/dirt_abr.png",
        },
        "ice": {
            "default": "assets/blocks/ice/ice.png",
            "vertical": "assets/blocks/ice/ice_vertical.png",
            "horizontal": "assets/blocks/ice/ice_horizontal.png",
            "top": "assets/blocks/ice/ice_top.png",
            "bottom": "assets/blocks/ice/ice_bottom.png",
            "isolated": "assets/blocks/ice/ice_isolated.png",
            "black": "assets/blocks/ice/ice_black.png",
            "top_bottom_left": "assets/blocks/ice/ice_tbl.png",
            "top_bottom_right": "assets/blocks/ice/ice_tbr.png",
            "top_left_right": "assets/blocks/ice/ice_tlr.png",
            "bottom_left_right": "assets/blocks/ice/ice_blr.png",
            "angle_top_left": "assets/blocks/ice/ice_atl.png",
            "angle_top_right": "assets/blocks/ice/ice_atr.png",
            "angle_bottom_left": "assets/blocks/ice/ice_abl.png",
            "angle_bottom_right": "assets/blocks/ice/ice_abr.png",
        },
        "ladder": {
            "default": "assets/blocks/frame.png",
            "vertical": "assets/blocks/frame_vertical.png",
            "horizontal": "assets/blocks/frame_horizontal.png",
            "isolated": "assets/blocks/frame_isolated.png",
        },
        "stone_brick": {
            "default": "assets/blocks/stone_brick.png",
            "vertical": "assets/blocks/stone_brick_vertical.png",
            "horizontal": "assets/blocks/stone_brick_horizontal.png",
            "isolated": "assets/blocks/stone_brick_isolated.png",
        },
        # Платформы
        "wood_platform": {
            "default": "assets/platforms/wood_platform.png",
            "supported_left": "assets/platforms/wood_platform_supported_left.png",
            "supported_right": "assets/platforms/wood_platform_supported_right.png",
        },
        "stone_platform": {
            "default": "assets/platforms/stone_platform.png",
            "connected_left": "assets/platforms/stone_platform_connected_left.png",
            "connected_right": "assets/platforms/stone_platform_connected_right.png",
            "connected_both": "assets/platforms/stone_platform_connected_both.png",
        },
        # Шипы
        "spike": {
            "default": "assets/traps/spike.png",
            "top": "assets/traps/spike_top.png",
            "bottom": "assets/traps/spike_bottom.png",
            "left": "assets/traps/spike_left.png",
            "right": "assets/traps/spike_right.png",
        },
    }

    @classmethod
    def parse_level(cls, level_file):
        """Загружает уровень из текстового файла и создает игровые объекты."""
        with open(level_file, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        all_sprites = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        traps = pygame.sprite.Group()

        block_grid = [[None for _ in range(cls.SCREEN_WIDTH)] for _ in range(cls.SCREEN_HEIGHT)]

        # Первоначальная загрузка блоков и объектов
        for row_index, line in enumerate(lines):
            for col_index, symbol in enumerate(line):
                if symbol in cls.SYMBOLS:
                    x = col_index * cls.TILE_SIZE
                    y = row_index * cls.TILE_SIZE

                    item_type = cls.SYMBOLS[symbol]
                    if item_type in {"dirt", "ice", "frame", "stone_brick"}:
                        block = Block(x, y, cls.TILE_SIZE, cls.TEXTURE_PATHS[item_type]["default"])
                        block_grid[row_index][col_index] = block
                        blocks.add(block)
                        all_sprites.add(block)

                    elif item_type == "wood_platform":
                        platform = Platform(x, y, cls.TILE_SIZE, cls.TEXTURE_PATHS[item_type]["default"])
                        block_grid[row_index][col_index] = platform
                        platforms.add(platform)
                        all_sprites.add(platform)

                    elif item_type == "stone_platform":
                        platform = Platform(x, y, cls.TILE_SIZE, cls.TEXTURE_PATHS[item_type]["default"])
                        block_grid[row_index][col_index] = platform
                        platforms.add(platform)
                        all_sprites.add(platform)

                    elif item_type == "spike":
                        spike = Spike(x, y, cls.TILE_SIZE, cls.TEXTURE_PATHS[item_type]["default"])
                        block_grid[row_index][col_index] = spike
                        traps.add(spike)
                        all_sprites.add(spike)

        # Обновление текстур блоков, платформ и шипов
        for row_index, row in enumerate(block_grid):
            for col_index, block in enumerate(row):
                if not block:
                    continue

                item_type = cls.SYMBOLS.get(lines[row_index][col_index])
                if item_type in cls.TEXTURE_PATHS:
                    neighbors = cls.get_neighbors(block_grid, row_index, col_index)
                    texture = cls.get_texture(item_type, neighbors)
                    block.update_texture(texture)

        return {
            "all_sprites": all_sprites,
            "blocks": blocks,
            "platforms": platforms,
            "traps": traps,
        }

    @staticmethod
    def get_neighbors(grid, row, col):
        """Определяет, есть ли соседи вокруг текущей позиции."""
        neighbors = {
            "top": row > 0 and grid[row - 1][col] is not None,
            "bottom": row < len(grid) - 1 and grid[row + 1][col] is not None,
            "left": col > 0 and grid[row][col - 1] is not None,
            "right": col < len(grid[0]) - 1 and grid[row][col + 1] is not None,
        }
        return neighbors

    @classmethod
    def get_texture(cls, item_type, neighbors):
        """Выбирает текстуру в зависимости от соседей."""
        if item_type in {"dirt", "ice", "frame", "stone_brick"}:
            if neighbors["top"] and neighbors["bottom"]: # Вертикальный блок
                return cls.TEXTURE_PATHS[item_type]["vertical"]
            elif neighbors["bottom"]: # Верхний блок
                return cls.TEXTURE_PATHS[item_type]["bottom"]
            elif neighbors["top"]: # Нижний блок
                return cls.TEXTURE_PATHS[item_type]["top"]
            
            elif neighbors["left"] and neighbors["right"]: # Горизонтальный блок
                return cls.TEXTURE_PATHS[item_type]["horizontal"]
            elif neighbors["left"]: # Правый блок
                return cls.TEXTURE_PATHS[item_type]["left"]
            elif neighbors["right"]: # Левый блок
                return cls.TEXTURE_PATHS[item_type]["right"]
            
            elif neighbors["top"] and neighbors["left"]: # Угловой блок
                return cls.TEXTURE_PATHS[item_type]["angle_top_left"]
            elif neighbors["top"] and neighbors["right"]: # Угловой блок
                return cls.TEXTURE_PATHS[item_type]["angle_top_right"]
            
            elif neighbors["bottom"] and neighbors["left"]: # Угловой блок
                return cls.TEXTURE_PATHS[item_type]["angle_bottom_left"]
            elif neighbors["bottom"] and neighbors["right"]: # Угловой блок
                return cls.TEXTURE_PATHS[item_type]["angle_bottom_right"]
            
            elif neighbors["top"] and neighbors["bottom"] and neighbors["left"]:
                return cls.TEXTURE_PATHS[item_type]["angle_top_bottom_left"]
            elif neighbors["top"] and neighbors["bottom"] and neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["angle_top_bottom_right"]
            elif neighbors["top"] and neighbors["left"] and neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["angle_top_left_right"]
            elif neighbors["bottom"] and neighbors["left"] and neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["angle_bottom_left_right"]
            elif neighbors["top"] and neighbors["bottom"] and neighbors["left"] and neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["black"]
            
            else:
                return cls.TEXTURE_PATHS[item_type]["isolated"] # Изолированный блок

        if item_type == "wood_platform":
            if neighbors["left"]:
                return cls.TEXTURE_PATHS[item_type]["supported_left"]
            elif neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["supported_right"]
            else:
                return cls.TEXTURE_PATHS[item_type]["default"]

        if item_type == "stone_platform":
            if neighbors["left"] and neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["connected_both"]
            elif neighbors["left"]:
                return cls.TEXTURE_PATHS[item_type]["connected_left"]
            elif neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["connected_right"]
            else:
                return cls.TEXTURE_PATHS[item_type]["default"]

        if item_type == "spike":
            if neighbors["top"]:
                return cls.TEXTURE_PATHS[item_type]["top"]
            elif neighbors["bottom"]:
                return cls.TEXTURE_PATHS[item_type]["bottom"]
            elif neighbors["left"]:
                return cls.TEXTURE_PATHS[item_type]["left"]
            elif neighbors["right"]:
                return cls.TEXTURE_PATHS[item_type]["right"]
            else:
                return cls.TEXTURE_PATHS[item_type]["default"]

        return cls.TEXTURE_PATHS[item_type]["default"]
    