# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from gestorRecursos import *
# -------------------------------------------------
# Clase Decorado


ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# -------------------------------------------------
# Clase Fase

# Clase Fase

class Fase:
    def __init__(self):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Creamos el decorado y el fondo
        self.decorado = Decorado()
        #self.fondo = Cielo()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        # self.jugador = Jugador()
        # self.grupoJugadores = pygame.sprite.Group( self.jugador)

        # Ponemos a los jugadores en sus posiciones iniciales
        # self.jugador.establecerPosicion((200, 551))

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        # self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1, self.jugador2, enemigo1 )
        # Creamos otro grupo con todos los Sprites
        # self.grupoSprites = pygame.sprite.Group( self.jugador1, self.jugador2, enemigo1, plataformaSuelo, plataformaCasa )


    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        #self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        # self.grupoSprites.draw(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT:
                return True

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)
        # No se sale del programa
        return False


class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('decorado.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 300))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)