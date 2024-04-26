from configuracion import lado
from random import randint, choice
from fun_Auxi import algun_vecino_es_X
from utilidades import traducir_coordenadas_al_reves



def disparo_ordenador_tonto(tablero):
    """
    Esta función realiza un disparo aleatorio por parte del ordenador en un tablero.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    x = randint(0, lado - 1)  # Se elige una coordenada x aleatoria dentro del rango del tablero
    y = randint(0, lado - 1)  # Se elige una coordenada y aleatoria dentro del rango del tablero
    print('El ordenador dispara:', traducir_coordenadas_al_reves(x, y))  # Se muestra el disparo realizado
    if tablero[x][y] == ' ':  # Si la casilla elegida está vacía, es decir, no ha sido atacada
        print('El ordenador dispara:', traducir_coordenadas_al_reves(x, y))  # Se muestra el disparo realizado
    else:
        print('Aquí ya he disparado, mejor vuelvo a lanzar los dados')  # Si la casilla ya ha sido atacada, se indica
        x, y = disparo_ordenador_tonto(tablero)  # Se vuelve a llamar a la función para elegir otra casilla
    return x, y
    



def disparo_ordenador_menos_tonto(tablero):
    """
    Esta función realiza un disparo aleatorio por parte del ordenador en un tablero,
    evitando disparar en casillas que ya han sido atacadas.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    x = randint(0, lado - 1)  # Se elige una coordenada x aleatoria dentro del rango del tablero
    y = randint(0, lado - 1)  # Se elige una coordenada y aleatoria dentro del rango del tablero
    
    # Puede ser desconocido o barco
    if tablero[x][y] == ' ':  # Si la casilla elegida está vacía, es decir, no ha sido atacada
        print('El ordenador dispara:', traducir_coordenadas_al_reves(x, y))  # Se muestra el disparo realizado
    else:
        print('Aquí ya he disparado, mejor vuelvo a lanzar los dados')  # Si la casilla ya ha sido atacada, se indica
        x, y = disparo_ordenador_menos_tonto(tablero)  # Se vuelve a llamar a la función para elegir otra casilla
    return x, y



def disparo_ordenador_medio_listo(tablero):
    """
    Esta función realiza un disparo por parte del ordenador en un tablero, dando prioridad
    a las casillas vecinas de las casillas que contienen un barco conocido.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    # Se generan las casillas prioritarias, que son aquellas vacías y tienen al menos un vecino con un barco conocido
    casillas_prioritarias = [
        (x, y) for x in range(lado)  # Se recorren todas las coordenadas x del tablero
            for y in range(lado)  # Se recorren todas las coordenadas y del tablero
        if (tablero[x][y] == ' ') and algun_vecino_es_X(tablero, x, y)  # Si la casilla está vacía y tiene al menos un vecino con un barco conocido
    ]
    
    if len(casillas_prioritarias) > 0:  # Si hay casillas prioritarias disponibles
        x, y = choice(casillas_prioritarias)  # Se elige una de forma aleatoria
    else:
        x, y = disparo_ordenador_menos_tonto(tablero)  # Si no hay casillas prioritarias, se procede como en la función menos tonta
    return x, y
