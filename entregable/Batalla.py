import pygame
import unittest

class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[' ']*self.columnas for _ in range(self.filas)]
        self.matriz_disparos = []

    def imprimir_separador_horizontal(self):
        print("+---" * self.columnas + "+")

    def imprimir_fila_de_numeros(self):
        print("|   " + "|".join(f" {x+1} " for x in range(self.columnas)) + "|")

    def imprimir_matriz(self, deberia_mostrar_barcos, jugador):
        print(f"Este es el mar del jugador {jugador}: ")
        letra = "A"
        for y in range(self.filas):
            self.imprimir_separador_horizontal()
            print(f"| {letra} ", end="")
            for x in range(self.columnas):
                celda = self.matriz[y][x]
                valor_real = celda if deberia_mostrar_barcos or celda == ' ' else ' '
                if (x, y) in self.matriz_disparos:
                    valor_real = '-' if celda == ' ' else celda
                print(f"| {valor_real} ", end="")
            letra = chr(ord(letra) + 1)
            print("|")
        self.imprimir_separador_horizontal()
        self.imprimir_fila_de_numeros()

class Sonido:
    def __init__(self, acertado, fallado):
        self.acertado = acertado
        self.fallado = fallado

class Juego:
    def __init__(self, jugador1, jugador2, disparos_iniciales, sonidos):
        self.tablero_j1 = jugador1
        self.tablero_j2 = jugador2  
        self.sonidos = sonidos
        self.disparos_iniciales = disparos_iniciales
        self.turno = 0
        self.disparos_restantes_j1 = disparos_iniciales
        self.disparos_restantes_j2 = disparos_iniciales
        self.jugador_actual = jugador1  # Inicializar el jugador actual como jugador1

# Método estático para colocar un barco en las coordenadas dadas del tablero
    @staticmethod
    def colocar_barco(tablero, x, y):
        # Verificar que las coordenadas estén dentro de los límites del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("La columna está fuera del tablero")
        if y < 0 or y >= len(tablero):
            raise IndexError("La fila está fuera del tablero")
        # Colocar el barco en la posición dada (cambiar el valor a 1)
        tablero[y][x] = 1

    def solicitar_coordenadas(self):
        while True:
            letra_fila = input("Ingresa la letra de la fila tal y como aparece en el tablero: ")
            if len(letra_fila) != 1:
                print("Debes ingresar únicamente una letra")
                continue
            y = ord(letra_fila.upper()) - 65
            if 0 <= y < self.tablero_j1.filas:
                break
            else:
                print("Fila inválida")

        while True:
            try:
                x = int(input("Ingresa el número de columna: ")) - 1
                if 0 <= x < self.tablero_j1.columnas:
                    break
                else:
                    print("Columna inválida")
            except ValueError:
                print("Ingresa un número válido")

        return x, y

    @staticmethod
    def disparar(tablero, x, y):
        # Verificar que las coordenadas estén dentro de los límites del tablero
        if x < 0 or x >= len(tablero[0]):
            raise IndexError("Columna inválida para disparar")
        if y < 0 or y >= len(tablero):
            raise IndexError("Fila inválida para disparar")
        # Verificar si la celda ya ha sido disparada
        if tablero[y][x] == -1:
            raise Exception("No puedes disparar a una celda ya disparada")
        # Marcar la celda como disparada (cambiar el valor a -1)
        tablero[y][x] = -1

    def todos_los_barcos_hundidos(self, tablero):
        for y in range(tablero.filas):
            for x in range(tablero.columnas):
                celda = tablero.matriz[y][x]
                if celda != ' ' and celda != '*' and celda != '-':
                    return False
        return True

    def imprimir_disparos_restantes(self):
        print(f"Disparos restantes de J1: {self.disparos_restantes_j1}  -  Disparos restantes de J2: {self.disparos_restantes_j2}")

    def indicar_victoria(self):
        print(f"Fin del juego\nEl jugador 1 es el ganador" if self.jugador_actual == self.tablero_j1 else "Fin del juego\nEl jugador 2 es el ganador")

    def indicar_fracaso(self):
        print(f"Fin del juego\nEl jugador 1 pierde. Se han acabado sus disparos" if self.jugador_actual == self.tablero_j1 else "Fin del juego\nEl jugador 2 pierde. Se han acabado sus disparos")

    def jugar(self):
        self.colocar_barcos(self.tablero_j1, 5)
        self.colocar_barcos(self.tablero_j2, 5)
        print("===============")
        print("¡Comienza el juego! Jugador 1, es tu turno.")
        while True:
            print(f"Turno del jugador {self.turno + 1}")  # Imprimir el número de turno
            self.imprimir_disparos_restantes()
            tablero_oponente = self.tablero_j2 if self.jugador_actual == self.tablero_j1 else self.tablero_j1
            tablero_oponente.imprimir_matriz(False, "J1" if self.jugador_actual == self.tablero_j2 else "J2")
            x, y = self.solicitar_coordenadas()
            acertado = self.disparar(x, y, tablero_oponente)
            if not acertado:
                self.turno += 1

            tablero_oponente.imprimir_matriz(True, "J1" if self.jugador_actual == self.tablero_j2 else "J2")
            if acertado:
                print("Disparo acertado")
                if self.todos_los_barcos_hundidos(tablero_oponente):
                    self.indicar_victoria()
                    break
            else:
                print("Disparo fallado")
                if self.turno >= self.disparos_iniciales:
                    self.indicar_fracaso()
                    break
            self.jugador_actual = self.tablero_j1 if self.jugador_actual == self.tablero_j2 else self.tablero_j2

class Menu:
    @staticmethod
    def acerca_de():
        print("David y Andrés UdeM  2024/1")

    @staticmethod
    def mostrar_menu():
        pygame.init()  # Inicializar Pygame
        while True:
            eleccion = input("""
1. Jugar
2. Acerca de
3. Salir
Elige: """)
            if eleccion == "1":
                tablero_j1 = Tablero(5, 5)
                tablero_j2 = Tablero(5, 5)
                sonido_acertado = pygame.mixer.Sound(r"sonidos\acertado.wav")
                sonido_fallado = pygame.mixer.Sound(r"sonidos\fallado.wav")
                sonidos = Sonido(sonido_acertado, sonido_fallado)
                juego = Juego(tablero_j1, tablero_j2, 10, sonidos)
                juego.jugar()
            elif eleccion == "2":
                Menu.acerca_de()
            
            elif eleccion == "3":
                break
            


if __name__ == '__main__':
    
    Menu.mostrar_menu()
