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
DURACION_MUERTE_ENEMIGO = 55
DURACION_MUERTE_JUGADOR = 35
DURACION_ATACAR = 10

#Dano personajes
MAX_VIDA_JUGADOR = 40
VIDA_JUGADOR = MAX_VIDA_JUGADOR
VIDA_ENEMIGO = 100

#Dano personajes
DANO_JUGADOR = 20
DANO_ENEMIGO = 1

#Frames de invencibilidad despues de ser atacados
INVULNERABLE_JUGADOR = 20
INVULNERABLE_ENEMIGO = 10

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

VELOCIDAD_ENEMIGO = 0.15 # Pixeles por milisegundo
VELOCIDAD_SALTO_ENEMIGO = 0.28 # Pixeles por milisegundo
RETARDO_ANIMACION_ENEMIGO = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura

VELOCIDAD_FASE5BOSSLOBO = 0.07 # Pixeles por milisegundo
VELOCIDAD_SALTO_FASE5BOSSLOBO = 0.4 # Pixeles por milisegundo
RETARDO_ANIMACION_FASE5BOSSLOBO = 10 # updates que durará cada imagen del personaje

VELOCIDAD_FASE5BOSSREINA = 0.18 # Pixeles por milisegundo
VELOCIDAD_SALTO_FASE5BOSSREINA = 0.28 # Pixeles por milisegundo
RETARDO_ANIMACION_FASE5BOSSREINA = 5 # updates que durará cada imagen del personaje

# El Sniper camina un poco más lento que el jugador, y salta menos

GRAVEDAD = 0.0003 # Píxeles / ms2

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
# -------------------------------------------------
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
# Clase Obstaculo
# -------------------------------------------------:
class Objeto(MiSprite):
    def __init__(self,image):
        MiSprite.__init__(self)
        # Se carga la hoja
        self.image = image
        self.rect = pygame.Rect(100,100,10,10)

    def dibujar(self,pantalla):
        pantalla.blit(self.image,self.rect)

class FireBall(Objeto):
    def __init__(self,aceleracion):
        Objeto.__init__(self,None)
        self.movimiento = ATACAR
        self.image1 = GestorRecursos.CargarImagen('fireball.png',-1)
        self.image1 = self.image1.convert_alpha()
        self.image = self.image1
        self.image2 = GestorRecursos.CargarImagen('fireballAbajo.png',-1)
        self.image2 = self.image2.convert_alpha()
        self.bajar = False
        self.subir = True
        self.aceleracion = -aceleracion
        self.currentIFrames = 100
        self.dano = 2
        self.visible = True

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = 0
        if self.posicion[1] >= ALTO_PANTALLA:
            self.image = self.image1
            self.bajar = False
            self.subir = True
        elif self.posicion[1]<= 100:
            self.bajar = True
            self.subir = False
            self.image = self.image2
        if self.subir == True :
            incrementoy = self.aceleracion
        if self.bajar == True :
            incrementoy = -self.aceleracion
        self.incrementarPosicion((incrementox, incrementoy))
        
    def dibujar(self,pantalla):
        pantalla.blit(self.image,self.rect)

class Ice(Objeto):
    def __init__(self,aceleracion):
        Objeto.__init__(self,None)
        self.movimiento = ATACAR
        self.image1 = GestorRecursos.CargarImagen('ObsGigantes222.png',-1)
        self.image1 = self.image1.convert_alpha()
        self.image = self.image1
        self.dano = 6
        self.currentIFrames = 100
        self.retardoAnimacion = 10
        self.bajar = True
        self.suelo = False
        self.aceleracion = -aceleracion
        self.currentImage = 0
        self.visible = True

    def update(self, tiempo):
        self.rect = self.image.get_rect()
        incrementox = self.velocidad[0]*tiempo
        incrementoy = 0
        if self.posicion[1] < 550:
            self.bajar = True
            self.subir = False
        elif self.posicion[1] > 550:
            self.bajar= False
            self.subir = False
            self.establecerPosicion((self.posicion[0], self.posicion[1]-530))
        if self.subir == True :
            incrementoy = self.aceleracion
        if self.bajar == True :
            incrementoy = -self.aceleracion
        self.incrementarPosicion((incrementox, incrementoy))
        
    def dibujar(self,pantalla):
        if self.visible:    
            pantalla.blit(self.image,self.rect)

    def sacarVida(self,enemigo):
        # No ataca a los enemigos
        # Modificado, en vez de dañarlo, sanara al enemigo
        enemigo.vida = enemigo.vida + self.dano

