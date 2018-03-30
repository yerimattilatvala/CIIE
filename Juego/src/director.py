# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
from escena import *
from pygame.locals import *

FPS = 60

class Director():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Juego con escenas")


        # Pila de escenas
        self.pila = []
        # Flag que nos indica cuando quieren salir de la escena
        self.salir_escena = False
        


    def bucle(self, escena):

        # Reloj de pygame
        reloj = pygame.time.Clock()

        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:

            # Sincronizar el juego a 60 fps
            tiempo_pasado = reloj.tick(FPS)
            
            # Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()


    def ejecutar(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.pila)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila)-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            self.bucle(escena)

            '''
            # Si la escena es de pyame
            if isinstance(escena, EscenaPygame):

                # Ejecutamos el bucle
                self.buclePygame(escena)

            # Si no, si la escena es de pyglet
            elif isinstance(escena, EscenaPyglet):

                # Ejecutamos la aplicacion de pyglet
                pyglet.app.run()

                # Cuando hayamos terminado la animacion con pyglet, cerramos la ventana
                escena.close()

            else:
                raise Exception('No se que tipo de escena es')
            '''


    def pararEscena(self):
        if (len(self.pila)>0):
            escena = self.pila[len(self.pila)-1]
            # Indicamos en el flag que se quiere salir de la escena
            self.salir_escena = True

            '''
            # Si la escena es de pygame
            if isinstance(escena, EscenaPygame):
                # Indicamos en el flag que se quiere salir de la escena
                self.salir_escena_pygame = True
            # Si es una escena de pyglet
            elif isinstance(escena, EscenaPyglet):
                # Salimos del bucle de pyglet
                pyglet.app.exit()
            else:
                raise Exception('No se que tipo de escena es')
            '''

    def salirEscena(self):
        self.pararEscena()
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.pila)>0):
            self.pila.pop()

    def salirPrograma(self):
        self.pararEscena()
        # Vaciamos la lista de escenas pendientes
        self.pila = []

    def cambiarEscena(self, escena):
        self.pararEscena()
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.pila)>0):
            self.pila.pop()
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)

    def apilarEscena(self, escena):
        self.pararEscena()
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.pila.append(escena)