
def traducir_coordenadas(disparo):
    """
    Traduce una coordenada de disparo de su formato de entrada a coordenadas de tablero.
    
    Args:
        disparo (str): Coordenada de disparo en formato alfanumérico, por ejemplo 'A1'.
        
    Returns:
        tuple: Coordenadas x, y en formato de tablero (0-indexed).
    """
    if len(disparo) < 2:
        return -1, -1
    letra, numero = disparo[:2]
    x = ord(numero) - ord('1')
    y = ord(letra.upper()) - ord('A')
    return x, y

def traducir_coordenadas_al_reves(x, y):
    """
    Traduce coordenadas de tablero a su formato de disparo alfanumérico.
    
    Args:
        x (int): Coordenada x en formato de tablero.
        y (int): Coordenada y en formato de tablero.
        
    Returns:
        str: Coordenada de disparo en formato alfanumérico, por ejemplo 'A1'.
    """
    numero = str(x + 1)
    letra = chr(ord('A') + y)
    disparo = letra + numero
    return disparo