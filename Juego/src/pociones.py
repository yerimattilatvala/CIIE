import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *
from values import *
from escena import *
from personajes import MAX_VIDA_JUGADOR

class PocionCerveza(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posX = 0
        self.posY = 0

        self.retardoAnimacion = 10

        self.scalex = 85
        self.scaley = 112

        self.currentImage = 0

        self.images = []
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/0.png',-1),(self.scalex,self.scaley)).convert_alpha())
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/1.png',-1),(self.scalex,self.scaley)).convert_alpha())
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/2.png',-1),(self.scalex,self.scaley)).convert_alpha())
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/3.png',-1),(self.scalex,self.scaley)).convert_alpha())
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/4.png',-1),(self.scalex,self.scaley)).convert_alpha())
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/5.png',-1),(self.scalex,self.scaley)).convert_alpha())

        self.rect = pygame.Rect(self.posX,self.posY,85,112)
    
    def updatePos(self,x,y):
        self.posX = x
        self.posY = y
        self.rect = pygame.Rect(self.posX,self.posY,85,112)

    def update(self,scrollX):
        self.rect.left = self.posX-scrollX

        self.retardoAnimacion -= 1
        if self.retardoAnimacion < 0:
            self.retardoAnimacion = 10

    def draw(self,pantalla,scrollX):

        if self.retardoAnimacion <= 0:
            self.currentImage += 1

        if self.currentImage >= len(self.images):
            self.currentImage = 0
        
        pantalla.blit(self.images[self.currentImage],(self.posX-scrollX,self.posY))
        #self.rect = self.images[self.currentImage].get_rect()
        #self.rect.left = self.posX-scrollX

    def collect(self,jugador):
        jugador.vida += 2
        if jugador.vida > MAX_VIDA_JUGADOR:
            jugador.vida = MAX_VIDA_JUGADOR
  