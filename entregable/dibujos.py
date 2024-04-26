import pygame
from configuracion import tipos_barcos,BLACK,BLUE,GREEN,GREY,WHITE,lado,TAMAÑO,letras,RED,velocidad_texto
from interfaz import win,monospace_large
from texto import tiempo_ultima_alerta
from texto import texto_alerta 


def dibuja_cuadricula(x0, y0):
    """
    Dibuja la cuadrícula del tablero de juego en la ventana.
    
    Esta función dibuja la cuadrícula del tablero de juego en la posición especificada en la ventana.
    
    Args:
        x0 (int): La coordenada x de la esquina superior izquierda de la cuadrícula.
        y0 (int): La coordenada y de la esquina superior izquierda de la cuadrícula.
    """
    # Dibujar el cuadro exterior de la cuadrícula
    pygame.draw.rect(win, WHITE,
                    (x0, y0,
                    lado*TAMAÑO['LADO_CUADRADO'], lado*TAMAÑO['LADO_CUADRADO']))
    
    # Dibujar líneas horizontales
    for j in range(0,lado+1):
        pygame.draw.line(win, BLACK,
                        (x0, y0 + TAMAÑO['LADO_CUADRADO']*j),
                        (x0 + TAMAÑO['LADO_CUADRADO']*lado, y0 + TAMAÑO['LADO_CUADRADO']*j), 1)
    
    # Dibujar letras en las filas
    for j in range(0,lado):
        letra = monospace_large.render(letras[j], True, BLACK) 
        win.blit(letra, (x0 - TAMAÑO['LADO_CUADRADO'], y0 + TAMAÑO['LADO_CUADRADO']*j))

    # Dibujar líneas verticales
    for j in range(0,lado+1):
        pygame.draw.line(win, BLACK,
                        (x0 + TAMAÑO['LADO_CUADRADO']*j, y0),
                        (x0 + TAMAÑO['LADO_CUADRADO']*j, y0 + TAMAÑO['LADO_CUADRADO']*lado), 1)

    # Dibujar números en las columnas


