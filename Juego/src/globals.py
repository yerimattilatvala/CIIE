
from os import path 

DATA_PY = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.normpath(path.join(DATA_PY, '..', 'images/')) 
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
