# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
import importlib



# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

# text => valoresFases.txt
# campo => FASE_NOMBRE_CAMPO=        IMPORTANTE PASALO CO IGUAL(=)
# NOMBRE => 1,2,....
# CAMPO => FONDO,FONDO_SCALE,POS_JUG,ENEM, ENEM_POS, PLAT_POS....LO QUE SEA
def getValues(text,campoSolicitado): 
    value = None
    myfile = open(text, 'r')
    for x in  myfile.readlines():
        if x[0:len(campoSolicitado)] == campoSolicitado:
            value = x[x.find(campoSolicitado)+len(campoSolicitado):len(x)-1]
    myfile.close()
    return value

def convertPosValues(field,fieldType):
    r = []
    l = []
    if fieldType == 'ace':
        for x in field.split():
            r.append(int(x))
    elif fieldType == 'pos':
        for x in field.split():
            r.append(int(x))
        return tuple(r)
    elif fieldType =='enemy':
        c = 0
        for x in field.split():
            l.append(int(x))
            c+=1
            if c == 2:
                c=0
                r.append(tuple(l))
                l = []
    elif fieldType =='plat':
        c = 0
        for x in field.split():
            l.append(int(x))
            c+=1
            if c == 4:
                c=0
                r.append(tuple(l))
                l = []
    return r

def str_to_class(module_name, class_name,val=None):
    try:
        module_ = importlib.import_module(module_name)
        try:
            if val is not None:
                class_ = getattr(module_, class_name)(val)
            else:
                class_ = getattr(module_, class_name)()
        except AttributeError:
            logging.error('Class does not exist')
    except ImportError:
        logging.error('Module does not exist')
    return class_ or None

def convertEnemies(enemies):
    r = []
    for x in enemies.split():
        r.append(str_to_class('personajes',x))
    return r

def convertObst(obstacules,aceleracion):
    r = []
    cont = -1
    for x in obstacules.split(): 
        cont += 1   
        r.append(str_to_class('personajes',x,aceleracion[cont]))
    return r

def convertAnimations(animations):
    r = []
    for x in animations.split():
        r.append(str_to_class('animaciones',x))
    return r

def convertPotions(potions):
    r = []
    for x in potions.split():
        r.append(str_to_class('pociones',x))
    return r

def convertObjects(enemies,action):
    r = []
    cont = -1
    for x in enemies.split():
        cont += 1
        r.append(str_to_class('personajes',x,bool(action[cont])))
    return r