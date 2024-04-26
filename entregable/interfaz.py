import pygame
from configuracion import TAMAÑO, WHITE
from constants import *

win = pygame.display.set_mode((TAMAÑO['ANCHO_VENTANA'], TAMAÑO['ALTO_VENTANA']))

def init_window():
    """
    Inicializa la ventana del juego.
    
    Esta función configura el tamaño de la ventana y establece el título del juego.
    """
    # Configurar el tamaño de la ventana y establecer el título
    tamano_ventana_juego()
    win.fill(WHITE)
    pygame.display.set_caption(titulo)
    
def tamano_ventana_juego():
    """
    Establece el tamaño de la ventana del juego y las fuentes.
    
    Esta función configura el tamaño de la ventana del juego y carga las fuentes necesarias.
    """
    global monospace_large, monospace_xxl
    # Configurar el tamaño de la ventana
    pygame.display.set_mode((TAMAÑO['ANCHO_VENTANA'], TAMAÑO['ALTO_VENTANA']))
    # Cargar fuentes para texto en diferentes tamaños
    monospace_large = pygame.font.SysFont('Monospace', TAMAÑO['tamaño_letra'])
    monospace_xxl = pygame.font.SysFont('Monospace Bold', TAMAÑO['tamaño_letra_grande'])
    # Llenar la ventana con un color de fondo blanco
    win.fill(WHITE)

def oculta_barcos(tablero):
    """
    Oculta los barcos en el tablero.
    
    Esta función crea un nuevo tablero donde los barcos están ocultos, representados como espacios en blanco.
    
    Args:
        tablero (list): El tablero original con los barcos.
        
    Returns:
        list: El nuevo tablero donde los barcos están ocultos.
    """
    nuevo_tablero = []
    for fila in tablero:
        nueva_fila = [(' ' if casilla=='B' else casilla) for casilla in fila]  
        nuevo_tablero.append(nueva_fila)
    return nuevo_tablero



