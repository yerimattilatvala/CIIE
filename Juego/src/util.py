# encoding: utf-8
import pygame
from globals import *
from text import *


def load_image(file_name, colorkey=False):
    file = path.join(IMAGE_DIR, file_name)
    image = pygame.image.load(file)
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            image = image.convert()
    else:
        image = image.convert_alpha()
    return image

def load_description_main_menu(item_name):
    text = None
    if item_name == MENU_OPTIONS[0]:
        text = DESCRIPTION_MENU[0]
    if item_name == MENU_OPTIONS[1]:
        text = DESCRIPTION_MENU[1]
    print(text)
    if not (text is None):
        text = Text(text,24,FONT_MENU)
    return text
        