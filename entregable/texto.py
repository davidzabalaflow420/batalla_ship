import pygame
from configuracion import TAMAÑO, velocidad_texto,  BLACK, WHITE, lado, RED
from constants import clock
from interfaz import init_window,tamano_ventana_juego

# Luego, donde necesites usar monospace_xxl, podrías hacer algo como:
tamano_ventana_juego()
# Ahora monospace_xxl debería estar disponible para su uso en este archivo

from interfaz import monospace_large,monospace_xxl

win = pygame.display.set_mode((TAMAÑO['ANCHO_VENTANA'], TAMAÑO['ALTO_VENTANA']))

# Definir el título del juego
titulo = 'pyBattleship classic'

def pantalla_texto(texto_total):
    """
    Muestra texto en pantalla con efecto de desplazamiento.

    Args:
        texto_total (str): El texto completo que se va a mostrar en pantalla.

    Returns:
        int: La tecla presionada por el usuario para continuar (ENTER o ESCAPE).
    """
    # Reproduce música de fondo y inicializa la ventana del juego
    pygame.mixer.music.play(-1)
    init_window()
    
    # Renderiza y muestra el título en la ventana
    wth = monospace_xxl.render(titulo, True, BLACK)
    win.blit(wth, (TAMAÑO['ANCHO_VENTANA']/2 - wth.get_bounding_rect().width/2, 50))
    
    # Inicializa el tiempo de inicio para el efecto de desplazamiento del texto
    tiempo_inicial = pygame.time.get_ticks()
    
    while True:
        clock.tick(40)
        
        # Calcula la posición del texto que se va a mostrar
        hasta_aqui = int((pygame.time.get_ticks() - tiempo_inicial)/velocidad_texto)
        
        # Detiene la música si se ha mostrado todo el texto
        if hasta_aqui > len(texto_total):
            pygame.mixer.music.stop()
        
        # Prepara el texto que se va a mostrar
        texto = texto_total[:hasta_aqui]
        
        # Muestra el texto en la ventana
        dibuja_texto_largo(texto, 100, 200, monospace_large, TAMAÑO['tamaño_letra'])
        pygame.display.update()
        
        # Captura eventos del usuario
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                # Si se presiona ENTER o ESCAPE, se detiene la música y se devuelve la tecla presionada
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    pygame.mixer.music.stop()
                    return event.key
                # Si se presiona ESPACIO o ABAJO, se simula el efecto de mostrar todo el texto de inmediato
                elif event.key in (pygame.K_SPACE, pygame.K_DOWN):
                    # Un truco para que muestre todo el texto instantáneamente
                    tiempo_inicial = -100000
                    pygame.mixer.music.stop()
                    

def texto_jugador(texto):
    """
    Muestra texto para el jugador en la ventana del juego.
    
    Esta función muestra texto para el jugador en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    wth = monospace_large.render(texto, True, BLACK)
    pygame.draw.rect(win, WHITE,
                    (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'],
                    2*TAMAÑO['tamaño_letra'], TAMAÑO['tamaño_letra']))
    win.blit(wth, (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen']))
    

def texto_ordenador(texto):
    """
    Muestra texto para el ordenador en la ventana del juego.
    
    Esta función muestra texto para el ordenador en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    wth = monospace_large.render(texto, True, RED)
    pygame.draw.rect(win, WHITE,
                    (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO'],
                    2*TAMAÑO['tamaño_letra'], TAMAÑO['tamaño_letra']))
    win.blit(wth, (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO']))

def texto_victoria(texto):
    """
    Muestra texto de victoria en la ventana del juego.
    
    Esta función muestra texto de victoria en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    x = 50
    y = TAMAÑO['ALTO_VENTANA'] - TAMAÑO['tamaño_letra']*4
    dibuja_texto_largo(texto, x, y, monospace_large, TAMAÑO['tamaño_letra'])
    
tiempo_ultima_alerta = pygame.time.get_ticks()
texto_alerta = ''

def alerta(texto):
    """
    Muestra una alerta en la ventana del juego.

    Esta función muestra una alerta en la ventana del juego y reproduce un sonido.

    Args:
        texto (str): El texto de la alerta.

    """
    pygame.mixer.music.play()
    global texto_alerta, tiempo_ultima_alerta
    tiempo_ultima_alerta = pygame.time.get_ticks()
    texto_alerta = texto

def dibuja_texto_largo(texto, x, y, font, fontsize):
    """
    Dibuja texto largo en la ventana del juego.

    Esta función toma un texto largo, lo divide en líneas y lo dibuja en la ventana del juego.

    Args:
        texto (str): El texto que se va a dibujar.
        x (int): La coordenada x de la posición de inicio del texto.
        y (int): La coordenada y de la posición de inicio del texto.
        font (pygame.font.Font): La fuente a utilizar para el texto.
        fontsize (int): El tamaño de la fuente.

    """
    lineas = texto.splitlines()
    pygame.draw.rect(win, WHITE,
                    (x, y, TAMAÑO['ANCHO_VENTANA'] - x, fontsize*len(lineas)))
    for i, l in enumerate(lineas):
        win.blit(font.render(l, True, BLACK), (x, y + fontsize*i))