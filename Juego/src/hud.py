import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *
from values import *
from escena import *
from personajes import MAX_VIDA_JUGADOR

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
        auxVida = MAX_VIDA_JUGADOR
        auxCounter = 1
        while auxVida > 0:
            self.blit_alpha(pantalla,self.image1,(self.scalex * auxCounter,self.topPadding),64)
            auxCounter += 1
            auxVida -= 4

        auxVida = self.vida
        auxCounter = 1

        while auxVida >= 4:
            #self.blit_alpha(pantalla,self.image1,(self.scalex * auxCounter,self.topPadding),128)
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

    def blit_alpha(self,target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)






