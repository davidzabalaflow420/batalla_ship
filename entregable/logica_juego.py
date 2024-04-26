from asyncio import sleep
import asyncio
from constants import *
import pygame
from random import randint, choice
from configuracion import  lado, TAMAÑO, tipos_barcos,GREY
from  menu import configurar
from texto import alerta, texto_ordenador, texto_victoria,texto_jugador
from utilidades import traducir_coordenadas, traducir_coordenadas_al_reves
from interfaz import init_window,oculta_barcos
from fun_Auxi import tablero_vacio,pprint,comprueba_hundido,disparo,ha_terminado
from dibujos import dibuja_alerta,dibuja_tableros,dibuja_barcos_en_fila,dibuja_barco_desde_arriba
from fun_dispa import disparo_ordenador_medio_listo
from menu import *
from idiomas.es import * 


def se_puede_colocar(largo, fila, columna, vertical, tablero):
    """
    Comprueba si un barco se puede colocar en una posición determinada del tablero.

    Args:
        largo (int): La longitud del barco.
        fila (int): La fila en la que se va a colocar el barco.
        columna (int): La columna en la que se va a colocar el barco.
        vertical (bool): Indica si el barco se coloca verticalmente o no.
        tablero (list): El tablero de juego.

    Returns:
        bool: True si el barco se puede colocar en la posición dada, False en caso contrario.
    """
    if (vertical and fila+largo > lado):
        alerta(texto_alerta_fuera) 
        return False
    if (not vertical and columna+largo > lado):
        alerta(texto_alerta_fuera) 
        return False
    if vertical:
        for y in range(max(0, fila-1), min(fila+largo+1, lado)):
            for x in range(max(0, columna-1), min(columna + 2, lado)):
                if tablero[x][y] == 'B':
                    alerta(texto_alerta_barcos_juntos)  
                    return False
    else:
        for y in range(max(0, fila-1), min(fila+2, lado)):
            for x in range(max(0, columna-1), min(columna + largo+1, lado)):
                if tablero[x][y] == 'B':
                    alerta(texto_alerta_barcos_juntos) 
                    return False
    return True

def coloca_un_barco(tablero, x, y, largo, vertical):
    """
    Coloca un barco en el tablero.

    Args:
        tablero (list): El tablero de juego.
        x (int): La coordenada x de la posición de inicio del barco.
        y (int): La coordenada y de la posición de inicio del barco.
        largo (int): La longitud del barco.
        vertical (bool): Indica si el barco se coloca verticalmente o no.

    Returns:
        list: El tablero con el barco colocado.
    """
    if vertical:
        for j in range(largo):
            tablero = coloca_barcos(tablero, x + j, y)
    else:
        for j in range(largo):
            tablero = coloca_barcos(tablero, x, y + j)
    return tablero

def coloca_barcos(tablero, x, y):
    """
    Coloca un barco en una fila o columna específica del tablero.

    Args:
        tablero (list): El tablero de juego.
        x (int): La coordenada x de la posición de inicio del barco.
        y (int): La coordenada y de la posición de inicio del barco.

    Returns:
        list: El tablero con el barco colocado.
    """
    nuevo_tablero = []
    for numero_fila in range(lado):
        if numero_fila != y:
            fila_antigua = tablero[numero_fila]
            nuevo_tablero.append(fila_antigua)
        else:
            fila_antigua = tablero[numero_fila]
            fila_nueva = []
            for numero_columna in range(lado):
                if numero_columna != x:
                    elemento_antiguo = fila_antigua[numero_columna]
                    fila_nueva.append(elemento_antiguo)
                else:
                    elemento_antiguo = fila_antigua[numero_columna]
                    if elemento_antiguo == ' ':
                        elemento_nuevo = 'B'
                    elif elemento_antiguo == 'B':
                        elemento_nuevo = ' '
                    else:
                        elemento_nuevo = elemento_antiguo
                    fila_nueva.append(elemento_nuevo)
            nuevo_tablero.append(fila_nueva)
    return nuevo_tablero

def ordenador_coloca_un_barco(tablero, largo):
    """
    Coloca un barco aleatoriamente en el tablero.
    
    Args:
        tablero (list): El tablero donde se colocará el barco.
        largo (int): La longitud del barco a colocar.
        
    Returns:
        tuple: El nuevo tablero con el barco colocado y las posiciones ocupadas por el barco.
    """
    buena_posicion = False
    while not buena_posicion:
        vertical = choice([True, False])
        if vertical:
            columna = randint(0, lado-1)
            fila = randint(0, lado-1-largo)
        else: # if horizontal
            columna = randint(0, lado-1-largo)
            fila = randint(0, lado-1)
        buena_posicion = se_puede_colocar(largo, fila, columna, vertical, tablero)
    nuevo_tablero = coloca_un_barco(tablero, fila, columna, largo, vertical)
    if vertical:
        posiciones_barco = [
            (columna, fila + j) for j in range(largo)
        ]
    else:
        posiciones_barco = [(columna+k, fila) for k in range(largo)]
    return nuevo_tablero, posiciones_barco

