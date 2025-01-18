import pygame, sys
import os
from core.settings import *


difficulty = 'easy'

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu', 'menu_background_19201080.png'))

os.path.join('assets', 'fonts', 'mainmenufont.otf')


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join('assets', 'fonts', 'mainmenufont.otf'), size)


def rescale_bg():
    global BG
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

def new_game_choose_difficulty():
    buttons = []
    while True:
        NGCD_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        NGCD_TEXT = get_font(100).render("CHOOSE DIFFICULTY", True, "#b68f40")
        NGCD_RECT = NGCD_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        SCREEN.blit(NGCD_TEXT, NGCD_RECT)

        NGCD_DIFF_MODE_EASY = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                'play_button.png')), pos=(WIDTH // 2, HEIGHT // 2),
                           text_input="EASY", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(NGCD_DIFF_MODE_EASY)

        NGCD_DIFF_MODE_MEDIUM = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                          'play_button.png')),
                                     pos=(WIDTH // 2, HEIGHT // 1.575),
                                     text_input="MEDUIM", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(NGCD_DIFF_MODE_MEDIUM)

        NGCD_DIFF_MODE_HARD = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                          'play_button.png')),
                                     pos=(WIDTH // 2, HEIGHT // 1.3),
                                     text_input="HARD", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(NGCD_DIFF_MODE_HARD)

        for button in buttons:
            button.changeColor(NGCD_MOUSE_POS)
            button.update(SCREEN)
        difficulty = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NGCD_DIFF_MODE_EASY.checkForInput(NGCD_MOUSE_POS):
                    difficulty = 'easy' # call game init and terminate menu
                if NGCD_DIFF_MODE_MEDIUM.checkForInput(NGCD_MOUSE_POS):
                    difficulty = 'meduim' # call game init and terminate menu
                if NGCD_DIFF_MODE_HARD.checkForInput(NGCD_MOUSE_POS):
                    difficulty = 'hard' # call game init and terminate menu
        pygame.display.update()

def play():
    buttons = []
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        LOAD_GAME = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                'play_button.png')), pos=(WIDTH // 2, HEIGHT // 2),
                           text_input="Load game", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(LOAD_GAME)
        NEW_GAME = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                'play_button.png')), pos=(WIDTH // 2, HEIGHT // 3),
                           text_input="New game", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(NEW_GAME)
        PLAY_BACK = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                'play_button.png')), pos=(WIDTH // 2, HEIGHT // 1.5),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        buttons.append(PLAY_BACK)

        for button in buttons:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if LOAD_GAME.checkForInput(PLAY_MOUSE_POS):
                    ...
                if NEW_GAME.checkForInput(PLAY_MOUSE_POS):
                    new_game_choose_difficulty()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")


        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    rescale_bg()
    running = True
    while running:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Game name", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                  'play_button.png')),
                             pos=(WIDTH // 4, HEIGHT // 3),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                     'menu_options_button.png')),
                                pos=(WIDTH // 4, HEIGHT // 2),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                  'menu_quit_button.png')),
                             pos=(WIDTH // 4, HEIGHT // 1.5),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
