# -*- encoding: utf-8 -*-

import sys
import pygame
import pyganim
from text import *
from pygame.locals import *
from escena import *
from gestorRecursos import *
from values import *
from fase import Fase
from animaciones import AnimacionFuego, AnimacionRayo, AnimacionHumo
from personajes import Jugador

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")

    def set_mouse_selection(self, item, mpos):  
        if item.is_mouse_selection(mpos):
            item.set_font_color(RED)
        else:
            item.set_font_color(WHITE)

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.rect.left and posx <= self.rect.left + self.rect.width) and \
            (posy <= self.rect.bottom and posy >= self.rect.bottom - self.rect.height):
                return True
        return False

    def set_keyboard_selection(self, key):
        for item in self.items:
            item.set_font_color(WHITE)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0
 
        self.items[self.cur_item].set_font_color(RED)

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].value
            self.action = text


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        self.texto = texto
        self.fuente = fuente
        # Se crea la imagen del texto
        self.imagen_texto = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen_texto.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_texto, self.rect)

    def set_font_color(self, color):
        self.imagen_texto = self.fuente.render(self.texto, True, color)
        #self.label = self.text.render


class CampoTexto(TextoGUI):
    def __init__(self, pantalla,texto,fuente,color,tamano,x,y,accion):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.Font(os.path.join(FONT_DIR, fuente + ".TTF"), tamano)
        self.accion = accion
        TextoGUI.__init__(self, pantalla, fuente, color, texto, (x, y))

    def accion(self):
        self.accion()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'Salir', (610, 565))
    def accion(self):
        self.pantalla.menu.salirPrograma()

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen,titulo):
        self.menu = menu
        self.title = titulo
        self.cur_item = None
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        # Se tiene una lista de animaciones
        self.animaciones = []
        self.mouse_is_visible = True


    def eventos(self, lista_eventos):
        mpos = pygame.mouse.get_pos()   # captura posicion del raton
        for evento in lista_eventos:
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                self.mouse_is_visible = False
                self.set_keyboard_selection(evento.key)
            if evento.type == MOUSEBUTTONDOWN:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

        if pygame.mouse.get_rel() != (0, 0):
            self.mouse_is_visible = True
            self.cur_item = None

        self.set_mouse_visibility()


    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)


    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())

        mpos = pygame.mouse.get_pos()   # captura posicion del raton
        pantalla.blit(self.title.render,(10,20)) #TITLE
        for item in self.elementosGUI:
            if self.mouse_is_visible:
                self.set_mouse_selection(item, mpos)
            pantalla.blit(item.imagen_texto, item.rect)

        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla,0)
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)


    def set_mouse_selection(self, item, mpos):  
        if item.is_mouse_selection(mpos):
            item.set_font_color(RED)
        else:
            item.set_font_color(WHITE)

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.rect.left and posx <= self.rect.left + self.width) and \
            (posy >= self.rect.bottom and posy <= self.rect.bottom + self.height):
                return True
        return False

    def set_keyboard_selection(self, key):
        for item in self.elementosGUI:
            item.set_font_color(WHITE)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.elementosGUI) - 1
            elif key == K_DOWN and \
                    self.cur_item < len(self.elementosGUI) - 1:
                self.cur_item += 1
            elif key == K_DOWN and \
                    self.cur_item == len(self.elementosGUI) - 1:
                self.cur_item = 0
 
        self.elementosGUI[self.cur_item].set_font_color(RED)

        if key == K_SPACE or key == K_RETURN:
            text = self.elementosGUI[self.cur_item].accion()
            self.action = text

    

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'Intro.jpg', Text(TITLE,60,FONT_MENU))

        self.campos_texto()
        

        # La animacion del fuego
        animacionFuego = AnimacionFuego()
        # Aumentamos un poco el tamaño de la animacion
        animacionFuego.scale((100,200))
        # La situamos en su posicion
        animacionFuego.posicionx = 70
        animacionFuego.posiciony = 100
        # Iniciamos la animacion
        animacionFuego.play()
        # Y la introducimos en la lista
        self.animaciones.append(animacionFuego)

        # La animacion del humo
        animacionHumo = AnimacionHumo()
        # La situamos en su posicion
        animacionHumo.posicionx = 695
        animacionHumo.posiciony = 420
        # Iniciamos la animacion
        animacionHumo.play()
        # Y la introducimos en la lista
        self.animaciones.append(animacionHumo)

        # La animacion del rayo
        animacionRayo = AnimacionRayo()
        # Rotamos un poco la animacion
        animacionRayo.rotate(30)
        # La situamos en su posicion
        animacionRayo.posicionx = 512
        animacionRayo.posiciony = 130
        # Iniciamos la animacion
        animacionRayo.play()
        # Y la introducimos en la lista
        self.animaciones.append(animacionRayo)

    def campos_texto(self):
        textoJugar = CampoTexto(self,'Empezar aventura',FONT_MENU,WHITE,30,20,200,self.menu.mostrarPantallaDificultad)
        textoCargar = CampoTexto(self,'Cargar aventura',FONT_MENU,WHITE,30,20,300,self.menu.noHaceNada)
        textoOpciones = CampoTexto(self,'Opciones',FONT_MENU,WHITE,30,20,400,self.menu.noHaceNada)
        textoSalir = CampoTexto(self,'Salir del juego',FONT_MENU,WHITE,30,20,500,self.menu.salirPrograma)

        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoCargar)
        self.elementosGUI.append(textoOpciones)
        self.elementosGUI.append(textoSalir)

