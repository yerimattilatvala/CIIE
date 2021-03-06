
from os import path 


DATA_PY = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.normpath(path.join(DATA_PY, '..', 'imagenes/')) 
FONT_DIR = path.normpath(path.join(DATA_PY, '..', 'fonts/'))
MENU_OPTIONS = ["Empezar aventura", "Cargar aventura", "Opciones", "Salir del juego"]
MENU_DIFFICULTY = ["Fase 0","Fase 1","Fase 2","Menu Principal"]
OPTIONS = ["NO IMPLEMENTADO"]
DESCRIPTION_MENU = ["Emprende la aventura que puede marcar el destino de Kilvas.", "Carga una partida guardada."]
FONT_MENU = "INCANTAT"
TITLE = "KILVAS LAST HOPE"
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

CERVEZA_0 = 'cerveza_0.png'
CERVEZA_1 = 'cerveza_1.png'
CERVEZA_2 = 'cerveza_2.png'
CERVEZA_3 = 'cerveza_3.png'
CERVEZA_4 = 'cerveza_4.png'
TEXT = 'valoresFases.txt'
