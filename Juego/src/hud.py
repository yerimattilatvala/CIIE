import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *
from values import *
from escena import *

class Hud(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.rect = pygame.Rect(0, 0, 100, 50)
        self.image = GestorRecursos.CargarImagen(CERVEZA_8,-1)
        self.rect = self.image.get_rect()

    def update(self,jugador):
        if jugador.vida == 8:
            finalImage = CERVEZA_8
        elif jugador.vida == 7:
            finalImage = CERVEZA_7
        elif jugador.vida == 6:
            finalImage = CERVEZA_6
        elif jugador.vida == 5:
            finalImage = CERVEZA_5
        elif jugador.vida == 4:
            finalImage = CERVEZA_4
        elif jugador.vida == 3:
            finalImage = CERVEZA_3
        elif jugador.vida == 2:
            finalImage = CERVEZA_2
        elif jugador.vida == 1:
            finalImage = CERVEZA_1
        elif jugador.vida == 0:
            finalImage = CERVEZA_0

        self.image = GestorRecursos.CargarImagen(finalImage,-1)