class Veneno(Objeto):
    def __init__(self,aceleracion):
        Objeto.__init__(self,None)
        self.movimiento = ATACAR
        self.dano = 6
        self.currentIFrames = 100
        self.retardoAnimacion = 1
        self.currentImage = 0
        self.images = []
        self.images.append(pygame.image.load('imagenes/smoke_Green1.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green2.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green3.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green4.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green5.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green6.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green7.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green8.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green9.png'))
        self.images.append(pygame.image.load('imagenes/smoke_Green10.png'))

        #image = pygame.image.load(file)
        self.image = self.images[0]
        self.visible = True
    
    def update(self, tiempo):
        self.retardoAnimacion -= 1
        if self.retardoAnimacion < 0:
            self.retardoAnimacion = 10

        if self.visible:
            if self.retardoAnimacion <= 0:
                self.currentImage += 1

            if self.currentImage >= len(self.images):
                self.currentImage = 0
            self.image = self.images[self.currentImage]

    def dibujar(self,pantalla):     
        if self.visible:
            pantalla.blit(self.image,self.rect)

    def sacarVida(self,enemigo):
        return

class Fuego(Objeto):
    def __init__(self):
        Objeto.__init__(self,None)
        self.movimiento = ATACAR
        self.dano = 10
        self.currentIFrames = 100
        self.retardoAnimacion = 10
        self.currentImage = 0
        self.images = []
        self.images.append(pygame.image.load('imagenes/flame_a_0001.png'))
        self.images.append(pygame.image.load('imagenes/flame_a_0002.png'))
        self.images.append(pygame.image.load('imagenes/flame_a_0003.png'))
        self.images.append(pygame.image.load('imagenes/flame_a_0004.png'))
        self.images.append(pygame.image.load('imagenes/flame_a_0005.png'))
        self.images.append(pygame.image.load('imagenes/flame_a_0006.png'))
        #image = pygame.image.load(file)
        self.image = self.images[0]
        self.visible = False
    
    def update(self, tiempo):
        self.retardoAnimacion -= 1
        if self.retardoAnimacion < 0:
            self.retardoAnimacion = 10

        if self.visible:
            if self.retardoAnimacion <= 0:
                self.currentImage += 1

            if self.currentImage >= len(self.images):
                self.currentImage = 0
            self.image = self.images[self.currentImage]

    def dibujar(self,pantalla):     
        if self.visible:
            pantalla.blit(self.image,self.rect)

    def sacarVida(self,enemigo):
        enemigo.vida = enemigo.vida-self.dano
        if enemigo.vida <=0:
            enemigo.numPostura = SPRITE_MUERTE

class BolasPinchos(Objeto):
    def __init__(self,aceleracion,limit):
        Objeto.__init__(self,None)
        self.movimiento = ATACAR
        self.dano = 20
        self.currentIFrames = 100
        self.scalex = 60
        self.scaley = 60
        self.retardoAnimacion = 10
        self.images = []
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('bolaPinchosItem/bola1.png',-1),(self.scalex,self.scaley)))
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('bolaPinchosItem/bola2.png',-1),(self.scalex,self.scaley)))
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('bolaPinchosItem/bola3.png',-1),(self.scalex,self.scaley)))
        self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('bolaPinchosItem/bola4.png',-1),(self.scalex,self.scaley)))
        self.image = self.images[0]
        self.bajar = False
        self.suelo = False
        self.limit = limit
        self.aceleracion = aceleracion
        self.currentImage = 0
        self.visible1 = True
        self.visible = False

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = 0

        self.retardoAnimacion -= 1
        if self.retardoAnimacion < 0:
            self.retardoAnimacion = 10

        if self.visible:
            self.bajar = True

        if self.posicion[1] >= self.limit:
            self.bajar = False
            self.suelo = True

        if self.bajar == True:
            incrementoy = self.aceleracion
            if self.retardoAnimacion <= 0:
                self.currentImage += 1

            if self.currentImage >= len(self.images):
                self.currentImage = 0
            self.image = self.images[self.currentImage]
        
        if self.suelo:
            self.image = self.images[1]

        self.incrementarPosicion((incrementox, incrementoy))

    def dibujar(self,pantalla):     
        if self.visible1:
            pantalla.blit(self.image,self.rect)

    def sacarVida(self,enemigo):
        enemigo.vida = enemigo.vida-self.dano
        if enemigo.vida <=0:
            enemigo.numPostura = SPRITE_MUERTE