def ordenador_coloca_barcos(tipos_barcos):
    """
    Coloca barcos aleatoriamente en el tablero para el ordenador.
    
    Args:
        tipos_barcos (list): Lista de longitudes de los barcos a colocar.
        
    Returns:
        tuple: El tablero con los barcos colocados y un diccionario que mapea índices de barcos a sus posiciones.
    """
    tablero = tablero_vacio()
    posiciones_barcos = {}
    for n, largo in enumerate(tipos_barcos):
        tablero, posiciones_barco = ordenador_coloca_un_barco(tablero, largo)
        posiciones_barcos[n] = posiciones_barco
    return tablero, posiciones_barcos


def jugar(tablero1, tablero2, posiciones_barcos1, posiciones_barcos2):
    """
    Función principal que maneja el juego entre el jugador y el ordenador.

    Args:
    - tablero1 (list): El tablero del jugador.
    - tablero2 (list): El tablero del ordenador.
    - posiciones_barcos1 (list): Las posiciones de los barcos del jugador.
    - posiciones_barcos2 (list): Las posiciones de los barcos del ordenador.
    """
    init_window()  # Se inicializa la ventana de juego
    alerta('')  # Se muestra una alerta vacía al principio del juego
    pygame.mixer.music.stop()  # Se detiene la música de fondo
    teclas = []  # Lista para almacenar las teclas presionadas por el jugador
    seguir_jugando = True  # Variable para controlar si se sigue jugando o no

    while seguir_jugando:
        dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros del jugador y del ordenador
        dibuja_alerta()  # Se dibuja la alerta en la ventana de juego
        sleep(0.1)  # Se realiza una pausa para que el juego no corra demasiado rápido
        events = pygame.event.get()  # Se obtienen los eventos ocurridos en pygame
        for event in events:
            if event.type == pygame.QUIT:  # Si se cierra la ventana, se sale del juego
                exit()
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_F10:  # Si se presiona F10, se abre la configuración del juego
                    configurar()
                    init_window()
                    dibuja_tableros(tablero1, tablero2)
                teclas.append(event.key)  # Se agrega la tecla presionada a la lista de teclas

        # Se comprueba si se han presionado suficientes teclas o si se ha presionado Enter o Esc
        if ((len(teclas) >= 3) or
            (teclas and
            (teclas[-1] in (pygame.K_RETURN, pygame.K_ESCAPE)))
        ):
            if (len(teclas) >= 3) and (teclas[2] == pygame.K_RETURN):  # Si se presionaron al menos tres teclas y la tercera es Enter
                coordenadas = chr(teclas[0]) + chr(teclas[1])  # Se obtienen las coordenadas ingresadas por el jugador

                x, y = traducir_coordenadas(coordenadas)  # Se traducen las coordenadas al formato del tablero
                disparo_ok = ((0 <= x < lado) and  # Se verifica si las coordenadas están dentro del tablero
                            (0 <= y < lado))
            else:
                disparo_ok = False  # Si no se presionaron tres teclas o la tercera no es Enter, el disparo no es válido
            teclas = []  # Se reinicia la lista de teclas

            if disparo_ok:  # Si el disparo es válido
                print()
                pprint(tablero1)  # Se imprime el tablero del jugador
                print()
                pprint(tablero2)  # Se imprime el tablero del ordenador
                texto_jugador(coordenadas)  # Se muestra el texto indicando las coordenadas ingresadas por el jugador
                comprueba_hundido(tablero2, posiciones_barcos2, x, y)  # Se verifica si se ha hundido algún barco del ordenador
                tablero2 = disparo(tablero2, x, y)  # Se realiza el disparo en el tablero del ordenador

                if ha_terminado(tablero2):  # Si el ordenador ha perdido todos sus barcos
                    dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                    texto_victoria(texto_has_ganado)  # Se muestra el texto de victoria para el jugador
                    pygame.display.update()  # Se actualiza la ventana de juego
                    sleep(3)  # Se espera un tiempo antes de salir del juego
                    seguir_jugando = False  # Se termina el juego
                dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                sleep(1)  # Se espera un segundo antes de que juegue el ordenador
                x, y = disparo_ordenador_medio_listo(oculta_barcos(tablero1))  # El ordenador realiza su disparo
                texto_ordenador(traducir_coordenadas_al_reves(x, y))  # Se muestra el texto del disparo del ordenador
                comprueba_hundido(tablero1, posiciones_barcos1, x, y)  # Se verifica si se ha hundido algún barco del jugador
                tablero1 = disparo(tablero1, x, y)  # Se realiza el disparo en el tablero del jugador
                
                if ha_terminado(tablero1):  # Si el jugador ha perdido todos sus barcos
                    texto_victoria(texto_has_perdido)  # Se muestra el texto de derrota para el jugador
                    pygame.display.update()  # Se actualiza la ventana de juego
                    sleep(3)  # Se espera un tiempo antes de salir del juego
                    dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                    seguir_jugando = False  # Se termina el juego
            else:
                texto_jugador('??')  # Si las coordenadas ingresadas por el jugador son incorrectas, se muestra un texto de error
                alerta(texto_coordenadas_erroneas)  # Se muestra una alerta indicando que las coordenadas son incorrectas
                


