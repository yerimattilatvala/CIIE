# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
from animaciones import *
from hud import *
from pociones import *

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
    def __init__(self, director, jugador, numeroFase, max_distance, img_decorado,scale_decorado,sky_img,sky_scale,pos_jugador,enemigos,pos_enemigos,plataformas,animaciones,pos_animaciones,pociones,pos_pociones,obstaculos,pos_obstaculos ,velo_obsta,objetos,pos_objetos,object_action, isBoss):

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos el decorado y el fondo
        self.fondo = Cielo(sky_img, sky_scale)
        self.decorado = Decorado(img_decorado, scale_decorado)
        self.scaleDecorado =  convertPosValues(scale_decorado,'pos')

        # Que parte del decorado estamos visualizando, scroll horizontal
        self.scrollx = 0
       
       # Datos fase
        self.numeroFase = numeroFase
        self.max_distance = max_distance
        self.isBoss = isBoss
        print(self.isBoss)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        self.jugador1.vida = jugador.vida
        self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion(convertPosValues(pos_jugador,'pos'))

        # Ponemos el hud
        self.hud = Hud()
        self.grupoHud = pygame.sprite.Group(self.hud)
        self.grupoPlataformas = pygame.sprite.Group()

        #Las plataformas
        for x in convertPosValues(plataformas,'plat'):
            self.grupoPlataformas.add(Plataforma(pygame.Rect(x)))

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)


        # Enemigos del decorado
        enemigos = convertEnemies(enemigos)
        enemigosPos = convertPosValues(pos_enemigos,'enemy')


        if not (enemigos is None):
            self.grupoEnemigos = pygame.sprite.Group()
            for i, val in enumerate(enemigos):
                val.establecerPosicion(enemigosPos[i])
                self.grupoEnemigos.add(val)
                self.grupoSpritesDinamicos.add(val)
            # Creamos otro grupo con todos los Sprites
            self.grupoSprites = pygame.sprite.Group( self.grupoEnemigos, self.grupoPlataformas ) 
        else:
            # Creamos otro grupo con todos los Sprites
            self.grupoSprites = pygame.sprite.Group( self.grupoJugadores, self.grupoPlataformas ) 


        #Animaciones
        if animaciones is not None:
            print(animaciones)
            animations = convertAnimations(animaciones)
            animationsPos = convertPosValues(pos_animaciones,'enemy')
            if not (animations is None):
                self.animaciones = []
                for i, val in enumerate(animations):
                    val.posicionx = animationsPos[i][0]
                    val.posiciony = animationsPos[i][1]
                    val.play()
                    self.animaciones.append(val)
            else:
                self.animaciones = []
        else:
            self.animaciones = []

        #Obstaculos
        self.obstaculos = pygame.sprite.Group()
        if obstaculos is not None:
            aceleracion = convertPosValues(velo_obsta,'ace')
            obsPos = convertPosValues(pos_obstaculos,'enemy') 
            obstaculos = convertObst(obstaculos,aceleracion)
            if obstaculos is not None:
                for i, val in enumerate(obstaculos):
                    val.establecerPosicion((obsPos[i][0],obsPos[i][1]))
                    self.obstaculos.add(val)
        
        #Objetos
        self.objetos = pygame.sprite.Group()
        if objetos is not None:
            actions = convertPosValues(object_action,'ace')
            objetos = convertObjects(objetos,actions)
            objPos = convertPosValues(pos_objetos,'enemy')
            if objetos is not None:
                for i,val in enumerate(objetos):
                    val.establecerPosicion((objPos[i][0],objPos[i][1]))
                    self.objetos.add(val)

        #Pociones
        if pociones is not None:
            potions = convertPotions(pociones)
            potionPos = convertPosValues(pos_pociones,'enemy')
            if not (potions is None):
                self.grupoPociones = pygame.sprite.Group()  
                for i, val in enumerate(potions):
                    val.updatePos(potionPos[i][0],potionPos[i][1])
                    self.grupoPociones.add(val)
            else:
                self.grupoPociones = pygame.sprite.Group() 
        else:
            self.grupoPociones = pygame.sprite.Group() 
        ##########################################################
    
        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):

        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (jugador.rect.left<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, dejamos que el jugador avance hasta el borde
                if jugador.posicion[0] < 1:
                    jugador.establecerPosicion((1, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

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

               # En su lugar, dejamos al jugador avanzar hasta el final de la imagen
                if jugador.posicion[0] > self.scaleDecorado[0] -self.jugador1.image.get_rect().width:
                    jugador.establecerPosicion((self.scaleDecorado[0] -self.jugador1.image.get_rect().width, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si ambos jugadores están entre los dos límites de la pantalla, no se hace nada
        return False;
        


    def actualizarScroll(self, jugador1):
        cambioScroll = self.actualizarScrollOrdenados(jugador1)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))
            jugador1.establecerPosicionPantalla((self.scrollx, 0))
            for obs in iter(self.obstaculos):
                obs.establecerPosicionPantalla((self.scrollx, 0))
            for obj in iter(self.objetos):
                obj.establecerPosicionPantalla((self.scrollx, 0))
            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx)



    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
    #  Se actualiza el decorado, fondo y animaciones
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

        #Obstaculos Jugador
        collide1 = pygame.sprite.groupcollide(self.obstaculos, self.grupoJugadores, False, False)
        #collide contine los sprites del primer grupo con los que ha colisionado
        if collide1!={}:
            for sprite in collide1:
                if sprite.visible:
                    self.jugador1.restarVidaObstaculo(sprite)
        
        #Obstaculos Enemigos
        collide1 = pygame.sprite.groupcollide(self.obstaculos, self.grupoEnemigos, False, False)
        #collide contine los sprites del primer grupo con los que ha colisionado
        if collide1!={}:
            for sprite in collide1:
                if sprite.visible:
                    for x in iter(self.grupoEnemigos):
                        sprite.sacarVida(x)

        #Objetos
        collide1 = pygame.sprite.groupcollide(self.objetos, self.grupoJugadores, False, False)
        #collide contine los sprites del primer grupo con los que ha colisionado
        if collide1!={}:
            for sprite in collide1:
                if self.jugador1.movimiento == ATACAR:
                    sprite.activar = True
                    for x in sprite.activeObstacules:
                        self.obstaculos.add(x)

        #Pociones
        collidePociones = pygame.sprite.groupcollide(self.grupoPociones, self.grupoJugadores, False, False)
        #collide contine los sprites del primer grupo con los que ha colisionado
        if collidePociones!={}:
            for sprite in collidePociones:
                sprite.collect(self.jugador1)
                pygame.sprite.Group.remove(self.grupoPociones,sprite)
       

        #Actualizamos las pociones
        self.grupoPociones.update(self.scrollx)

        #Actualizamos el Hud
        self.grupoHud.update(self.jugador1)

        #Si estamos muerto nos vamos al pricipio del nivel
        if self.jugador1.muerto:
            self.jugador1.vida = 8
            if self.numeroFase == 1:
                fase = Fase(self.director,self.jugador1,1,4800,getValues(TEXT,'FASE1_FONDO='),getValues(TEXT,'FASE1_FONDO_SCALE='),getValues(TEXT,'FASE1_CIELO='),getValues(TEXT,'FASE1_CIELO_SCALE='),getValues(TEXT,'FASE1_POS_JUGADOR='),getValues(TEXT,'FASE1_ENEMIGOS='),getValues(TEXT,'FASE1_ENEMIGOS_POS='),getValues(TEXT,'FASE1_PLATAFORMAS='),None,None,getValues(TEXT,'FASE1_POCIONES='),getValues(TEXT,'FASE1_POS_POCIONES='),getValues(TEXT,'FASE1_OBSTACULOS='),getValues(TEXT,'FASE1_OBSTACULOS_POS='),getValues(TEXT,'FASE1_ACELERACION='),None,None,None,False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 2:
                fase = Fase(self.director,self.jugador1, 2, 5400, getValues(TEXT,'FASE2_FONDO='),getValues(TEXT,'FASE2_FONDO_SCALE='),getValues(TEXT,'FASE2_CIELO='),getValues(TEXT,'FASE2_CIELO_SCALE='),getValues(TEXT,'FASE2_POS_JUGADOR='),getValues(TEXT,'FASE2_ENEMIGOS='),getValues(TEXT,'FASE2_ENEMIGOS_POS='),getValues(TEXT,'FASE2_PLATAFORMAS='),None,None,getValues(TEXT,'FASE2_POCIONES='),getValues(TEXT,'FASE2_POS_POCIONES='),getValues(TEXT,'FASE2_OBSTACULOS='),getValues(TEXT,'FASE2_OBSTACULOS_POS='),getValues(TEXT,'FASE2_ACELERACION='),None,None,None, False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 3:
                fase = Fase(self.director,self.jugador1, 3, 4900, getValues(TEXT,'FASE3_FONDO='),getValues(TEXT,'FASE3_FONDO_SCALE='),None, None, getValues(TEXT,'FASE3_POS_JUGADOR='),getValues(TEXT,'FASE3_ENEMIGOS='),getValues(TEXT,'FASE3_ENEMIGOS_POS='),getValues(TEXT,'FASE3_PLATAFORMAS='),None,None,getValues(TEXT,'FASE3_POCIONES='), getValues(TEXT,'FASE3_POS_POCIONES='),getValues(TEXT,'FASE3_OBSTACULOS=') , getValues(TEXT,'FASE3_OBSTACULOS_POS='), getValues(TEXT,'FASE3_ACELERACION='),None,None,None, False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 5:
                fase = Fase(self.director,self.jugador1, 5, 4600, getValues(TEXT,'FASE5_FONDO='),getValues(TEXT,'FASE5_FONDO_SCALE='),getValues(TEXT,'FASE5_CIELO='),getValues(TEXT,'FASE5_CIELO_SCALE='),getValues(TEXT,'FASE5_POS_JUGADOR='),getValues(TEXT,'FASE5_ENEMIGOS='),getValues(TEXT,'FASE5_ENEMIGOS_POS='),getValues(TEXT,'FASE5_PLATAFORMAS='),getValues(TEXT,'FASE5_ANIMACIONES='),getValues(TEXT,'FASE5_POS_ANIMACIONES='),getValues(TEXT,'FASE5_POCIONES='),getValues(TEXT,'FASE5_POS_POCIONES='),None,None,None,None,None,None, False)
                self.director.cambiarEscena(fase)
            

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

        for obs in iter(self.obstaculos):
            obs.update(tiempo)

        for obj in iter(self.objetos):
            obj.update(tiempo)
        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)

        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoPlataformas.draw(pantalla)

        for enemigo in self.grupoEnemigos:
            enemigo.draw(pantalla)

        #Jugador
        self.jugador1.draw(pantalla)
        
        #Obstaculos
        for obs in iter(self.obstaculos):
            obs.dibujar(pantalla)

        #Objetos
        for obj in iter(self.objetos):
            obj.dibujar(pantalla)

        #Las pociones
        for sprite in self.grupoPociones:
            sprite.draw(pantalla,self.scrollx)

        # El hud
        #self.grupoHud.draw(pantalla)
        for sprite in self.grupoHud:
            sprite.draw(pantalla)     

        # Y por ultimo, dibujamos las animaciones por encima del decorado
        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla,self.scrollx)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_w, K_s, K_a, K_d, K_SPACE)

        
        #Cambiar a escena
        if (self.jugador1.posicion[0]>self.max_distance) and not (self.isBoss):
            if self.numeroFase == 1:
                fase = Fase(self.director,self.jugador1,1,1000,getValues(TEXT,'FASE1BOSS_FONDO='),getValues(TEXT,'FASE1BOSS_FONDO_SCALE='),getValues(TEXT,'FASE1BOSS_CIELO='),getValues(TEXT,'FASE1BOSS_CIELO_SCALE='),getValues(TEXT,'FASE1BOSS_POS_JUGADOR='),getValues(TEXT,'FASE1BOSS_ENEMIGOS='),getValues(TEXT,'FASE1BOSS_ENEMIGOS_POS='),getValues(TEXT,'FASE1BOSS_PLATAFORMAS='),None,None,None,None,None, None,None,None,None,None,True)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 2:
                fase = Fase(self.director,self.jugador1, 2, 5000, getValues(TEXT,'FASE2BOSS_FONDO='),getValues(TEXT,'FASE2BOSS_FONDO_SCALE='),getValues(TEXT,'FASE2BOSS_CIELO='),getValues(TEXT,'FASE2BOSS_CIELO_SCALE='),getValues(TEXT,'FASE2BOSS_POS_JUGADOR='),getValues(TEXT,'FASE2BOSS_ENEMIGOS='),getValues(TEXT,'FASE2BOSS_ENEMIGOS_POS='),getValues(TEXT,'FASE2BOSS_PLATAFORMAS='),None,None,None,None,None,None,None,getValues(TEXT,'FASE2BOSS_OBJETOS='),getValues(TEXT,'FASE2BOSS_OBJETOS_POS='),getValues(TEXT,'FASE2BOSS_OBJETOS_ACTION='), True)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 3:
                fase = Fase(self.director,self.jugador1, 3, 5000, getValues(TEXT,'FASE3BOSS_FONDO='),getValues(TEXT,'FASE3BOSS_FONDO_SCALE='),getValues(TEXT,'FASE3BOSS_CIELO='),getValues(TEXT,'FASE3BOSS_CIELO_SCALE='),getValues(TEXT,'FASE3BOSS_POS_JUGADOR='),getValues(TEXT,'FASE3BOSS_ENEMIGOS='),getValues(TEXT,'FASE3BOSS_ENEMIGOS_POS='),getValues(TEXT,'FASE3BOSS_PLATAFORMAS='),None,None,getValues(TEXT, 'FASE3_POCIONES_BOSS='), getValues(TEXT, 'FASE3_POS_POCIONES_BOSS='), getValues(TEXT,'FASE3_OBSTACULOS_BOSS='), getValues(TEXT,'FASE3_OBSTACULOS_POS_BOSS='),getValues(TEXT,'FASE3_ACELERACION_BOSS='),None,None,None, True)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 5:
                fase = Fase(self.director,self.jugador1, 5,1499,getValues(TEXT,'FASE5BOSS_FONDO='),getValues(TEXT,'FASE5BOSS_FONDO_SCALE='),getValues(TEXT,'FASE5BOSS_CIELO='),getValues(TEXT,'FASE5BOSS_CIELO_SCALE='),getValues(TEXT,'FASE5BOSS_POS_JUGADOR='),getValues(TEXT,'FASE5BOSS_ENEMIGOS='),getValues(TEXT,'FASE5BOSS_ENEMIGOS_POS='),getValues(TEXT,'FASE5BOSS_PLATAFORMAS='),None,None,None,None,None,None,None,None,None,None,True)
                self.director.cambiarEscena(fase)

        if len(self.grupoEnemigos) == 0 and self.isBoss:
            if self.numeroFase == 1:
                fase = Fase(self.director,self.jugador1, 2, 5400, getValues(TEXT,'FASE2_FONDO='),getValues(TEXT,'FASE2_FONDO_SCALE='),getValues(TEXT,'FASE2_CIELO='),getValues(TEXT,'FASE2_CIELO_SCALE='),getValues(TEXT,'FASE2_POS_JUGADOR='),getValues(TEXT,'FASE2_ENEMIGOS='),getValues(TEXT,'FASE2_ENEMIGOS_POS='),getValues(TEXT,'FASE2_PLATAFORMAS='),None,None,getValues(TEXT,'FASE2_POCIONES='),getValues(TEXT,'FASE2_POS_POCIONES='),getValues(TEXT,'FASE2_OBSTACULOS='),getValues(TEXT,'FASE2_OBSTACULOS_POS='),getValues(TEXT,'FASE2_ACELERACION='),None,None,None, False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 2:
                fase = Fase(self.director,self.jugador1, 3, 4900, getValues(TEXT,'FASE3_FONDO='),getValues(TEXT,'FASE3_FONDO_SCALE='),None, None, getValues(TEXT,'FASE3_POS_JUGADOR='),getValues(TEXT,'FASE3_ENEMIGOS='),getValues(TEXT,'FASE3_ENEMIGOS_POS='),getValues(TEXT,'FASE3_PLATAFORMAS='),None,None,getValues(TEXT,'FASE3_POCIONES='), getValues(TEXT,'FASE3_POS_POCIONES='),getValues(TEXT,'FASE3_OBSTACULOS=') , getValues(TEXT,'FASE3_OBSTACULOS_POS='), getValues(TEXT,'FASE3_ACELERACION='),None,None,None, False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 3:
                fase = Fase(self.director,self.jugador1, 5, 4600, getValues(TEXT,'FASE5_FONDO='),getValues(TEXT,'FASE5_FONDO_SCALE='),getValues(TEXT,'FASE5_CIELO='),getValues(TEXT,'FASE5_CIELO_SCALE='),getValues(TEXT,'FASE5_POS_JUGADOR='),getValues(TEXT,'FASE5_ENEMIGOS='),getValues(TEXT,'FASE5_ENEMIGOS_POS='),getValues(TEXT,'FASE5_PLATAFORMAS='),getValues(TEXT,'FASE5_ANIMACIONES='),getValues(TEXT,'FASE5_POS_ANIMACIONES='),getValues(TEXT,'FASE5_POCIONES='),getValues(TEXT,'FASE5_POS_POCIONES='),None,None,None,None,None,None, False)
                self.director.cambiarEscena(fase)
            elif self.numeroFase == 5:
                self.director.salirEscena()


        


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
    def __init__(self,image,image_scale):
        if image is not None: 
            self.sol = GestorRecursos.CargarImagen(image, -1)
            values = convertPosValues(image_scale,'pos')
            self.sol = pygame.transform.scale(self.sol, (values[0],values[1]))
            self.rect = self.sol.get_rect()
            self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
            self.update(0)
        else:
            self.sol = None
            self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
            self.colorCielo = (0, 0, 0)
            self.update(0)

    def update(self, tiempo):
        if self.sol is not None:
            self.posicionx += VELOCIDAD_SOL * tiempo
            if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
                self.posicionx = 0
            self.rect.right = self.posicionx
            # Calculamos el color del cielo
            if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
                ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
            else:
                ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
            self.colorCielo = (0*ratio, 0*ratio, 0)
         
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        if self.sol is not None:
            # Y ponemos el sol
            pantalla.blit(self.sol, self.rect)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self,image,scale_value):
        self.imagen = GestorRecursos.CargarImagen(image, None)

        values = convertPosValues(scale_value,'pos')
        self.imagen = pygame.transform.scale(self.imagen, (values[0], values[1]))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
