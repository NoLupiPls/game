import random
import os
import pygame
from core.structure_platforms import Block
from core.structure_platforms import Platform
from entities.hazards import Spike

class LevelParser:
    TILE_SIZE = 32  # Размер каждого блока в пикселях
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
            "default": os.path.join('assets', 'images', 'platform', 'blocks', 'dirt', 'dirt_black.png'),
            "vertical": "assets/images/platform/blocks/dirt/dirt_vertical.png",
            "horizontal": "assets/images/platform/blocks/dirt/dirt_blr.png",
            "top": "assets/images/platform/blocks/dirt/dirt_top.png",
            "bottom": "assets/images/platform/blocks/dirt/dirt_bottom.png",
            "left": "assets/images/platform/blocks/dirt/dirt_left.png",
            "right": "assets/images/platform/blocks/dirt/dirt_right.png",
            "isolated": "assets/images/platform/blocks/dirt/dirt_isolated.png",
            "black": "assets/images/platform/blocks/dirt/dirt_black.png",
            "top_bottom_left": "assets/images/platform/blocks/dirt/dirt_tbr.png",
            "top_bottom_right": "assets/images/platform/blocks/dirt/dirt_tbl.png",
            "top_left_right": "assets/images/platform/blocks/dirt/dirt_black.png",
            "bottom_left_right": "assets/images/platform/blocks/dirt/dirt_blr.png",
            "angle_top_left": "assets/images/platform/blocks/dirt/dirt_atl.png",
            "angle_top_right": "assets/images/platform/blocks/dirt/dirt_atr.png",
            "angle_bottom_left": "assets/images/platform/blocks/dirt/dirt_abl.png",
            "angle_bottom_right": "assets/images/platform/blocks/dirt/dirt_abr.png",
        },
        "ice": {
            "default": "assets/images/platform/blocks/ice/ice.png",
            "vertical": "assets/images/platform/blocks/ice/ice_vertical.png",
            "horizontal": "assets/images/platform/blocks/ice/ice_horizontal.png",
            "top": "assets/images/platform/blocks/ice/ice_top.png",
            "bottom": "assets/images/platform/blocks/ice/ice_bottom.png",
            "left": "assets/images/platform/blocks/ice/ice_left.png",
            "right": "assets/images/platform/blocks/ice/ice_right.png",
            "isolated": "assets/images/platform/blocks/ice/ice_isolated.png",
            "black": "assets/images/platform/blocks/ice/ice_black.png",
            "top_bottom_left": "assets/images/platform/blocks/ice/ice_tbl.png",
            "top_bottom_right": "assets/images/platform/blocks/ice/ice_tbr.png",
            "top_left_right": "assets/images/platform/blocks/ice/ice_tlr.png",
            "bottom_left_right": "assets/images/platform/blocks/ice/ice_blr.png",
            "angle_top_left": "assets/images/platform/blocks/ice/ice_atl.png",
            "angle_top_right": "assets/images/platform/blocks/ice/ice_atr.png",
            "angle_bottom_left": "assets/images/platform/blocks/ice/ice_abl.png",
            "angle_bottom_right": "assets/images/platform/blocks/ice/ice_abr.png",
        },
        "ladder": {
            "vertical": "assets/images/platform/blocks/ladder_vertical.png",
            "horizontal": "assets/images/platform/blocks/ladder_horizontal.png",
            "isolated": "assets/images/platform/blocks/ladder_isolated.png",
        },
        "stone_brick": {
            "default": "assets/images/platform/blocks/stone_brick.png",
            "vertical": "assets/images/platform/blocks/stone_brick_vertical.png",
            "horizontal": "assets/images/platform/blocks/stone_brick_horizontal.png",
            "isolated": "assets/images/platform/blocks/stone_brick_isolated.png",
            "black": "assets/images/platform/blocks/stone_brick_black.png",
            "top": "assets/images/platform/blocks/stone_brick_top.png",
            "bottom": "assets/images/platform/blocks/stone_brick_bottom.png",
            "left": "assets/images/platform/blocks/stone_brick_left.png",
            "right": "assets/images/platform/blocks/stone_brick_right.png",
            "angle_top_left": "assets/images/platform/blocks/stone_brick_atl.png",
            "angle_top_right": "assets/images/platform/blocks/stone_brick_atr.png",
            "angle_bottom_left": "assets/images/platform/blocks/stone_brick_abl.png",
            "angle_bottom_right": "assets/images/platform/blocks/stone_brick_abr.png",
            "top_bottom_left": "assets/images/platform/blocks/stone_brick_atbl.png",
            "top_bottom_right": "assets/images/platform/blocks/stone_brick_tbr.png",
            "top_left_right": "assets/images/platform/blocks/stone_brick_atlr.png",
            "bottom_left_right": "assets/images/platform/blocks/stone_brick_ablr.png",

        },
        # Платформы
        "wood_platform": {
            "default": "assets/platform/platform/wood_platform/wood_platform.png",
            "supported_left": "assets/platform/platform/wood_platform/wood_platform_supported_left.png",
            "supported_right": "assets/platform/platform/wood_platform/wood_platform_supported_right.png",
        },
        "stone_platform": {
            "default": "assets/platform/platform/stone_platform/default.png",
            "connected_left": "assets/platform/platform/stone_platform/default.png",
            "connected_right": "assets/platform/platform/stone_platform/default.png",
            "connected_both": "assets/platform/platform/stone_platform/default.png",
        },
        # Шипы
        "spike": {
            "top": "assets/images/hazards/spikes/spike_top.png",
            "bottom": "assets/images/hazards/spikes/spike_bottom.png",
            "left": "assets/images/hazards/spikes/spike_left.png",
            "right": "assets/images/hazards/spikes/spike_right.png",
        },
    }

    GRASS_ANIMATION_PATHS = [
        os.path.join('assets', 'images', 'platform', 'animations', 'grass', 'grass_1.png'),
        "assets/images/platform/animations/grass/grass_2.png",
        "assets/images/platform/animations/grass/grass_3.png",
    ]

    GRASS_ANIMATION_CHANCE = 0.2

    @classmethod
    def parse_level(cls, level_file):
        """Загружает уровень из текстового файла и создает игровые объекты."""
        with open(level_file, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        all_sprites = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        animations = pygame.sprite.Group()
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
                    if item_type in {"dirt", "ice", "ladder", "stone_brick"}:
                        block = Block(x, y, cls.TILE_SIZE, cls.TEXTURE_PATHS[item_type]["default"])
                        block_grid[row_index][col_index] = block
                        blocks.add(block)
                        all_sprites.add(block)
                        if item_type in {"dirt", "stone_brick"}:
                            if random.random() < cls.GRASS_ANIMATION_CHANCE:
                                grass_animation = Block(
                                    x, y - 4,
                                    cls.TILE_SIZE,
                                    cls.GRASS_ANIMATION_PATHS[random.randrange(0, 3)],
                                    frame_duration=200,
                                    )
                                animations.add(grass_animation)
                                all_sprites.add(grass_animation)

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
            "platform": platforms,
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
    