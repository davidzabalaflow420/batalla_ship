from  configuracion import lado
from texto import alerta
from idiomas.es import * 

def trasponer(tablero):
    """
    Transpone una matriz/tablero dado.
    
    Esta función toma una matriz/tablero como entrada y devuelve su transpuesta.
    
    Args:
        tablero (list): La matriz/tablero a transponer.
        
    Returns:
        list: La transpuesta del tablero.
    """
    lado = len(tablero)
    tablero_tras = [[' ']*lado for _ in range(lado)]  # Crear una matriz/tablero vacío con las dimensiones transpuestas
    for i in range(lado):
        for j in range(lado):
            tablero_tras[i][j] = tablero[j][i]  # Copiar los elementos de la matriz original en su posición transpuesta
    return tablero_tras

def pprint(tablero):
    """
    Imprime un tablero de juego de manera legible.
    
    Esta función toma un tablero de juego como entrada y lo imprime en la consola, organizando las filas y columnas de manera legible.
    
    Args:
        tablero (list): El tablero de juego a imprimir.
    """
    tablero_tras = trasponer(tablero)  # Transponer el tablero para imprimir las columnas como filas
    for fila in tablero_tras:
        print(fila)
        

def disparo(tablero, x, y):
    """
    Realiza un disparo en una posición específica del tablero.
    
    Esta función simula un disparo en una posición específica del tablero y actualiza el tablero en consecuencia.
    
    Args:
        tablero (list): El tablero donde se realizará el disparo.
        x (int): La coordenada x del disparo.
        y (int): La coordenada y del disparo.
        
    Returns:
        list: El tablero actualizado después del disparo.
    """
    elemento_antiguo = tablero[x][y]
    if elemento_antiguo in ' .':
        elemento_nuevo = 'O'
    elif elemento_antiguo == 'B':
        elemento_nuevo = 'X'
        # Marcar espacios alrededor del barco como 'agua'
        if x > 0 and y > 0 and tablero[x-1][y-1] == ' ':
            tablero[x-1][y-1] = '.'
        if x > 0 and y < lado - 1 and tablero[x-1][y+1] == ' ':
            tablero[x-1][y+1] = '.'
        if x < lado - 1 and y > 0 and tablero[x+1][y-1] == ' ':
            tablero[x+1][y-1] = '.'
        if x < lado - 1 and y < lado - 1 and tablero[x+1][y+1] == ' ':
            tablero[x+1][y+1] = '.'
    else:
        elemento_nuevo = elemento_antiguo
    tablero[x][y] = elemento_nuevo
    return tablero

def ha_terminado(tablero):
    """
    Verifica si todos los barcos han sido hundidos en el tablero.
    
    Args:
        tablero (list): El tablero a verificar.
        
    Returns:
        bool: True si todos los barcos han sido hundidos, False en caso contrario.
    """
    for linea in tablero:
        for elemento in linea:
            if elemento == 'B':
                return False
    return True


def tablero_vacio():
    """
    Crea un tablero vacío lleno de espacios en blanco.
    
    Returns:
        list: Tablero vacío.
    """
    return [[' ']*lado for _ in range(lado)]

def vecinos_de(x, y):
    """
    Encuentra los vecinos de una posición en el tablero.
    
    Esta función devuelve una lista de las posiciones vecinas (arriba, abajo, izquierda, derecha) de una posición dada en el tablero.
    
    Args:
        x (int): La coordenada x de la posición.
        y (int): La coordenada y de la posición.
        
    Returns:
        list: Una lista de tuplas que representan las posiciones de los vecinos.
    """
    vecinos = []
    if x > 0:
        vecinos.append((x - 1, y))
    if x < lado - 1:
        vecinos.append((x + 1, y))
    if y > 0:
        vecinos.append((x, y - 1))
    if y < lado - 1:
        vecinos.append((x, y + 1))
    return vecinos

def algun_vecino_es_X(tablero, x, y):
    """
    Comprueba si alguno de los vecinos de una posición contiene una 'X'.
    
    Esta función verifica si alguno de los vecinos de una posición dada en el tablero contiene una 'X'.
    
    Args:
        tablero (list): El tablero donde se realizará la búsqueda.
        x (int): La coordenada x de la posición.
        y (int): La coordenada y de la posición.
        
    Returns:
        bool: True si alguno de los vecinos contiene una 'X', False en caso contrario.
    """
    vecinos = vecinos_de(x, y)
    return any(tablero[x_vecino][y_vecino] == 'X'
            for (x_vecino, y_vecino) in vecinos)

def comprueba_hundido(tablero, posiciones_barcos, x, y):
    """
    Comprueba si un disparo ha hundido un barco en el tablero.
    
    Args:
        tablero (list): El tablero donde se ha realizado el disparo.
        posiciones_barcos (dict): Un diccionario que mapea índices de barcos a sus posiciones en el tablero.
        x (int): Coordenada x del disparo.
        y (int): Coordenada y del disparo.
        
    Returns:
        bool: True si el disparo ha hundido un barco, False en caso contrario.
    """
    if tablero[x][y] != 'B':
        return False
    if not algun_vecino_es_X(tablero, x, y):
        return False
    for j, posiciones_barco in posiciones_barcos.items():
        if any((xbarco == x) and (ybarco == y)
            for xbarco, ybarco in posiciones_barco):
            # Estoy disparando al barco j
            daño = sum(1 for xbarco, ybarco in posiciones_barco
                    if tablero[xbarco][ybarco] == 'X')
            largo = len(posiciones_barco)
            if daño == largo - 1:
                x_primer, y_primer = posiciones_barco[0]
                x_ultima, y_ultima = posiciones_barco[-1]
                if x_primer == x_ultima:
                    # Vertical
                    # Primera casilla
                    x = x_primer
                    y = y_primer - 1
                    if y >= 0 and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                    # Última casilla
                    x = x_primer
                    y = y_ultima + 1
                    if y < lado and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                else:
                    # Horizontal
                    # Primera casilla
                    x = x_primer - 1
                    y = y_primer
                    if x >= 0 and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                    # Última casilla
                    x = x_ultima + 1
                    y = y_ultima
                    if x < lado and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                alerta(texto_alerta_hundido)
                return True

