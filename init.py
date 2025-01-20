from entities.player import Player
from entities.hazards import *
from entities.platform import *
from ui.menu import difficulty
from levels.level_parser import LevelParser
from core.settings import *
import os
import ui.menu


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
j = ui.menu.main_menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ... # call pause menu