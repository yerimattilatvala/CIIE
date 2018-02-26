# -*- coding: utf-8 -*-

import pygame,sys
from text import *
from util import *

class Menu(object):
    def __init__(self,screen,title,items):
        self.screen = screen;
        self.title = Text(title,60,FONT_MENU)
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.items = []
        self.action = None
        pos_y = self.screen.get_rect().width/len(items)
        for index, item in enumerate(items):
            menu_item = MenuItem(item,FONT_MENU, 32)
            t_h = len(items) * menu_item.height
            pos_x = 20
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            pos_y += self.screen.get_rect().width/(len(items)**1.9)
        self.mouse_is_visible = True
        self.cur_item = None
        
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

 #CAMBIA EL COLOR DE LA OPCION AL SELECIONARLA CON EL TECLADO
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

#CAMBIA EL COLOR DE LA OPCION AL PASAR POR ENCIMA CON EL RATON
    def set_mouse_selection(self, item, mpos):  
        if item.is_mouse_selection(mpos):
            item.set_font_color(RED)
        else:
            item.set_font_color(WHITE)

    def draw(self):
        mpos = pygame.mouse.get_pos()   # captura posicion del raton
        self.screen.blit(self.title.render,(10,20))
        for item in self.items:
            if self.mouse_is_visible:
                self.set_mouse_selection(item, mpos)
            self.screen.blit(item.label, item.position)

    # controlar eventos
    def check_events(self):
        mpos = pygame.mouse.get_pos()   # captura posicion del raton
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.mouse_is_visible = False
                self.set_keyboard_selection(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in self.items:
                    if item.is_mouse_selection(mpos):
                        self.action= item.value

        if pygame.mouse.get_rel() != (0, 0):
            self.mouse_is_visible = True
            self.cur_item = None

        self.set_mouse_visibility()

    # METODO SOBRECARGADO
    def handle_selection(self):
        pass

class MenuItem(Menu):
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, (pos_x, pos_y)=(0, 0)):
        self.value = text   
        self.text = Text(self.value,font_size,font,font_color)
        self.label = self.text.render
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

# DETERMINA SI EL ITEM EL SELECCIONADO POR EL RATON
    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, color):
        self.text.set_color(color)
        self.label = self.text.render

class MainMenu(Menu):
    def __init__(self,screen,title,items):
        Menu.__init__(self,screen,title,items)
        self.active = True
        self.background = load_image("Intro.jpg")

    def run(self):
        while self.active==True:
            self.screen.blit(self.background, (0,0)) 
            self.check_events()
            self.handle_selection()
            self.draw()
            pygame.display.flip()
            
    def handle_selection(self):
        if self.action == MENU_OPTIONS[0]:
            self.action = None
            NoMenu = MenuDificultad(self.screen,"Dificultad",MENU_DIFFICULTY)
            NoMenu.run()
        '''if self.action == MENU_OPTIONS[1]:
            #print(2)
        if self.action == MENU_OPTIONS[2]:
            #print(3)'''
        if self.action == MENU_OPTIONS[3]:
            pygame.quit()
            sys.exit()


class MenuDificultad(Menu):
    def __init__(self,screen,title,items):
        Menu.__init__(self,screen,title,items)
        self.active = True
        self.background = load_image("Intro.jpg")

    def run(self):
        while self.active==True:
            self.screen.blit(self.background, (0,0)) 
            self.check_events()
            self.handle_selection()
            self.draw()
            pygame.display.flip()

    def handle_selection(self):
        '''if self.action == MENU_DIFFICULTY[0]:
            #print(1)
        if self.action == MENU_DIFFICULTY[1]:
            #print(2)
        if self.action == MENU_DIFFICULTY[2]:
            #print(3)'''
        if self.action == MENU_DIFFICULTY[3]:
           self.active = False

pygame.init()
screen = pygame.display.set_mode((795, 525), 0, 32) #CARATERISTICAS DE LA VENTANA
pygame.display.set_caption('Game Menu')
gm = MainMenu(screen,TITLE,MENU_OPTIONS)
gm.run()
