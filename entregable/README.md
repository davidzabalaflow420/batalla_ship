# batalla_naval_python:
 Batalla naval programada en Python
## Quien lo hizo: 
    David Zabala y Andrés Arango
## Que es y para que:
    Juego de Batalla Naval para divertirse y ganar la materia
## Como lo hago funcionar:
  Interfáz gráfica: Para correr el juego de BattleShip por interfaz lo primero que debes hacer es descargar "entregable" que es la carpeta que contiene los archivos del juego. Una vez descargada en instalada en tu PC debes abrir el programa en un IDE de python (En este caso VScode). Abres la terminal de VScode (https://code.visualstudio.com/docs) y una vez se inicie el terminal debes escribir la sentencia "python jugar.py" para que el juego inicie. Debes tener en cuenta que el juego aún no tiene base de datos por lo que deberás cambiar la ruta del path de los sonidos utilizados, éste cambio lo realizas yendo a la carpeta "sonidos" dentro del IDE y dando click derecho en "morse-code-alphabet.ogg", le das click e la opción "copy relative path" y la pegas en ésta parte del archivo constants.py: 
                                                                                    "pygame.mixer.music.load('sonidos\morse-code-alphabet.ogg')"

Consola: Para correr el Juego de Battleship por consola lo primero que debes hacer es descargar "entregable" que es la carpeta que contiene los archivos del juego. Una vez descargada en instalada en tu PC debes abrir el programa en un IDE de python (En este caso VScode). Abres la terminal de VScode (https://code.visualstudio.com/docs) y una vez se inicie el terminal debes escribir la sentencia "python Batalla.py" para que el juego por consola inicie. Debes tener en cuenta que el juego aún no tiene base de datos por lo que deberás cambiar la ruta del path de los sonidos utilizados, éste cambio lo realizas yendo a la carpeta "sonidos" dentro del IDE y dando click derecho en "sonidos\fallado.wav y sonidos\acertado.wav", les das click e la opción "copy relative path" y las pegas en ésta parte del archivo Sonidos.py:
                                                                                        # Rutas de los archivos de sonido
                                                                                            ruta_acertado = r"sonidos\acertado.wav"
                                                                                            ruta_fallado = r"sonidos\fallado.wav"

Para correr las pruebas unitarias:Lo primero que debes hacer es abrir el terminal y usar el comando "cd Test" para trasladarte a la carpeta donde se encuentran las pruebas unitarias. Para ejecutarlos debes usar el comando "python Test.py".


## Como está hecho:
    Archivos Principales:

    Main.py: Este archivo es el punto de entrada de la aplicación. Se encarga de iniciar el juego creando una instancia de la clase Main y llamando al método iniciar().
    Menu.py: Contiene la clase Menu, que muestra el menú principal del juego y maneja las opciones seleccionadas por el usuario, como jugar, ver información acerca de los desarrolladores o salir del juego.
    Juego.py: Define la clase Juego, que gestiona la lógica del juego. Controla los turnos, la mecánica de disparo, las condiciones de victoria y derrota, y realiza las interacciones entre los tableros y los jugadores.
    Tablero.py: Contiene la clase Tablero, que representa el tablero de juego. Se encarga de manejar la colocación de barcos, verificar si los barcos están hundidos y imprimir el estado del tablero en la consola.
    Sonido.py: Define la clase Sonido, que gestiona los sonidos del juego. Carga archivos de sonido para indicar aciertos y fallos en los disparos.
    Clases y Funcionalidades:

    Menu: Proporciona métodos estáticos para mostrar el menú principal del juego y la información acerca de los desarrolladores. También maneja la lógica para iniciar el juego o salir del programa.
    Juego: Controla el flujo del juego, gestionando los turnos de los jugadores, la interacción con los tableros, los disparos y las condiciones de victoria o derrota.
    Tablero: Representa el tablero de juego donde se colocan los barcos y se realizan los disparos. Maneja la colocación de barcos, verifica si todos los barcos están hundidos y muestra el estado del tablero en la consola.
    Sonido: Administra los archivos de sonido del juego para indicar aciertos y fallos en los disparos.
    Interacción con el Usuario:

    El usuario interactúa con el juego a través de la consola, donde se muestran los mensajes y opciones del menú.
    Se utilizan entradas de teclado para seleccionar opciones del menú y para ingresar las coordenadas de los disparos durante el juego.
    Implementación de la Lógica del Juego:

    La lógica del juego se implementa principalmente en la clase Juego, donde se controlan los turnos, los disparos, la colocación de barcos y las condiciones de victoria o derrota.
    Se utilizan métodos y atributos en las clases Tablero y Juego para realizar las interacciones necesarias durante el juego, como la colocación de barcos, la verificación de disparos acertados y la actualización del estado del tablero.

## Estrucutra sugerida:
POO y SOLID
    
