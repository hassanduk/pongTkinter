Explicación del Código:

Interfaz Gráfica :

El juego utiliza un Canvas de tkinter como área de dibujo.
El fondo es negro, las paletas y la pelota son blancas.

Control de Movimiento :

Las paletas se mueven con las teclas W/S para el jugador izquierdo y ↑/↓ para el jugador derecho.
La pelota rebota en los bordes y en las paletas.

Pausa y Menú:

Al presionar Esc, el juego se pausa y muestra un menú con opciones para reiniciar o salir.
El menú se implementa con una ventana emergente (Toplevel).

Marcador :

El marcador se actualiza automáticamente cuando un jugador anota un gol.
Usa una fuente "pixelada" para darle un estilo retro.

Reinicio del Juego :

Al reiniciar, el marcador vuelve a cero y la pelota regresa al centro.