import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *
from values import *
from escena import *

class Hud(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 80

        self.topPadding = 70

        self.scalex = 50
        self.scaley = 50

        self.image0 = pygame.transform.scale(GestorRecursos.CargarImagen(CERVEZA_0,-1),(self.scalex,self.scaley)).convert_alpha()
        self.image1 = pygame.transform.scale(GestorRecursos.CargarImagen(CERVEZA_1,-1),(self.scalex,self.scaley)).convert_alpha()
        self.image2 = pygame.transform.scale(GestorRecursos.CargarImagen(CERVEZA_2,-1),(self.scalex,self.scaley)).convert_alpha()
        self.image3 = pygame.transform.scale(GestorRecursos.CargarImagen(CERVEZA_3,-1),(self.scalex,self.scaley)).convert_alpha()
        self.image4 = pygame.transform.scale(GestorRecursos.CargarImagen(CERVEZA_4,-1),(self.scalex,self.scaley)).convert_alpha()

    def update(self,jugador):
        self.vida = jugador.vida

    def draw(self,pantalla):
        auxVida = self.vida
        auxCounter = 1

        while auxVida >= 4:
            pantalla.blit(self.image1,(self.scalex * auxCounter,self.topPadding))
            auxCounter += 1
            auxVida -= 4

        if auxVida == 3:
            pantalla.blit(self.image2,(self.scalex * auxCounter,self.topPadding))
        elif auxVida == 2:
            pantalla.blit(self.image3,(self.scalex * auxCounter,self.topPadding))
        elif auxVida == 1:
            pantalla.blit(self.image4,(self.scalex * auxCounter,self.topPadding))
        else:
            pantalla.blit(self.image0,(self.scalex * auxCounter,self.topPadding))






