#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import fase
from fase import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Creamos la fase
    fase = Fase()



    # Se dibuja en pantalla
    fase.dibujar(pantalla)
    pygame.display.flip()

