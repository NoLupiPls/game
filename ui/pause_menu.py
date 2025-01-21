# функция main должна будет вызываться из основного цикла по нажатию esc
# передаёт объект screen

import pygame, sys
import os
from core.settings import *


pygame.init()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join('assets', 'fonts', 'mainmenufont.otf'), size)


def main(screen):
    s = pygame.Surface((WIDTH, HEIGHT))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((0,0,0))           # this fills the entire surface
    screen.blit(s, (0,0))
    running = True
    while running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                  'play_button.png')),
                             pos=(WIDTH // 2, HEIGHT // 3),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                     'menu_options_button.png')),
                                pos=(WIDTH // 2, HEIGHT // 2),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(os.path.join('assets', 'images', 'ui', 'menu',
                                                                  'menu_quit_button.png')),
                             pos=(WIDTH // 2, HEIGHT // 1.5),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    # play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ...
                    # options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

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



