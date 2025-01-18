from entities.player import Player
from entities.hazards import *
from entities.platform import *
from ui.menu import difficulty
from levels.level_parser import LevelParser
from core.settings import *
import os


player = Player(0, 0, difficulty)
levelparse = LevelParser.parse_level(os.path.join('tests', 'level.txt'))
all_sprites = levelparse['all_sprites']
blocks = levelparse['blocks']
platforms = levelparse['platform']
traps = levelparse['traps']

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ... # call pause menu
    all_sprites.update()
    blocks.update()
    platforms.update()
    traps.update()