class Palanca(Objeto):
    def __init__(self,action):
        Objeto.__init__(self,None)
        self.image1 = GestorRecursos.CargarImagen('palanca.png',-1)
        self.image1 = self.image1.convert_alpha()
        self.image = self.image1
        #Objeto.__init__(self,self.image1)
        self.image2 = GestorRecursos.CargarImagen('palanca2.png',-1)
        self.image2 = self.image2.convert_alpha()
        self.activar = False
        self.activeObstacules = []
        if action:
            self.obsPos = [(340,390), (380,390), (420,390), (460,390), (500,390),(540,390)]
            for i in range(6):
                val = Fuego()
                val.establecerPosicion((self.obsPos[i][0],self.obsPos[i][1]))
                self.activeObstacules.append(val)
        else:
            self.obsPos = [(190,140), (225,140), (260,140), (207,101), (243,101),(225,70)]
            self.limit = [429,429,429,387,387,355]
            for i in range(6):
                val = BolasPinchos(3,self.limit[i])
                val.establecerPosicion((self.obsPos[i][0],self.obsPos[i][1]))
                self.activeObstacules.append(val)

    def update(self,tiempo):
        if self.activar:
            for x in self.activeObstacules:
                x.visible = True
            self.image = self.image2
        for x in self.activeObstacules:
            x.update(tiempo)

    def dibujar(self,pantalla):
        pantalla.blit(self.image,self.rect)
        for x in self.activeObstacules:
            x.dibujar(pantalla)

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;
        for x in self.activeObstacules:
            x.establecerPosicionPantalla(scrollDecorado)


# -------------------------------------------------
# Clases Personaje
# -------------------------------------------------
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte,isBoss,scalex,scaley):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        #Si es un boss es mas grande
        self.isBoss = isBoss
        self.scalex = scalex
        self.scaley = scaley

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
            self.movimiento= ARRIBA
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
            if self.isBoss:
                self.image = pygame.transform.scale(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]),(self.scalex,self.scaley))
            else:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                if self.isBoss:
                    self.image = pygame.transform.scale(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]),(self.scalex,self.scaley))
                else:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                if self.isBoss:
                   self.image = pygame.transform.scale( pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0),(self.scalex,self.scaley)) 
                else:
                    self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        #Inicializamos la postura nueva
        posturaNueva = self.numPostura

        if posturaNueva == SPRITE_MUERTE:
            '''self.rect.bottom = self.posicion[1]'''
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
        
        return


    # Retorno de pantalla cuando muere
    def dead(self):
        pygame.display.update()




# -------------------------------------------------
# Clase Jugador
# -------------------------------------------------
class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'Enano.png','coordEnano.txt', [4, 11, 1, 7, 3, 7], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,VIDA_JUGADOR,DANO_JUGADOR,INVULNERABLE_JUGADOR,DURACION_MUERTE_JUGADOR,False,None,None);

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, atacar):

        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

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

        else:
            self.vida=0
            if self.vida <= 0:
                self.numPostura = SPRITE_MUERTE
                self.dead()
            self.currentIFrames = self.iFrames

    def restarVida(self,enemigo):
        if self.atacando:
            #Hacemos dano al enemigo
            if enemigo.currentIFrames <= 0:
                enemigo.vida = enemigo.vida - self.dano
                #print("enemigo vida %d" , enemigo.vida)
                if enemigo.vida <= 0:
                    enemigo.retardoAccion -= 1
                    enemigo.numPostura = SPRITE_MUERTE
                enemigo.currentIFrames = enemigo.iFrames

        else:
            if enemigo.movimiento == ATACAR:
                #Si no nos acaban de pegar restamos vida
                if self.currentIFrames <= 0:
                    self.vida = self.vida - enemigo.dano
                    #print(self.vida)
                    if self.vida <= 0:
                        self.numPostura = SPRITE_MUERTE
                        self.dead()
                    self.currentIFrames = self.iFrames



