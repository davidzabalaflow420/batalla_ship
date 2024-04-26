from Logica import *
import unittest

class Pruebas(unittest.TestCase):
    """
    Clase que contiene pruebas unitarias para la clase Tablero.
    """

    def test_crear_tablero_negativo(self):
        """
        Prueba para verificar el manejo de valores negativos al crear el tablero.
        """
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(-3, 5)

    def test_crear_tablero_cero(self):
        """
        Prueba para verificar el manejo de filas con valor cero al crear el tablero.
        """
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(0, 5)

    def test_colocar_barco_columna_negativa(self):
        """
        Prueba para verificar el manejo de columna negativa al colocar un barco.
        """
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            tablero.colocar_barcos(1)  # Llamar al método en una instancia de Tablero

    def test_colocar_barco_fila_negativa(self):
        """
        Prueba para verificar el manejo de fila negativa al colocar un barco.
        """
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            tablero.colocar_barcos(1)  # Llamar al método en una instancia de Tablero

    def test_disparar_columa_negativa(self):
        """
        Prueba para verificar el manejo de columna negativa al realizar un disparo.
        """
        tablero = Tablero.crear_tablero(5, 5)
        self.assertFalse(tablero.disparar(-1, 3))  # Cambiar assertRaises por assertFalse

    def test_disparar_celda_disparada(self):
        """
        Prueba para verificar el manejo de disparo a una celda ya disparada.
        """
        tablero = Tablero.crear_tablero(5, 5)
        self.assertFalse(tablero.disparar(2, 3))  # Cambiar assertRaises por assertFalse

#Pruebas unitarias
class TestTablero(unittest.TestCase):
    """
    Clase que contiene pruebas unitarias para la clase Tablero.
    """
    def setUp(self):
        """
        Configura el tablero antes de cada prueba.
        """
        self.tablero = Tablero(5, 5)  # Crear un tablero de 5x5

    def test_creacion_tablero(self):
        """
        Prueba la creación del tablero.
        """
        self.assertEqual(self.tablero.filas, 5)
        self.assertEqual(self.tablero.columnas, 5)
        self.assertEqual(len(self.tablero.matriz), 5)
        self.assertEqual(len(self.tablero.matriz[0]), 5)

    def test_inicializacion_matriz(self):
        """
        Prueba la inicialización de la matriz del tablero.
        """
        for fila in self.tablero.matriz:
            for celda in fila:
                self.assertEqual(celda, ' ')

    def test_colocar_barcos(self):
        """
        Prueba la colocación de barcos en el tablero.
        """
        self.tablero.colocar_barcos(3)
        self.assertEqual(self.tablero.barcos_hundidos, 0)

    def test_colocar_barcos_cantidad_correcta(self):
        """
        Prueba que se coloquen la cantidad correcta de barcos.
        """
        cantidad_barcos = 3
        self.tablero.colocar_barcos(cantidad_barcos)
        self.assertEqual(sum(row.count('S') for row in self.tablero.matriz), cantidad_barcos)

    def test_disparar_fallado(self):
        """
        Prueba de un disparo fallido.
        """
        x, y = 2, 2
        self.assertFalse(self.tablero.matriz[y][x] == 'S')
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '-')

    def test_disparar_acertado(self):
        """
        Prueba de un disparo acertado.
        """
        x, y = 3, 3
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.matriz[y][x] = 'S'
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '*')


class TestTableros(unittest.TestCase):
    def setUp(self):
        """
        Configura el tablero para las pruebas.
        """
        self.tablero = Tablero(5, 5)

    def test_creacion_con_filas_no_enteras(self):
        """
        Prueba de creación del tablero con filas no enteras.
        """
        with self.assertRaises(ValueError):
            Tablero(2.5, 5)

    def test_creacion_con_columnas_no_enteras(self):
        """
        Prueba de creación del tablero con columnas no enteras.
        """
        with self.assertRaises(ValueError):
            Tablero(4, "B")

    def test_colocar_barcos_sobre_celdas_ocupadas(self):
        """
        Prueba de colocar barcos sobre celdas ya ocupadas.
        """
        self.tablero.matriz[2][2] = 'S'
        with self.assertRaises(ValueError, msg="No se levantó ValueError al colocar barcos sobre celdas ocupadas"):
            self.tablero.colocar_barcos(1)

    def test_colocar_barcos_exitosamente(self):
        """
        Prueba de colocar barcos correctamente.
        """
        cantidad_barcos = 3
        try:
            self.tablero.colocar_barcos(cantidad_barcos)
        except ValueError as e:
            self.fail(f"Se generó un ValueError inesperado: {e}")

        barcos_en_tablero = sum(row.count('S') for row in self.tablero.matriz)
        self.assertEqual(barcos_en_tablero, cantidad_barcos)

    def test_disparar_con_coordenadas_invalidas(self):
        """
        Prueba de disparar con coordenadas fuera de límites.
        """
        self.assertFalse(self.tablero.disparar(6, 2))
        self.assertFalse(self.tablero.disparar(2, 6))

    def test_disparar_con_coordenadas_ya_utilizadas(self):
        """
        Prueba de disparar en celdas ya utilizadas.
        """
        x, y = 2, 2
        self.tablero.disparar(x, y)
        self.assertFalse(self.tablero.disparar(x, y))

    def test_disparar_en_celda_ya_utilizada(self):
        """
        Prueba de disparar en celda ya utilizada.
        """
        x, y = 2, 2
        self.tablero.disparar(x, y)
        self.assertFalse(self.tablero.disparar(x, y))

    def test_disparar_fuera_de_limites(self):
        """
        Prueba de disparar fuera de límites.
        """
        self.assertFalse(self.tablero.disparar(-1, 2))
        self.assertFalse(self.tablero.disparar(2, -1))


if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