def colocar_barcos():
    """
    Función principal para que el jugador coloque sus barcos en el tablero.

    Returns:
        tuple: Una tupla que contiene el tablero con los barcos colocados y un diccionario de las posiciones de los barcos.
    """
    # Inicializa la ventana del juego y otras variables
    init_window()
    num_barcos = len(tipos_barcos)
    posiciones_barcos = {j:[] for j in range(num_barcos)}
    tablero1 = tablero_vacio()
    tablero2 = tablero_vacio()
    y_coloca_barcos_min = TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO']*(lado+2)
    y_coloca_barcos_max = y_coloca_barcos_min + TAMAÑO['LADO_CUADRADO']
    x_coloca_barcos_min = TAMAÑO['separacion']
    x_coloca_barcos_max = (x_coloca_barcos_min
        + sum(largo for largo in tipos_barcos)*TAMAÑO['LADO_CUADRADO']
        + sum(1 for largo in tipos_barcos)*TAMAÑO['LADO_CUADRADO']
    )
    seguir_colocando = True
    barco_seleccionado = -1
    barcos_colocados = [False]*len(tipos_barcos)
    vertical = False

    # Bucle principal para colocar los barcos
    while seguir_colocando:
        sleep(0.1)
        dibuja_tableros(tablero1, tablero2)
        dibuja_alerta()
        barco_en_columna = dibuja_barcos_en_fila(
            x_coloca_barcos_min, y_coloca_barcos_min,
            barco_seleccionado, barcos_colocados)

        # Eventos del juego
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Verifica si todos los barcos han sido colocados antes de continuar
                if sum(barcos_colocados) < num_barcos:
                    alerta(texto_alerta_sin_terminar)
                else:
                    seguir_colocando = False
            elif event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if event.button == 3:  # Botón derecho del ratón
                    vertical = not vertical
                elif ((barco_seleccionado >= 0) and
                    (TAMAÑO['margen'] <= x < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO']) and
                    (TAMAÑO['margen'] <= y < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO'])):
                    columna = (x - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    fila = (y - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    largo = tipos_barcos[barco_seleccionado]
                    # Verifica si el barco se puede colocar en la posición seleccionada
                    if vertical and (fila+largo <= lado):
                        dibuja_barco_desde_arriba(largo, TAMAÑO['margen']+columna*TAMAÑO['LADO_CUADRADO'], TAMAÑO['margen']+fila*TAMAÑO['LADO_CUADRADO'], vertical, color=GREY)
                    elif (not vertical) and (columna + largo <= lado):
                        dibuja_barco_desde_arriba(largo, TAMAÑO['margen']+columna*TAMAÑO['LADO_CUADRADO'], TAMAÑO['margen']+fila*TAMAÑO['LADO_CUADRADO'], vertical, color=GREY)
                    # Actualiza la ventana del juego
                    pygame.display.update()
                    # Procesa los eventos de ratón
                    if se_puede_colocar(largo, fila, columna, vertical, tablero1):
                        tablero1 = coloca_un_barco(tablero1, fila, columna, largo, vertical)
                        barcos_colocados[barco_seleccionado] = True
                        if vertical:
                            posiciones_barcos[barco_seleccionado] = [
                                (columna, fila + j) for j in range(largo)
                            ]
                        else:
                            posiciones_barcos[barco_seleccionado] = [
                                (columna + j, fila) for j in range(largo)
                            ]
                        barco_seleccionado = -1
                # Verifica si se ha hecho clic en la zona de selección de barcos
                elif ((x_coloca_barcos_min <= x < x_coloca_barcos_max) and
                    (y_coloca_barcos_min <= y < y_coloca_barcos_max)):
                    columna = (x - x_coloca_barcos_min)//TAMAÑO['LADO_CUADRADO']
                    barco_seleccionado = barco_en_columna[columna]
                    # Si el barco seleccionado ya estaba colocado, quita el barco del tablero
                    if barcos_colocados[barco_seleccionado]:
                        for columna, fila in posiciones_barcos[barco_seleccionado]:
                            tablero1[columna][fila] = ' '
                        barcos_colocados[barco_seleccionado] = False

    # Limpia la alerta y detiene la música de alerta
    alerta('')
    pygame.mixer.music.stop()
    return tablero1, posiciones_barcos