def dibuja_un_tablero(x0, y0, tablero):
    """
    Dibuja un tablero en la ventana del juego.
    
    Esta función dibuja un tablero en la posición especificada en la ventana del juego.
    
    Args:
        x0 (int): La coordenada x de la esquina superior izquierda del tablero.
        y0 (int): La coordenada y de la esquina superior izquierda del tablero.
        tablero (list): El tablero a dibujar.
    """
    # Dibujar la cuadrícula del tablero
    dibuja_cuadricula(x0, y0)
    
    # Iterar sobre cada fila y columna del tablero
    for fila in range(lado):
        for columna in range(lado):
            casilla = tablero[fila][columna]
            # Dibujar las fichas según su tipo
            if casilla in 'BOX':
                if casilla == 'B':
                    color = GREY
                elif casilla == 'O':
                    color = BLUE
                elif casilla == 'X':
                    color = RED
                # Dibujar una ficha circular en la posición correspondiente
                pygame.draw.circle(win, color,
                                (x0 + TAMAÑO['LADO_CUADRADO']*fila + TAMAÑO['LADO_CUADRADO']//2, y0 + TAMAÑO['LADO_CUADRADO']*columna + TAMAÑO['LADO_CUADRADO']//2),
                                TAMAÑO['LADO_CUADRADO']//2)
            elif (casilla == ' ') or (casilla == '.'):
                # No hacer nada si la casilla está vacía o es un punto
                pass
            else:
                # Dibujar el contenido de la casilla (letra) en la posición correspondiente
                letra = monospace_large.render(casilla, True, BLACK)
                win.blit(letra, (x0 + TAMAÑO['LADO_CUADRADO']*fila, y0 + TAMAÑO['LADO_CUADRADO']*columna))
    for j in range(0,lado):
        letra = monospace_large.render(str(j+1), True, BLACK)
        win.blit(letra, (x0 + TAMAÑO['LADO_CUADRADO']*j + (TAMAÑO['LADO_CUADRADO'] - TAMAÑO['tamaño_letra']), y0 + TAMAÑO['LADO_CUADRADO']*lado))

def dibuja_tableros(tablero1, tablero2):
    """
    Dibuja dos tableros en la ventana del juego.
    
    Esta función dibuja dos tableros en la ventana del juego, uno al lado del otro, con el tablero 1 visible y el tablero 2 con los barcos ocultos.
    
    Args:
        tablero1 (list): El primer tablero a dibujar.
        tablero2 (list): El segundo tablero a dibujar.
    """
    # Dibujar el tablero 1
    x0 = TAMAÑO['margen']
    y0 = TAMAÑO['margen']
    dibuja_un_tablero(x0, y0, tablero1)
    
    # Dibujar el tablero 2 con los barcos ocultos
    x0 = TAMAÑO['margen'] + TAMAÑO['separacion'] + TAMAÑO['LADO_CUADRADO']*lado
    y0 = TAMAÑO['margen']
    tablero2_oculto = oculta_barcos(tablero2)  # Ocultar los barcos del tablero 2
    dibuja_un_tablero(x0, y0, tablero2_oculto)
    
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.update()

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
        nueva_fila = [(' ' if casilla=='B' else casilla) for casilla in fila]  # Reemplazar 'B' con espacio en blanco
        nuevo_tablero.append(nueva_fila)
    return nuevo_tablero

def dibuja_alerta():
    """
    Dibuja la alerta en la ventana del juego.

    Esta función dibuja la alerta en la ventana del juego.

    """
    hasta_aqui = int((pygame.time.get_ticks() - tiempo_ultima_alerta)/velocidad_texto)
    texto = texto_alerta[:hasta_aqui]
    if hasta_aqui > len(texto_alerta):
        pygame.mixer.music.stop()
    x_alerta = 50
    y_alerta = TAMAÑO['ALTO_VENTANA'] - 100
    pygame.draw.rect(win, WHITE,
                    (x_alerta, y_alerta, TAMAÑO['ANCHO_VENTANA'], TAMAÑO['LADO_CUADRADO']))
    win.blit(monospace_large.render(texto, True, BLACK), (x_alerta, y_alerta))

#dibujos de barcos 

def dibuja_barcos_en_fila(x, y, barco_seleccionado, barcos_colocados):
    """
    Dibuja los barcos en una fila del panel de selección de barcos.
    
    Esta función dibuja los barcos en una fila del panel de selección de barcos, marcando el barco seleccionado y los barcos ya colocados.
    
    Args:
        x (int): La coordenada x de la esquina superior izquierda del panel.
        y (int): La coordenada y de la esquina superior izquierda del panel.
        barco_seleccionado (int): El índice del barco seleccionado.
        barcos_colocados (list): Una lista que indica qué barcos ya han sido colocados.
        
    Returns:
        list: Una lista que indica qué barcos están en cada columna del panel.
    """
    barco_en_columna = [-1]*(sum(tipos_barcos) + len(tipos_barcos))
    columna = 0
    for j, largo in enumerate(tipos_barcos):
        if j == barco_seleccionado:
            color = BLUE
        elif barcos_colocados[j]:
            color = GREEN
        else:
            color = GREY
        dibuja_barco_desde_arriba(largo, x + columna*TAMAÑO['LADO_CUADRADO'], y, False, color)
        barco_en_columna[columna:columna+largo] = [j]*largo
        columna = columna + largo + 1
    return barco_en_columna


def dibuja_barco_desde_arriba(largo, x, y, vertical, color=GREY):
    """
    Dibuja un barco en el tablero desde arriba.
    
    Esta función dibuja un barco en el tablero desde arriba, con la opción de dibujarlo vertical u horizontalmente.
    
    Args:
        largo (int): La longitud del barco.
        x (int): La coordenada x de la esquina superior izquierda del barco.
        y (int): La coordenada y de la esquina superior izquierda del barco.
        vertical (bool): True si el barco se dibuja verticalmente, False si se dibuja horizontalmente.
        color (tuple): El color del barco. Por defecto, es GREY.
    """
    if vertical:
        pygame.draw.polygon(win, color, [
            (x, y + TAMAÑO['LADO_CUADRADO']//2),
            (x, y + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1)),
            (x + TAMAÑO['LADO_CUADRADO']//2, y + TAMAÑO['LADO_CUADRADO']*largo),
            (x + TAMAÑO['LADO_CUADRADO'], y + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1)),
            (x + TAMAÑO['LADO_CUADRADO'], y + TAMAÑO['LADO_CUADRADO']//2),
            (x + TAMAÑO['LADO_CUADRADO']//2, y)
            ])
    else:
        pygame.draw.polygon(win, color, [
            (x + TAMAÑO['LADO_CUADRADO']//2, y),
            (x + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1), y),
            (x + TAMAÑO['LADO_CUADRADO']*largo, y + TAMAÑO['LADO_CUADRADO']//2),
            (x + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1), y + TAMAÑO['LADO_CUADRADO']),
            (x + TAMAÑO['LADO_CUADRADO']//2, y + TAMAÑO['LADO_CUADRADO']),
            (x, y + TAMAÑO['LADO_CUADRADO']//2)
            ])