# -------------------------------------------------
# Clase NoJugador
# -------------------------------------------------
class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte,isBoss,scalex,scaley):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, vida, dano, iFrames, duracionMuerte,isBoss,scalex,scaley)

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    # Acciones por defecto teniendo solo IZQUIERDA, DERECHA, ARRIBA, ATACAR
    def mover_cpu(self, jugador1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)

        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            # Y nos movemos andando hacia el
            if ((jugador1.posicion[1] < self.posicion[1]) and (jugador1.posicion[0]<self.posicion[0]) and (abs(jugador1.posicion[0]-self.posicion[0])<150)):
                Personaje.mover(self, IZQUIERDA)
                Personaje.mover(self, ARRIBA)
                self.atacando = False
            elif (jugador1.posicion[0]<self.posicion[0]+40):
                Personaje.mover(self, IZQUIERDA)
                self.atacando = False
            if ((jugador1.posicion[1] < self.posicion[1]) and (jugador1.posicion[0]>self.posicion[0]) and (abs(jugador1.posicion[0]-self.posicion[0])<150)):
                Personaje.mover(self, DERECHA)
                Personaje.mover(self, ARRIBA)
                self.atacando = False                
            elif (jugador1.posicion[0]>self.posicion[0]-40):
                Personaje.mover(self, DERECHA)
                self.atacando = False  


        
            # Cuando este cerca atacara
            if abs(self.posicion[0]-jugador1.posicion[0])<=40:
                self.atacando = True
                Personaje.mover(self,ATACAR)
            else:
                self.atacando = False
                if (jugador1.posicion[1] < self.posicion[1]):
                    Personaje.mover(self, ARRIBA)
                elif (jugador1.posicion[0]>self.posicion[0]):
                    Personaje.mover(self, DERECHA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)
            
            

# -------------------------------------------------
# Clase Sniper
# -------------------------------------------------
class Sniper(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6, 0, 0, 11], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO,DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Nos movemos andando hacia el
            if jugador1.posicion[0]<self.posicion[0]:
                Personaje.mover(self,IZQUIERDA)
                Personaje.mover(self, ARRIBA)
            else:
                Personaje.mover(self,DERECHA)
                Personaje.mover(self, ARRIBA)

            if jugador1.movimiento==ARRIBA:
                Personaje.mover(self, ARRIBA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)


# -------------------------------------------------
# Clase Fase3Enemigo
# -------------------------------------------------
class Fase3Enemigo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Fase3Enemigo.png','coordFase3Enemigo.txt', [1, 6, 2, 4, 1, 3], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO,DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):
       NoJugador.mover_cpu(self,jugador)


