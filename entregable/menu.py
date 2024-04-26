import importlib
import pygame
from configuracion import  idiomas, BLACK, tamaños, tipos_barcos,TAMAÑO
from constants import clock
from texto import pantalla_texto,titulo
from interfaz import init_window,tamano_ventana_juego,win,monospace_large,monospace_xxl
from idiomas.es import *
from Batalla import *


def elegir_opcion(opciones):
    """
    Permite al jugador elegir entre una lista de opciones.

    Muestra las opciones en la pantalla y espera a que el jugador haga clic en una de ellas.

    Args:
        opciones (list): Una lista de tuplas que contienen el índice de la opción y el texto de la opción.

    Returns:
        int: El índice de la opción seleccionada por el jugador.

    """
    init_window()
    wth = monospace_xxl.render(titulo, True, BLACK)
    win.blit(wth, (TAMAÑO['ANCHO_VENTANA']/2 - wth.get_bounding_rect().width/2, 50))
    xinicio, yinicio = 100, 200
    linea = 0
    coordenadas_opciones = {}
    espacio = TAMAÑO['tamaño_letra'] + 30
    margen_configuracion = 3
    for indice_opcion, opcion in opciones:
        texto_opcion = monospace_large.render(opcion, True, BLACK)
        r = texto_opcion.get_bounding_rect()
        xtexto = xinicio
        ytexto = yinicio + espacio*linea
        coordenadas_opcion = (
            xinicio + r.left - margen_configuracion,
            ytexto + r.top - margen_configuracion,
            r.width + 2*margen_configuracion,
            r.height + 2*margen_configuracion
        )
        coordenadas_opciones[indice_opcion] = coordenadas_opcion
        pygame.draw.rect(win, BLACK, coordenadas_opcion, 1)
        win.blit(texto_opcion, (xinicio, ytexto))
        linea = linea + 1

    pygame.display.update()
    while True:
        clock.tick(40)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                for opcion, coordenadas in coordenadas_opciones.items():
                    xopcion, yopcion, ancho, alto = coordenadas
                    if ((x > xopcion) and
                        (y > yopcion) and
                        (x < xopcion + ancho) and
                        (y < yopcion + alto)):
                        return opcion
                    

def elegir_idioma():
    """
    Permite al jugador elegir un idioma.

    Muestra una lista de idiomas disponibles y espera a que el jugador seleccione uno.

    Returns:
        int: El índice del idioma seleccionado por el jugador.

    """
    return elegir_opcion(idiomas)
def configurar():
    """
    Configura las opciones del juego.
    
    Esta función permite al jugador configurar diferentes opciones del juego, como el idioma o la resolución de pantalla.
    """
    eleccion = configuracion()
    while eleccion > 0:
        if eleccion == 1:
            # Configurar el idioma del juego
            idioma = elegir_idioma()
            cargar_idioma(idioma)
        elif eleccion == 2:
            # Cambiar la resolución de la pantalla
            tamaño = elegir_resolucion_pantalla()
            cambiar_resolucion_pantalla(tamaño)
        elif eleccion == 3:
            pantalla_texto(texto_instruccion) 
        
        elif eleccion == 4:
            Menu.mostrar_menu()

            

        
        
        eleccion = configuracion()

def configuracion():
    """
    Permite al jugador configurar diversas opciones del juego.

    Muestra una lista de opciones de configuración y espera a que el jugador seleccione una.

    Returns:
        int: El índice de la opción de configuración seleccionada por el jugador.
    """
    opciones = [
        (0, texto_config_jugar),
        (1, texto_config_idioma),
        (2, texto_config_pantalla),
        (3, texto_instrucciones),
        (4, texto_juego_por_consola)
        
]
    eleccion = elegir_opcion(opciones)

    if eleccion == 3: 
        pantalla_texto(texto_instruccion) 
    
    elif eleccion == 4:
        Menu.mostrar_menu()
    

    return eleccion

def elegir_resolucion_pantalla():
    """
    Permite al jugador elegir la resolución de la pantalla del juego.

    Muestra una lista de opciones de resolución de pantalla y espera a que el jugador seleccione una.

    Returns:
        int: El índice de la opción de resolución de pantalla seleccionada por el jugador.

    """
    opciones = [
        (0, texto_resolucion_peque), 
        (1, texto_resolucion_medio), 
        (2, texto_resolucion_grande)
    ]
    return elegir_opcion(opciones)

def cambiar_resolucion_pantalla(indice_tamaño):
    """
    Cambia la resolución de la pantalla del juego.

    Args:
        indice_tamaño (int): El índice del tamaño de pantalla seleccionado.

    """
    global TAMAÑO
    TAMAÑO = tamaños[indice_tamaño]
    tamano_ventana_juego()


def cargar_idioma(idioma):
    """
    Carga un idioma específico para el juego.

    Args:
        idioma (str): El nombre del idioma a cargar.

    """
    mod_idiomas = importlib.import_module('idiomas.' + idioma)
    globals().update(mod_idiomas.__dict__)
    pygame.display.set_caption(titulo)

def volver_a_jugar():
    """
    Pregunta al jugador si desea volver a jugar.

    Muestra un mensaje al jugador preguntando si desea volver a jugar y espera su respuesta.

    Returns:
        bool: True si el jugador desea volver a jugar, False si no.

    """
    tecla = pantalla_texto(texto_volver_a_jugar)
    if tecla == pygame.K_RETURN:
        return True
    elif tecla == pygame.K_ESCAPE:
        return False
    

def intro():
    """
    Muestra la introducción del juego con información sobre la longitud de los barcos.

    Genera y muestra el texto de introducción del juego, incluyendo información sobre la longitud de los barcos.

    """
    texto_colocar = '\n'.join(texto_longitud_barco+str(largo)
        for largo in tipos_barcos)
    texto_total = texto_intro + texto_colocar + texto_continuar
    pantalla_texto(texto_total)

def intro_jugar():
    """
    Muestra la introducción para comenzar a jugar.

    Genera y muestra el texto de introducción para empezar a jugar.

    """
    texto_total = texto_intro_jugar + texto_continuar
    pantalla_texto(texto_total)

def creditos():
    """
    Muestra los créditos del juego.

    Genera y muestra el texto de los créditos del juego.

    """
    texto_total = texto_creditos
    pantalla_texto(texto_total)




