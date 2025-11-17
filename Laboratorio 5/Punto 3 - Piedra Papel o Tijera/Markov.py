import tkinter as tk
from tkinter import font
import random
import time

# ------------------------------
class MarkovRPS:
    def __init__(self):
        self.chain = {} 

    def update(self, last_two, new_move):
        if last_two not in self.chain:
            self.chain[last_two] = {}
        if new_move not in self.chain[last_two]:
            self.chain[last_two][new_move] = 0
        self.chain[last_two][new_move] += 1

    def predict(self, last_two):
        if last_two not in self.chain:
            return random.choice(["Piedra", "Papel", "Tijeras"])
        options = self.chain[last_two]
        return max(options, key=options.get)

    def counter_move(self, move):
        if move == "Piedra":
            return "Papel"
        if move == "Papel":
            return "Tijeras"
        return "Piedra"


# ------------------------------------------
# Animaciones
# ------------------------------------------

class RPS_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Piedra · Papel · Tijeras ")

        self.bg = "#f8f4fc"
        self.card = "#ffffff"
        self.accent = "#8b5cf6"

        self.root.configure(bg=self.bg)

       
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.stats_font = font.Font(family="Helvetica", size=14, weight="bold")

      
        self.markov = MarkovRPS()
        self.player_history = []

       
        self.wins = 0
        self.losses = 0
        self.ties = 0

        self.frame = tk.Frame(self.root, bg=self.bg)
        self.frame.pack(pady=40)

        self.title = tk.Label(self.frame, text="Piedra · Papel · Tijera",
                              font=self.title_font, bg=self.bg, fg="#333")
        self.title.pack(pady=10)


        self.canvas = tk.Canvas(self.frame, width=400, height=220,
                                bg=self.card, highlightthickness=0)
        self.canvas.pack(pady=20)

        # Estadísticas
        self.stats_label = tk.Label(self.frame, text="Victorias: 0   Derrotas: 0   Empates: 0",
                                    font=self.stats_font, bg=self.bg, fg="#333")
        self.stats_label.pack(pady=10)

        # Botones de elecciones
        self.buttons_frame = tk.Frame(self.frame, bg=self.bg)
        self.buttons_frame.pack()

        self.Piedra_btn = tk.Button(self.buttons_frame, text="🪨 Piedra",
                                  font=self.button_font, bg=self.accent, fg="white",
                                  width=10, command=lambda: self.play("Piedra"))
        self.Piedra_btn.grid(row=0, column=0, padx=10)

        self.Papel_btn = tk.Button(self.buttons_frame, text="📄 Papel",
                                   font=self.button_font, bg=self.accent, fg="white",
                                   width=10, command=lambda: self.play("Papel"))
        self.Papel_btn.grid(row=0, column=1, padx=10)

        self.Tijeras_btn = tk.Button(self.buttons_frame, text="✂️ Tijera",
                                      font=self.button_font, bg=self.accent, fg="white",
                                      width=10, command=lambda: self.play("Tijeras"))
        self.Tijeras_btn.grid(row=0, column=2, padx=10)

        # Botón Jugar de nuevo
        self.retry_btn = tk.Button(self.frame, text="🔄 Jugar de nuevo",
                                   font=self.button_font, bg="#10b981",
                                   fg="white", width=15, command=self.reset_game)
        self.retry_btn.pack(pady=10)
        self.retry_btn.pack_forget()

    def animate_text(self, text, y, delay=40):
        self.canvas.delete("text")
        x = 200
        for i in range(len(text)):
            self.canvas.delete("text")
            self.canvas.create_text(
                x, y,
                text=text[:i+1],
                font=("Helvetica", 26, "bold"),
                fill=self.accent,
                tags="text"
            )
            self.canvas.update()
            time.sleep(delay / 1000)

    def play(self, player_move):

        # Markov
        if len(self.player_history) < 2:
            ai_move = random.choice(["Piedra", "Papel", "Tijeras"])
        else:
            last_two = tuple(self.player_history[-2:])
            predicted = self.markov.predict(last_two)
            ai_move = self.markov.counter_move(predicted)

        # Actualizar modelo
        if len(self.player_history) >= 2:
            self.markov.update(tuple(self.player_history[-2:]), player_move)

        self.player_history.append(player_move)

        # 2. Determinar ganador
        result = self.get_result(player_move, ai_move)

        # Actualizar stats
        if result == "🏆 ¡Ganaste!":
            self.wins += 1
        elif result == "💀 Perdiste":
            self.losses += 1
        else:
            self.ties += 1

        self.update_stats()

        # Animación
        self.animate_text(f"Tú: {player_move}", 60)
        time.sleep(0.25)
        self.animate_text(f"IA: {ai_move}", 110)
        time.sleep(0.3)
        self.animate_text(result, 160)

        # Botón Jugar de nuevo
        self.retry_btn.pack()

    # ---------------------------
    # Reset
    # ---------------------------
    def reset_game(self):
        # 1. Limpiar animación
        self.canvas.delete("all")

        # 2. Resetear estadísticas del jugador
        self.wins = 0
        self.losses = 0
        self.ties = 0

        # 3. Actualizar visualmente las estadísticas
        self.stats_label.config(
            text=f"Victorias: {self.wins}   Derrotas: {self.losses}   Empates: {self.ties}"
        )
        self.stats_label.update()  # <<< Fuerza el refresco en pantalla

        # 4. Resetear historial de movimientos del jugador
        self.player_history = []

        # 5. Resetear modelo Markov (borrar memoria)
        self.markov.chain = {}

        # 6. Restaurar texto inicial
        self.animate_text("Elige tu jugada…", 120)

        # 7. Ocultar botón "Jugar de Nuevo"
        self.retry_btn.pack_forget()

    # ---------------------------
    # Actualizar estadísticas
    # ---------------------------
    def update_stats(self):
        self.stats_label.config(
            text=f"Victorias: {self.wins}   Derrotas: {self.losses}   Empates: {self.ties}"
        )

    def get_result(self, p, ai):
        if p == ai:
            return "🤝 Empate"
        if (p == "Piedra" and ai == "Tijeras") or \
           (p == "Papel" and ai == "Piedra") or \
           (p == "Tijeras" and ai == "Papel"):
            return "🏆 ¡Ganaste!"
        return "💀 Perdiste"

root = tk.Tk()
gui = RPS_GUI(root)
gui.animate_text("Elige tu jugada…", 120)
root.mainloop()