# -------------------------------------------------
# Clase Fase3Boss
# -------------------------------------------------
class Fase3Boss(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Fase3Boss.png','coordFase3Boss.txt', [1, 7, 4, 11, 1, 3], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO, DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        global VELOCIDAD_ENEMIGO 
        VELOCIDAD_ENEMIGO = VELOCIDAD_ENEMIGO + 0.1
        global VIDA_ENEMIGO 
        VIDA_ENEMIGO = VIDA_ENEMIGO + 20
        
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            # Y nos movemos andando hacia el
            if (jugador1.posicion[0]<self.posicion[0]+40):
                Personaje.mover(self, IZQUIERDA)
                self.atacando = False               
            elif (jugador1.posicion[0]>self.posicion[0]-40):
                Personaje.mover(self, DERECHA)
                self.atacando = False  

        
            # Cuando este cerca atacara
            if abs(self.posicion[0]-jugador1.posicion[0])<=40:
                self.atacando = True
                Personaje.mover(self,ATACAR)
            else:
                self.atacando = False
                if (jugador1.posicion[1] < self.posicion[1]):
                    if (jugador1.posicion[0]>self.posicion[0]):
                        Personaje.mover(self, DERECHA)
                    else: Personaje.mover(self, IZQUIERDA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)

        VELOCIDAD_ENEMIGO = VELOCIDAD_ENEMIGO - 0.10
        VIDA_ENEMIGO = VIDA_ENEMIGO - 20



# -------------------------------------------------
# Clase Fase1Enemigo
# -------------------------------------------------
class Fase1Enemigo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase1Enemigo1.png','coordFase1Enemigo1.txt', [2, 6, 4, 4, 1, 2], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO,DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        NoJugador.mover_cpu(self,jugador1)

        
# -------------------------------------------------
# Clase Fase1Boss
# -------------------------------------------------
class Fase1Boss(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase1Boss.png','coordFase1Boss.txt', [1, 3, 6, 10, 1, 6], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, 5,1500,int(VIDA_JUGADOR/4),INVULNERABLE_ENEMIGO,80,False,None,None);
        self.mirando = IZQUIERDA
        self.parar = False
        self.derecha = False
        self.izquierda = True
        self.derecha1 = False
        self.izquierda1 = True
        self.cerca = False
        self.lejos = True
        self.atacando=False
        self.cerca2=False

    def mover_cpu(self, jugador1):
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
        
            if abs(self.posicion[0]-jugador1.posicion[0])<=120 and abs(self.posicion[0]-jugador1.posicion[0])>=90 :
                self.atacando= False
                self.cerca2 = True
                self.cerca = False
                self.lejos = False
        
            if (abs(self.posicion[0]-jugador1.posicion[0])<=90):
                self.atacando= False
                self.cerca = True
                self.cerca2 = False
                self.lejos = False
                self.teleport = True

            if abs(self.posicion[0]-jugador1.posicion[0])>=125:
                self.atacando = True
                self.cerca = False
                self.cerca2 = False
                self.lejos = True
                self.teleport= False

                
                
            if self.cerca2 == True and self.cerca==False:
               Personaje.mover(self,ARRIBA)

            
            elif self.cerca == True:
                if self.posicion[0]>=jugador1.posicion[0]:
                    self.establecerPosicion((250,550))
                    
                elif self.posicion[0]<=jugador1.posicion[0]:
                    self.establecerPosicion((750,550))
                    
            elif self.cerca==False and self.atacando:
                Personaje.mover(self,ATACAR)
            else:
                Personaje.mover(self,QUIETO)
            

# -------------------------------------------------
# Clase Fase5Enemigo
# -------------------------------------------------
class Fase5Enemigo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase5Enemigo.png','coordFase5Enemigo.txt', [3, 6, 2, 3, 2, 4], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO,DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        NoJugador.mover_cpu(self,jugador1)

# -------------------------------------------------
# Clase Fase2Enemigo
# -------------------------------------------------
class Fase2Enemigo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase2Enemigo1.png','coordFase2Enemigo1.txt', [1,3,3,2,2,1], VELOCIDAD_ENEMIGO, VELOCIDAD_SALTO_ENEMIGO, RETARDO_ANIMACION_ENEMIGO,VIDA_ENEMIGO,DANO_ENEMIGO,INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);
        #self.images.append(pygame.transform.scale(GestorRecursos.CargarImagen('cerveza_item/0.png',-1),(self.scalex,self.scaley)).convert_alpha())

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        NoJugador.mover_cpu(self,jugador1)

# -------------------------------------------------
# Clase Fase2Boss
# -------------------------------------------------
class Fase2Boss(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase2Boss.gif','coordFase2Boss.txt', [1,6,3,3,1,1], 0.15, VELOCIDAD_SALTO_ENEMIGO, 5,2200,int(VIDA_JUGADOR/4),INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,True,80,112);
        self.mirando = IZQUIERDA
        self.Pelear = True
        self.sufrir = False
        self.vidaIni = self.vida
        self.limite1 = 370
        self.limite2 = 580
        self.limite3 = 200
        self.atacando = False
        self.derecha = False
        self.izquierda = True
        self.parar = False

    def mover_cpu(self, jugador1):
        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            if self.parar == False:
                if jugador1.posicion[1] <= 200:
                    self.Pelear = False
                if self.posicion[0]<=0:
                    self.parar = True

                if abs(self.posicion[0]-jugador1.posicion[0])<=40 and abs(self.posicion[1]-jugador1.posicion[1])<=90:
                    self.atacando = True
                else:
                    self.atacando = False

                if self.sufrir == False and self.Pelear == False and abs(self.posicion[0]-jugador1.posicion[0])>=250:
                    self.Pelear = True

                if self.vida <= self.vidaIni-200:
                    self.sufrir = True
                    self.Pelear = False
                    self.derecha = False
                    self.izquierda = False

                if self.Pelear:
                    if jugador1.posicion[0]<=self.posicion[0]:
                        Personaje.mover(self,IZQUIERDA)
                    elif jugador1.posicion[0]>=self.posicion[0]:
                        Personaje.mover(self,DERECHA)
                else:
                    self.atacando = False
                    if self.posicion[0]>=self.limite2:
                        self.izquierda = True
                        self.derecha = False
                    elif self.posicion[0]<=self.limite1:
                        self.derecha = True
                        self.izquierda = False

                if self.sufrir == False and self.Pelear == False and self.derecha :
                    Personaje.mover(self,DERECHA)
                elif self.sufrir == False and self.Pelear == False and self.izquierda:
                    Personaje.mover(self,IZQUIERDA)

                if self.Pelear and self.atacando:
                    Personaje.mover(self,ATACAR)

                if self.sufrir:
                    if self.posicion[0]>self.limite3:
                        Personaje.mover(jugador1,QUIETO)
                        Personaje.mover(self,IZQUIERDA)
                    else:
                        self.parar = True
            else:
                if abs(self.posicion[0]-jugador1.posicion[0])<=40 and abs(self.posicion[1]-jugador1.posicion[1])<=90:
                    Personaje.mover(self,ATACAR)
                else:
                    self.mirando = DERECHA
                    Personaje.mover(self,QUIETO)


# -------------------------------------------------
# Clase Fase5BossLobo
# -------------------------------------------------
class Fase5BossLobo(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase5BossLobo.png','coordFase5BossLobo.txt', [6,6,1,2,2,7], VELOCIDAD_FASE5BOSSLOBO, VELOCIDAD_SALTO_FASE5BOSSLOBO, RETARDO_ANIMACION_FASE5BOSSLOBO,1500,int(VIDA_JUGADOR/3),INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);
        self.visto = False

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)

        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA or self.visto:

            #Una vez que veamos al boss nos persigue siempre, da igual si sale de nuestra pantalla
            self.visto = True

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            # Y nos movemos andando hacia el
            if (jugador1.posicion[0] < self.posicion[0]):
                Personaje.mover(self, IZQUIERDA)
                #Personaje.mover(self, ARRIBA)
                self.atacando = False
            elif (jugador1.posicion[0]>self.posicion[0]):
                Personaje.mover(self, DERECHA)
                self.atacando = False              


            # Cuando este cerca atacara
            collide = pygame.sprite.groupcollide(pygame.sprite.Group(jugador1),pygame.sprite.Group(self), False, False)
            #collide contine los sprites del primer grupo con los que ha colisionado
            if collide!={}:
                self.atacando = True
                Personaje.mover(self,ATACAR)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)

# -------------------------------------------------
# Clase Fase5BossReina
# -------------------------------------------------
class Fase5BossReina(NoJugador):

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'fase5BossReina.png','coordFase5BossReina.txt', [1,1,1,2,2,2], VELOCIDAD_FASE5BOSSREINA, VELOCIDAD_SALTO_FASE5BOSSREINA, RETARDO_ANIMACION_FASE5BOSSREINA,1500,int(VIDA_JUGADOR/3),INVULNERABLE_ENEMIGO,DURACION_MUERTE_ENEMIGO,False,None,None);
        self.visto = False

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)

        #Restamos iFrames
        if self.currentIFrames > 0:
            self.currentIFrames -= 1

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA or self.visto:

            #Una vez que veamos al boss nos persigue siempre, da igual si sale de nuestra pantalla
            self.visto = True

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano

            # Y nos movemos andando hacia el
            if (jugador1.posicion[0] < self.posicion[0]):
                Personaje.mover(self, IZQUIERDA)
                #Personaje.mover(self, ARRIBA)
                self.atacando = False
            elif (jugador1.posicion[0]>self.posicion[0]):
                Personaje.mover(self, DERECHA)
                self.atacando = False              


            # Cuando este cerca atacara
            collide = pygame.sprite.groupcollide(pygame.sprite.Group(jugador1),pygame.sprite.Group(self), False, False)
            #collide contine los sprites del primer grupo con los que ha colisionado
            if collide!={}:
                self.atacando = True
                Personaje.mover(self,ATACAR)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)
