# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ATACAR = 5

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2
SPRITE_ATACANDO = 3
SPRITE_ATACANDO_EN_SALTO = 4
SPRITE_MUERTE = 5

#Tiempos que duran las animaciones
DURACION_MUERTE_SNIPER = 55
DURACION_MUERTE_JUGADOR = 35
DURACION_ATACAR = 10

#Dano personajes
MAX_VIDA_JUGADOR = 40
VIDA_JUGADOR = MAX_VIDA_JUGADOR
VIDA_SNIPER = 100

#Dano personajes
DANO_JUGADOR = 40
DANO_SNIPER = 1

#Frames de invencibilidad despues de ser atacados
INVULNERABLE_JUGADOR = 20
INVULNERABLE_SNIPER = 10

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

VELOCIDAD_SNIPER = 0.12 # Pixeles por milisegundo
VELOCIDAD_SALTO_SNIPER = 0.27 # Pixeles por milisegundo
RETARDO_ANIMACION_SNIPER = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura
# El Sniper camina un poco más lento que el jugador, y salta menos

GRAVEDAD = 0.0003 # Píxeles / ms2

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.retardoAccion = 0
        self.atacando = False
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        #vida y dano
        self.vida = vida
        self.dano = dano
        self.iFrames = iFrames
        self.currentIFrames = 0
        self.duracionMuerte = duracionMuerte
        self.muerto = False

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = DERECHA
        self.mirandoAnterior = self.mirando

        self.padding = 0

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 6):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()

    def draw(self,pantalla):
        if self.mirandoAnterior == DERECHA:
            if self.mirando == IZQUIERDA:
                self.padding =  self.image.get_rect().width
                pantalla.blit(self.image,(self.rect.left - self.image.get_rect().width + self.padding , self.posicion[1] - self.image.get_rect().height))
            else:
                pantalla.blit(self.image,(self.rect.left, self.posicion[1] - self.image.get_rect().height))
        else:
            if self.mirando == IZQUIERDA:
                pantalla.blit(self.image,(self.rect.left - self.image.get_rect().width + self.padding , self.posicion[1] - self.image.get_rect().height))
            else:
                self.padding = 0
                pantalla.blit(self.image,(self.rect.left, self.posicion[1] - self.image.get_rect().height))


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        if movimiento == ARRIBA:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO or self.numPostura == SPRITE_ATACANDO_EN_SALTO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        else:
            self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        #Inicializamos la postura nueva
        posturaNueva = self.numPostura

        if posturaNueva == SPRITE_MUERTE:
            if self.duracionMuerte == 0:
                self.muerto = True
            self.duracionMuerte -= 1
            velocidadx = 0
            velocidady = 0
        else:
            # Las velocidades a las que iba hasta este momento
            (velocidadx, velocidady) = self.velocidad

            # Si vamos a la izquierda o a la derecha        
            if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
                # Esta mirando hacia ese lado
                self.mirandoAnterior = self.mirando
                self.mirando = self.movimiento

                # Si vamos a la izquierda, le ponemos velocidad en esa dirección
                if self.movimiento == IZQUIERDA:
                    velocidadx = -self.velocidadCarrera
                # Si vamos a la derecha, le ponemos velocidad en esa dirección
                else:
                    velocidadx = self.velocidadCarrera

                # Si no estamos en el aire
                if self.numPostura != SPRITE_SALTANDO:
                    #if self.atacando:
                    #    self.numPostura = SPRITE_ATACANDO
                    #   self.retardoAccion = DURACION_ATACAR
                    #else:
                        # La postura actual sera estar caminando
                    posturaNueva = SPRITE_ANDANDO
                    # Ademas, si no estamos encima de ninguna plataforma, caeremos
                    if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                        posturaNueva = SPRITE_SALTANDO

                #Chocar lateralmente con las plataformas
                plataformas = pygame.sprite.groupcollide(grupoPlataformas, pygame.sprite.Group(self), False, False)

                for plataforma in plataformas:
                    if plataforma.rect.height > 15:
                        if plataforma != None:
                            if self.movimiento == IZQUIERDA:
                                if self.rect.left <= plataforma.rect.left + plataforma.rect.width and self.rect.left > plataforma.rect.left and self.posicion[1] -1 > plataforma.posicion[1]:
                                    velocidadx = 0
                                    if self.numPostura != SPRITE_SALTANDO:
                                        posturaNueva = QUIETO
                            else:
                                if self.rect.left  >= plataforma.rect.left - self.image.get_rect().width and self.rect.left < plataforma.rect.left and self.posicion[1] -1 > plataforma.posicion[1]:
                                    velocidadx = 0
                                    if self.numPostura != SPRITE_SALTANDO:
                                        posturaNueva = QUIETO


        

            # Si queremos saltar
            elif self.movimiento == ARRIBA:
                # La postura actual sera estar saltando
                posturaNueva = SPRITE_SALTANDO
                # Le imprimimos una velocidad en el eje y
                velocidady = -self.velocidadSalto
                #Cancelamos el ataque
                self.atacando = False
                self.retardoAccion = 0

            # Si no se ha pulsado ninguna tecla
            elif self.movimiento == QUIETO:
                # Si no estamos saltando, la postura actual será estar quieto
                if not self.numPostura == SPRITE_SALTANDO:
                    posturaNueva = SPRITE_QUIETO
                velocidadx = 0
            
            
            if self.movimiento != ATACAR: 
                #if self.retardoAccion <= 0:
                    self.atacando = False
                    self.retardoAccion = 0

            #Para atacar en otras posiciones
            if self.atacando:
                if self.retardoAccion <= 0:
                    posturaNueva = SPRITE_ATACANDO
                    self.retardoAccion = DURACION_ATACAR*3.5
                else:
                    posturaNueva = SPRITE_ATACANDO 

            #Para salir del modo ataque si estamos haciendo cualquier cosa
            if self.retardoAccion > 0:
                self.retardoAccion -= 1
                #print(self.retardoAccion)
            else:
                self.atacando = False

            # Además, si estamos en el aire
            if self.numPostura == SPRITE_SALTANDO or self.numPostura == SPRITE_ATACANDO_EN_SALTO:

                #Para atacar en otras posiciones
                if self.atacando:
                    if self.retardoAccion <= 0:
                        #print(self.retardoAccion)
                        posturaNueva = SPRITE_ATACANDO_EN_SALTO
                        self.retardoAccion = DURACION_ATACAR*2.5
                    else:
                        posturaNueva = SPRITE_ATACANDO_EN_SALTO
                elif self.numPostura == SPRITE_ATACANDO_EN_SALTO:
                    posturaNueva = SPRITE_SALTANDO

                #Para salir del modo ataque si estamos haciendo cualquier cosa
                if self.retardoAccion > 0:
                    self.retardoAccion -= 1
                    #print(self.retardoAccion)
                else:
                    self.atacando = False

                # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
                #  Para ello, miramos si hay colision con alguna plataforma del grupo
                plataformas = pygame.sprite.groupcollide(grupoPlataformas, pygame.sprite.Group(self), False, False)
                #  Ademas, esa colision solo nos interesa cuando estamos cayendo
                #  y solo es efectiva cuando caemos encima, no de lado, es decir,
                #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
                for plataforma in plataformas:
                    if (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                        plataforma.rect.height
                        # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                        #  para poder detectar cuando se cae de ella
                        self.establecerPosicion((self.posicion[0], plataforma.posicion[1]))
                        # Lo ponemos como quieto
                        posturaNueva = SPRITE_QUIETO
                        # Y estará quieto en el eje y
                        velocidady = 0
                        break
                    else:
                        velocidady += GRAVEDAD * tiempo
                
                # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
                if plataformas == {}:
                    velocidady += GRAVEDAD * tiempo

            if posturaNueva != SPRITE_ATACANDO_EN_SALTO:
                if self.atacando:
                    velocidadx = 0


        # Asignamos la postura auxiliar
        self.numPostura = posturaNueva

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        #self.rect.left += Solucionar cosas
        #self.rect.bottom -= self.image.get_rect().height
        
        return



# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'Enano.png','coordEnano.txt', [4, 11, 1, 7, 3, 7], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,VIDA_JUGADOR,DANO_JUGADOR,INVULNERABLE_JUGADOR,DURACION_MUERTE_JUGADOR);

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, atacar):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[atacar]:
            self.atacando = True
            Personaje.mover(self,ATACAR)
        else:
            Personaje.mover(self,QUIETO)
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

    def restarVida(self,enemigo):
        if self.atacando:
            #Hacemos dano al enemigo
            if enemigo.currentIFrames <= 0:
                enemigo.vida -= self.dano
                print(enemigo.vida)
                if enemigo.vida <= 0:
                    enemigo.numPostura = SPRITE_MUERTE
                enemigo.currentIFrames = enemigo.iFrames
        else:
            #Si no nos acaban de pegar restamos vida
            if self.currentIFrames <= 0:
                self.vida = self.vida - enemigo.dano
                print(self.vida)
                if self.vida <= 0:
                    self.numPostura = SPRITE_MUERTE
                self.currentIFrames = self.iFrames



# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador1, jugador2):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

# -------------------------------------------------
# Clase Sniper

class Sniper(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6, 0, 0, 11], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER,VIDA_SNIPER,DANO_SNIPER,INVULNERABLE_SNIPER,DURACION_MUERTE_SNIPER);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            jugadorMasCercano = jugador1

            # Y nos movemos andando hacia el
            if jugadorMasCercano.posicion[0]<self.posicion[0]:
                Personaje.mover(self,IZQUIERDA)
            else:
                Personaje.mover(self,DERECHA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)




class Fase3Enemigo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Fase3Enemigo.png','coordFase3Enemigo.txt', [1, 6, 2, 3, 2, 3], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER,VIDA_SNIPER,DANO_SNIPER,INVULNERABLE_SNIPER,DURACION_MUERTE_SNIPER);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            jugadorMasCercano = jugador1

            # Y nos movemos andando hacia el
            if jugadorMasCercano.posicion[0]<self.posicion[0]:
                Personaje.mover(self,IZQUIERDA)
            else:
                Personaje.mover(self,DERECHA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)



