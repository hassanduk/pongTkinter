import tkinter as tk
from tkinter import messagebox

# Configuración inicial del juego
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
SPEED = 2
BALL_SPEED_X, BALL_SPEED_Y = 4, 4
PAUSE = False

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Game")
        self.root.resizable(False, False)

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Marcador (Scoreboard)
        self.score_left = 0
        self.score_right = 0
        self.score_board = self.canvas.create_text(
            WIDTH // 2, 30, text=f"{self.score_left} : {self.score_right}",
            font=("Pixelated", 24), fill="white"
        )

        # Paletas
        self.paddle_left = self.canvas.create_rectangle(
            20, HEIGHT // 2 - PADDLE_HEIGHT // 2,
            20 + PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2,
            fill="white"
        )
        self.paddle_right = self.canvas.create_rectangle(
            WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2,
            WIDTH - 20, HEIGHT // 2 + PADDLE_HEIGHT // 2,
            fill="white"
        )

        # Pelota
        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
            WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS,
            fill="white"
        )

        # Variables de movimiento
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y
        self.left_paddle_dy = 2
        self.right_paddle_dy = 2

        # Eventos de teclado
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        # Iniciar el juego
        self.game_loop()

    def key_press(self, event):
        """Maneja las teclas presionadas."""
        if event.keysym == "w":
            self.left_paddle_dy = -SPEED
        elif event.keysym == "s":
            self.left_paddle_dy = SPEED
        elif event.keysym == "Up":
            self.right_paddle_dy = -SPEED
        elif event.keysym == "Down":
            self.right_paddle_dy = SPEED
        elif event.keysym == "Escape":
            self.toggle_pause()

    def key_release(self, event):
        """Maneja las teclas liberadas."""
        if event.keysym in ("w", "s"):
            self.left_paddle_dy = 0
        elif event.keysym in ("Up", "Down"):
            self.right_paddle_dy = 0

    def toggle_pause(self):
        """Activa o desactiva la pausa."""
        global PAUSE
        PAUSE = not PAUSE
        if PAUSE:
            self.show_pause_menu()
        else:
            self.hide_pause_menu()

    def show_pause_menu(self):
        """Muestra el menú de pausa."""
        self.pause_menu = tk.Toplevel(self.root)
        self.pause_menu.title("Pause Menu")
        self.pause_menu.geometry("200x100")
        self.pause_menu.resizable(False, False)

        reset_button = tk.Button(self.pause_menu, text="Reset", command=self.reset_game)
        reset_button.pack(pady=10)

        quit_button = tk.Button(self.pause_menu, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)

    def hide_pause_menu(self):
        """Oculta el menú de pausa."""
        if hasattr(self, "pause_menu"):
            self.pause_menu.destroy()

    def reset_game(self):
        """Reinicia el juego."""
        global PAUSE
        PAUSE = False
        self.hide_pause_menu()
        self.score_left = 0
        self.score_right = 0
        self.canvas.itemconfig(self.score_board, text=f"{self.score_left} : {self.score_right}")
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
                           WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS)
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y

    def game_loop(self):
        """Bucle principal del juego."""
        if not PAUSE:
            # Mover paletas
            self.move_paddles()

            # Mover pelota
            self.move_ball()

            # Detectar colisiones
            self.check_collisions()

        # Actualizar el canvas
        self.root.after(16, self.game_loop)

    def move_paddles(self):
        """Mueve las paletas."""
        self.canvas.move(self.paddle_left, 0, self.left_paddle_dy)
        self.canvas.move(self.paddle_right, 0, self.right_paddle_dy)

        # Limitar movimiento dentro del canvas
        for paddle in (self.paddle_left, self.paddle_right):
            coords = self.canvas.coords(paddle)
            if coords[1] < 0:
                self.canvas.move(paddle, 0, -coords[1])
            elif coords[3] > HEIGHT:
                self.canvas.move(paddle, 0, HEIGHT - coords[3])

    def move_ball(self):
        """Mueve la pelota."""
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

    def check_collisions(self):
        """Detecta colisiones y actualiza el marcador."""
        ball_coords = self.canvas.coords(self.ball)

        # Colisión con bordes superior e inferior
        if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
            self.ball_dy = -self.ball_dy

        # Colisión con paleta izquierda
        paddle_left_coords = self.canvas.coords(self.paddle_left)
        if (ball_coords[0] <= paddle_left_coords[2] and
                paddle_left_coords[1] <= ball_coords[3] and
                paddle_left_coords[3] >= ball_coords[1]):
            self.ball_dx = -self.ball_dx

        # Colisión con paleta derecha
        paddle_right_coords = self.canvas.coords(self.paddle_right)
        if (ball_coords[2] >= paddle_right_coords[0] and
                paddle_right_coords[1] <= ball_coords[3] and
                paddle_right_coords[3] >= ball_coords[1]):
            self.ball_dx = -self.ball_dx

        # Gol anotado por el jugador izquierdo
        if ball_coords[0] <= 0:
            self.score_right += 1
            self.update_score()
            self.reset_ball()

        # Gol anotado por el jugador derecho
        if ball_coords[2] >= WIDTH:
            self.score_left += 1
            self.update_score()
            self.reset_ball()


    def update_score(self):
        """Actualiza el marcador."""
        self.canvas.itemconfig(self.score_board, text=f"{self.score_left} : {self.score_right}")

    def reset_ball(self):
        """Reinicia la posición de la pelota."""
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
                           WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS)
        self.ball_dx = -self.ball_dx

if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()