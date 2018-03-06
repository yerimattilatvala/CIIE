
from os import path 
from fase import Plataforma
import pygame

DATA_PY = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.normpath(path.join(DATA_PY, '..', 'imagenes/')) 
FONT_DIR = path.normpath(path.join(DATA_PY, '..', 'fonts/'))
MENU_OPTIONS = ["Empezar aventura", "Cargar aventura", "Opciones", "Salir del juego"]
MENU_DIFFICULTY = ["Aprendiz enano","Enano","Guerrero enano","Menu Principal"]
OPTIONS = ["NO IMPLEMENTADO"]
DESCRIPTION_MENU = ["Emprende la aventura que puede marcar el destino de Kilvas.", "Carga una partida guardada."]
FONT_MENU = "INCANTAT"
TITLE = "TITULO DEL JUEGO"
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

CERVEZA_0 = 'cerveza_0.png'
CERVEZA_1 = 'cerveza_1.png'
CERVEZA_2 = 'cerveza_2.png'
CERVEZA_3 = 'cerveza_3.png'
CERVEZA_4 = 'cerveza_4.png'
CERVEZA_5 = 'cerveza_5.png'
CERVEZA_6 = 'cerveza_6.png'
CERVEZA_7 = 'cerveza_7.png'
CERVEZA_8 = 'cerveza_8.png'
FASE0_FONDO = 'decorado5.png'
FASE0_FONDO_SCALE = (5000,300)
FASE0_POS_JUGADOR = (200,551)
FASE0_ENEMIGOS_POS = [(1000, 551),(2500, 551),(3100, 418)]
FASE0_PLATAFORMAS = [Plataforma(pygame.Rect(0, 550, 5000, 15)),Plataforma(pygame.Rect(890, 417, 160, 10)),Plataforma(pygame.Rect(0, 417, 300, 10)),Plataforma(pygame.Rect(3010, 417, 250, 10)),Plataforma(pygame.Rect(3400, 417, 200, 10))]