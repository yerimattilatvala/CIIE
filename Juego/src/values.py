
from os import path 


DATA_PY = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.normpath(path.join(DATA_PY, '..', 'imagenes/')) 
FONT_DIR = path.normpath(path.join(DATA_PY, '..', 'fonts/'))
MENU_OPTIONS = ["Empezar aventura", "Cargar aventura", "Opciones", "Salir del juego"]
MENU_DIFFICULTY = ["Fase 0","Fase 1","Fase 2","Menu Principal"]
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

FASE0_FONDO = 'decorado5.png'
FASE0_FONDO_SCALE = (5000,300)
FASE0_POS_JUGADOR = (200,551)
FASE0_ENEMIGOS_POS = [(1000, 551),(2500, 551),(3100, 418)]
FASE0_PLATAFORMAS = [(0, 550, 5000, 15),(890, 417, 160, 10),(0, 417, 300, 10),(3010, 417, 250, 10),(3400, 417, 200, 10)]


FASE1_FONDO = 'fase1Fondo.png'
FASE1_FONDO_SCALE = (5000,300)
FASE1_POS_JUGADOR = (200,551)
FASE1_ENEMIGOS_POS = [(1000, 551),(2500, 551),(3100, 418)]
FASE1_PLATAFORMAS = [(0, 550, 5000, 15),(890, 417, 160, 10),(0, 417, 300, 10),(3010, 417, 250, 10),(3400, 417, 200, 10)]