# -*- coding: utf-8 -*-
import pygame,os
from pygame.locals import * 
from values import *


class Text():
    def __init__(self, text, size, font, color=(255,255,255)):
        self.text = text
        self.size = size
        self.fuente = font
        self.color = color
        self.draw()

    def draw(self):
        font_obj = pygame.font.Font(os.path.join(FONT_DIR, self.fuente + ".TTF"), self.size)
        self.render = font_obj.render(self.text, True, self.color)
    
    def set_color(self,color):
        self.color = color
        self.draw()
