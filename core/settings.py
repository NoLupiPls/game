# Настройки окна
WIDTH = 1400         # Ширина окна
HEIGHT = 700        # Высота окна
FPS = 60            # Кадры в секунду
TITLE = "Game"      # Заголовок окна
DIFFICULTY = 'easy'
# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (30, 30, 30)  # Фон (темно-серый)

# Настройки игрока
PLAYER_SIZE_X = 24          # Размер игрока (высота персонажа)
PLAYER_SIZE_Y = 36
PLAYER_COLOR = WHITE      # Цвет игрока
PLAYER_SPEED = 5          # Скорость игрока (пикселей за тик)

# Настройки уровня
TILE_SIZE = 31            # Размер тайла (ширина и высота в пикселях)

# Пути к ресурсам
ASSETS_DIR = "assets/"            # Общая папка с ресурсами
IMAGES_DIR = ASSETS_DIR + "images/"  # Папка с изображениями
SOUNDS_DIR = ASSETS_DIR + "sounds/"  # Папка с аудиофайлами
LEVELS_DIR = ASSETS_DIR + "levels/"  # Папка с уровнями
FONTS_DIR = ASSETS_DIR + "fonts/"    # Папка со шрифтами
MUSIC_DIR = ASSETS_DIR + "music/"    # Папка с музыкой

# Прочие настройки
GRAVITY = 1.5             # Сила гравитации
MAX_FALL_SPEED = 10       # Максимальная скорость падения
JUMP_POWER = -300          # Сила прыжка
