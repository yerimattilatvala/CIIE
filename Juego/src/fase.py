# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
from animaciones import *
from hud import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 350
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self, director, img_decorado,scale_decorado,pos_jugador,num_enemigos,tipo_enemigo,pos_enemigos,plataformas):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        '''
            img_decorado = 'image.png'
            scale_decorado = (width,heigh)
            pos_jugador = (x,y)
            num_enemigos = 1,2,3....>0
            tipo_enemigos = 'sniper'...'bestia'
            pos_enemigos = [(x,y),(x,y),....]
            plataformas = [Plataforma1,Plataforma2,.....]
        '''
        Escena.__init__(self, director)
        # Creamos el decorado y el fondo
        self.fondo = Cielo()
        self.decorado = Decorado(img_decorado,scale_decorado)
        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1 )
        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion(pos_jugador)
        # Ponemos el hud
        self.hud = Hud()
        self.grupoHud = pygame.sprite.Group(self.hud)

        self.grupoPlataformas = pygame.sprite.Group()
        for x in plataformas:
            self.grupoPlataformas.add(Plataforma(pygame.Rect(x)))

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)
        enemigos = self.crearEnemigos(num_enemigos,tipo_enemigo)
        if not (enemigos is None):
            self.grupoEnemigos = pygame.sprite.Group()
            for i, val in enumerate(enemigos):
                val.establecerPosicion(pos_enemigos[i])
                self.grupoEnemigos.add(val)
                self.grupoSpritesDinamicos.add(val)
            # Creamos otro grupo con todos los Sprites
            self.grupoSprites = pygame.sprite.Group( self.grupoEnemigos, self.grupoPlataformas ) 
        else:
            # Creamos otro grupo con todos los Sprites
            self.grupoSprites = pygame.sprite.Group( self.grupoJugadores, self.grupoPlataformas ) 

        # Ponemos el hud
        #self.hud = Hud()
        #self.grupoHud = pygame.sprite.Group(self.hud)

        '''# Creamos el decorado y el fondo
        self.decorado = Decorado()
        self.fondo = Cielo()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((200, 551))

        # Ponemos el hud
        self.hud = Hud()
        self.grupoHud = pygame.sprite.Group(self.hud)

        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 5000, 15))
        # La plataforma del techo del edificio
        #plataformaCasa = Plataforma(pygame.Rect(890, 417, 160, 10))
        plataformaCasa1 = Plataforma(pygame.Rect(0, 417, 300, 10))
        plataformaCasa2 = Plataforma(pygame.Rect(3010, 417, 250, 10))
        plataformaCasa3 = Plataforma(pygame.Rect(3400, 417, 200, 10))
        
        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group( plataformaSuelo, plataformaCasa1,plataformaCasa2,plataformaCasa3 )

        # Y los enemigos que tendran en este decorado
        enemigo1 = Sniper()
        enemigo1.establecerPosicion((1000, 551))
        enemigo2 = Sniper()
        enemigo2.establecerPosicion((2500, 551))
        enemigo3 = Sniper()
        enemigo3.establecerPosicion((3100, 418))
        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group( enemigo1, enemigo2,enemigo3 )

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1, enemigo1, enemigo2,enemigo3 )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group( self.grupoJugadores, self.grupoEnemigos, self.grupoPlataformas )
        '''
        # Creamos las animaciones de fuego,
        #  las que estan detras del decorado, y delante

        self.animacionesDetras = []
        for i in range(9):
            # La animacion del fuego
            animacionFuego = AnimacionFuego()
            # Aumentamos un poco el tamaño de la animacion
            animacionFuego.scale((400,400))
            # La situamos en su posicion
            animacionFuego.posicionx = 120*i - 200
            animacionFuego.posiciony = 250
            # Iniciamos la animacion
            animacionFuego.play()
            animacionFuego.nextFrame(i)
            # y la anadimos a la lista de animaciones detras
            self.animacionesDetras.append(animacionFuego)

        '''
        self.animacionesDelante = []
        for i in range(11):
            # La animacion del fuego
            animacionFuego = AnimacionFuego()
            # Aumentamos un poco el tamaño de la animacion
            animacionFuego.scale((450,450))
            # La situamos en su posicion
            animacionFuego.posicionx = 120*i - 200
            animacionFuego.posiciony = 450
            # Iniciamos la animacion
            animacionFuego.play()
            animacionFuego.nextFrame(i)
            # y la anadimos a la lista de animaciones delante
            self.animacionesDelante.append(animacionFuego)
        '''

    # n = numeroEnemigos
    # type(obvio)
    #problema -> un caso para cada enemigo -> obliganos a modificar a clase
    def crearEnemigos(self,n,type):
        l = None
        if n>0:
            l = []
            for x in xrange(n):
                if type == 'sniper':
                    l.append(Sniper())
        return l
        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):
        # Si ambos jugadores se han ido por ambos lados de los dos bordes
       # if (jugadorIzq.rect.left<MINIMO_X_JUGADOR) and (jugadorDcha.rect.right>MAXIMO_X_JUGADOR):

            # Colocamos al jugador que esté a la izquierda a la izquierda de todo
        #    jugadorIzq.establecerPosicion((self.scrollx+MINIMO_X_JUGADOR, jugadorIzq.posicion[1]))
            # Colocamos al jugador que esté a la derecha a la derecha de todo
        #    jugadorDcha.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugadorDcha.rect.width, jugadorDcha.posicion[1]))
            
        #    return False; # No se ha actualizado el scroll

        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (jugador.rect.left<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la derecha no se pueda desplazar
            #  tantos pixeles a la derecha por estar muy cerca del borde derecho
            #elif ((MAXIMO_X_JUGADOR-jugador.rect.right)<desplazamiento):
                
                # En este caso, ponemos el jugador de la izquierda en el lado izquierdo
            #    jugador.establecerPosicion((jugadorIzq.posicion[0]+desplazamiento, jugadorIzq.posicion[1]))

             #   return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador de la derecha se encuentra más allá del borde derecho
        if (jugador.rect.right>MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la izquierda no se pueda desplazar
            #  tantos pixeles a la izquierda por estar muy cerca del borde izquierdo
            #elif ((jugador.rect.left-MINIMO_X_JUGADOR)<desplazamiento):

                # En este caso, ponemos el jugador de la derecha en el lado derecho
             #   jugadorDcha.establecerPosicion((jugadorDcha.posicion[0]-desplazamiento, jugadorDcha.posicion[1]))

              #  return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si ambos jugadores están entre los dos límites de la pantalla, no se hace nada
        return False;
        


    def actualizarScroll(self, jugador1):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
        #if (jugador1.posicion[0]<jugador2.posicion[0]):
        #    cambioScroll = self.actualizarScrollOrdenados(jugador1, jugador2)
        #else:
        cambioScroll = self.actualizarScrollOrdenados(jugador1)
        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))
            jugador1.establecerPosicionPantalla((self.scrollx, 0))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx)



    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
    #  Se actualiza la posicion del sol y el color del cielo
    def update(self, tiempo):

        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover_cpu(self.jugador1)
        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        collide = pygame.sprite.groupcollide(self.grupoEnemigos, self.grupoJugadores, False, False)
        #collide contine los sprites del primer grupo con los que ha colisionado
        if collide!={}:
            for sprite in collide:
                self.jugador1.restarVida(sprite)

        #Actualizamos el Hud
        self.grupoHud.update(self.jugador1)

        #Si estamos muerto nos vamos a la pantalla principal
        if self.jugador1.muerto:
            self.director.salirEscena()

        #Miramos si hay que matar enemigos
        self.grupoEnemigos = [enemy for enemy in self.grupoEnemigos if enemy.muerto == False]
        #Como esta ahora mismo para que se deje de dibujar tenemos que sacarlo de aquí tambien
        self.grupoSprites = pygame.sprite.Group(self.grupoEnemigos, self.grupoPlataformas )

            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            #self.director.salirEscena()

        # Actualizamos el scroll
        self.actualizarScroll(self.jugador1)
  
        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo
        self.fondo.update(tiempo)

        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Despues, las animaciones que haya detras
        for animacion in self.animacionesDetras:
            animacion.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)

        self.jugador1.draw(pantalla)
        # El hud
        #self.grupoHud.draw(pantalla)
        for sprite in self.grupoHud:
            sprite.draw(pantalla)
        # Y por ultimo, dibujamos las animaciones por encima del decorado
        '''
        for animacion in self.animacionesDelante:
            animacion.dibujar(pantalla)
        '''

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_w, K_s, K_a, K_d, K_SPACE)

# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))
# -------------------------------------------------
# Clase Cielo

class Cielo:
    def __init__(self):
        self.sol = GestorRecursos.CargarImagen('sol.png', -1)
        self.sol = pygame.transform.scale(self.sol, (300, 200))

        self.rect = self.sol.get_rect()
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        pantalla.blit(self.sol, self.rect)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self,image,scale_value):
        self.imagen = GestorRecursos.CargarImagen(image, -1)
        self.imagen = pygame.transform.scale(self.imagen, (scale_value[0], scale_value[1]))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