#Si se necesitan más menús se copia esta clase, se modifican los campos de texto
#  y se añade la pantalla y el método para llamarla abajo en la clase Menu
class PantallaDificultadGUI(PantallaInicialGUI):
    def __init__(self, menu):
        PantallaInicialGUI.__init__(self,menu)

    def campos_texto(self):
        #CampoTexto(self,texto,nombre_fuente,tamaño_fuente,x,y,accion_a_realizar_al_pulsar)
        textFase0 = CampoTexto(self,'Fase Test',FONT_MENU,WHITE,30,20,200,self.menu.ejecutarJuego)
        textFase1 = CampoTexto(self,'Ruben',FONT_MENU,WHITE,30,20,250,self.menu.ejecutarFase1)
        textFase2 = CampoTexto(self,'Isa-GIGANTES',FONT_MENU,WHITE,30,20,300,self.menu.ejecutarFase3)
        textFase3 = CampoTexto(self,'Yeray',FONT_MENU,WHITE,30,20,350,self.menu.ejecutarFase2)
        #textFase4 = CampoTexto(self,'Nagas',FONT_MENU,WHITE,30,20,400,self.menu.ejecutarFase4)
        textFase5 =CampoTexto(self,'Dani',FONT_MENU,WHITE,30,20,450,self.menu.ejecutarFase5)
        textMenu = CampoTexto(self,'Menu Principal',FONT_MENU,WHITE,30,20,500,self.menu.mostrarPantallaInicial)

        self.elementosGUI.append(textFase0)
        self.elementosGUI.append(textFase1)
        self.elementosGUI.append(textFase2)
        self.elementosGUI.append(textFase3)
        #self.elementosGUI.append(textFase4)
        self.elementosGUI.append(textFase5)
        self.elementosGUI.append(textMenu)


# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Escena):

    def __init__(self, director):
        #Creamos a nuestro jugador
        self.jugador = Jugador()
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director);
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self))
        self.listaPantallas.append(PantallaDificultadGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.salirPrograma()


    def ejecutarJuego(self):
        fase = Fase(self.director,self.jugador,1,4800,getValues(TEXT,'FASE1_FONDO='),getValues(TEXT,'FASE1_FONDO_SCALE='),getValues(TEXT,'FASE1_CIELO='),getValues(TEXT,'FASE1_CIELO_SCALE='),getValues(TEXT,'FASE1_POS_JUGADOR='),getValues(TEXT,'FASE1_ENEMIGOS='),getValues(TEXT,'FASE1_ENEMIGOS_POS='),getValues(TEXT,'FASE1_PLATAFORMAS='),None,None,getValues(TEXT,'FASE1_POCIONES='),getValues(TEXT,'FASE1_POS_POCIONES='),getValues(TEXT,'FASE1_OBSTACULOS='),getValues(TEXT,'FASE1_OBSTACULOS_POS='),getValues(TEXT,'FASE1_ACELERACION='),None,None,None,False)
        self.director.apilarEscena(fase)
		
    def ejecutarFase1(self):
        fase = Fase(self.director,self.jugador, 1,4800, getValues(TEXT,'FASE1_FONDO='),getValues(TEXT,'FASE1_FONDO_SCALE='),getValues(TEXT,'FASE1_CIELO='),getValues(TEXT,'FASE1_CIELO_SCALE='),getValues(TEXT,'FASE1_POS_JUGADOR='),getValues(TEXT,'FASE1_ENEMIGOS='),getValues(TEXT,'FASE1_ENEMIGOS_POS='),getValues(TEXT,'FASE1_PLATAFORMAS='),None,None,getValues(TEXT,'FASE1_POCIONES='),getValues(TEXT,'FASE1_POS_POCIONES='),getValues(TEXT,'FASE1_OBSTACULOS='),getValues(TEXT,'FASE1_OBSTACULOS_POS='),getValues(TEXT,'FASE1_ACELERACION='),None,None,None,False)
        self.director.apilarEscena(fase)
        
        
    def ejecutarFase2(self):
        fase = Fase(self.director,self.jugador, 2, 5400, getValues(TEXT,'FASE2_FONDO='),getValues(TEXT,'FASE2_FONDO_SCALE='),getValues(TEXT,'FASE2_CIELO='),getValues(TEXT,'FASE2_CIELO_SCALE='),getValues(TEXT,'FASE2_POS_JUGADOR='),getValues(TEXT,'FASE2_ENEMIGOS='),getValues(TEXT,'FASE2_ENEMIGOS_POS='),getValues(TEXT,'FASE2_PLATAFORMAS='),None,None,getValues(TEXT,'FASE2_POCIONES='),getValues(TEXT,'FASE2_POS_POCIONES='),getValues(TEXT,'FASE2_OBSTACULOS='),getValues(TEXT,'FASE2_OBSTACULOS_POS='),getValues(TEXT,'FASE2_ACELERACION='),None,None,None, False)
        self.director.apilarEscena(fase)
        

    def ejecutarFase3(self):
        fase = Fase(self.director,self.jugador, 3, 4900, getValues(TEXT,'FASE3_FONDO='),getValues(TEXT,'FASE3_FONDO_SCALE='),None, None, getValues(TEXT,'FASE3_POS_JUGADOR='),getValues(TEXT,'FASE3_ENEMIGOS='),getValues(TEXT,'FASE3_ENEMIGOS_POS='),getValues(TEXT,'FASE3_PLATAFORMAS='),None,None,getValues(TEXT,'FASE3_POCIONES='), getValues(TEXT,'FASE3_POS_POCIONES='),getValues(TEXT,'FASE3_OBSTACULOS=') , getValues(TEXT,'FASE3_OBSTACULOS_POS='), getValues(TEXT,'FASE3_ACELERACION='),None,None,None, False)
        self.director.apilarEscena(fase)
        

    def ejecutarFase4(self):
        fase = Fase(self.director,self.jugador, 4, getValues(TEXT,'MAX_DISTANCE_4='), getValues(TEXT,'FASE4_FONDO='),getValues(TEXT,'FASE4_FONDO_SCALE='), None, None, getValues(TEXT,'FASE4_POS_JUGADOR='),getValues(TEXT,'FASE4_ENEMIGOS='),getValues(TEXT,'FASE4_ENEMIGOS_POS='),getValues(TEXT,'FASE4_PLATAFORMAS='),None,None,None,None,None,None,None,None,None,None, False)
        self.director.apilarEscena(fase)

    def ejecutarFase5(self):
        fase = Fase(self.director,self.jugador, 5, 4600, getValues(TEXT,'FASE5_FONDO='),getValues(TEXT,'FASE5_FONDO_SCALE='),getValues(TEXT,'FASE5_CIELO='),getValues(TEXT,'FASE5_CIELO_SCALE='),getValues(TEXT,'FASE5_POS_JUGADOR='),getValues(TEXT,'FASE5_ENEMIGOS='),getValues(TEXT,'FASE5_ENEMIGOS_POS='),getValues(TEXT,'FASE5_PLATAFORMAS='),getValues(TEXT,'FASE5_ANIMACIONES='),getValues(TEXT,'FASE5_POS_ANIMACIONES='),getValues(TEXT,'FASE5_POCIONES='),getValues(TEXT,'FASE5_POS_POCIONES='),None,None,None,None,None,None, False)
        self.director.apilarEscena(fase)
        

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def mostrarPantallaDificultad(self):
        self.pantallaActual = 1

    def noHaceNada(self):
        #Solo está para evitar crash mientras no tenemos las opciones
        pass
