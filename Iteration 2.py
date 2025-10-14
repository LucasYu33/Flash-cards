import tkinter as tk
import random

# Difficulty levels (rows, cols)
DIFFICULTIES = {
    "Easy": (4, 4),      # 16 cards (8 pairs)
    "Medium": (8, 8),    # 64 cards (32 pairs)
    "Hard": (10, 10)     # 100 cards (50 pairs)
}

window = tk.Tk()
window.title("Flash Cards")
window.configure(bg="#F0F8FF")

# Title label
title_label = tk.Label(window, text="Flash Cards", font=("Helvetica", 18, "bold"),
                       bg="#F0F8FF", fg="#333")
title_label.grid(row=0, column=0, columnspan=10, pady=(10, 10))

# Difficulty dropdown
difficulty_var = tk.StringVar(value="Easy")
difficulty_menu = tk.OptionMenu(window, difficulty_var, *DIFFICULTIES.keys())
difficulty_menu.config(font=("Helvetica", 12))
difficulty_menu.grid(row=1, column=0, columnspan=3, pady=10)

# Start button
start_button = tk.Button(window, text="Start Game", font=("Helvetica", 12),
                         command=lambda: start_game(difficulty_var.get()))
start_button.grid(row=1, column=3, columnspan=3, pady=10)

# Move counter label
move_label = None

# Variables for game state
buttons = []
flipped = []
flipped_values = []
matched = []
moves = 0
lock = False
card_values = []
total_cards = 0
grid_rows = 0
grid_cols = 0

def start_game(difficulty):
    global card_values, total_cards, buttons, flipped, flipped_values, matched, moves
    global lock, move_label, grid_rows, grid_cols

    # Clear previous board
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) >= 2:
            widget.destroy()

    # Reset game state
    buttons = []
    flipped = []
    flipped_values = []
    matched = []
    moves = 0
    lock = False

    # Set grid size
    grid_rows, grid_cols = DIFFICULTIES[difficulty]
    total_cards = grid_rows * grid_cols
    num_pairs = total_cards // 2

    # Generate card values
    card_symbols = [chr(65 + i) for i in range(26)] + [chr(97 + i) for i in range(26)]
    card_values = (card_symbols[:num_pairs]) * 2
    random.shuffle(card_values)

    # Move counter label
    move_label = tk.Label(window, text="Moves: 0", font=("Helvetica", 12),
                          bg="#F0F8FF", fg="black")
    move_label.grid(row=2, column=0, columnspan=grid_cols, pady=(0, 10))

    # Create card buttons
    for i in range(total_cards):
        btn = tk.Button(window, text=" ", width=6, height=3,
                        bg="#87CEFA", font=("Helvetica", 12, "bold"),
                        command=lambda idx=i: on_card_click(idx))
        row = (i // grid_cols) + 3
        col = i % grid_cols
        btn.grid(row=row, column=col, padx=3, pady=3)
        buttons.append(btn)

    # Restart button
    restart_btn = tk.Button(window, text="Restart", font=("Helvetica", 12),
                            bg="#D3D3D3", command=lambda: start_game(difficulty))
    restart_btn.grid(row=grid_rows + 4, column=0, columnspan=grid_cols, pady=(10, 0))

def on_card_click(index):
    global lock
    if lock:
        return

    button = buttons[index]
    value = card_values[index]

    if button in matched or button in flipped:
        return

    button.config(text=value, bg="#FFD700")
    flipped.append(button)
    flipped_values.append(value)

    # Check match if two cards are flipped
    if len(flipped) == 2:
        lock = True
        window.after(800, check_match)

def check_match():
    global flipped, flipped_values, matched, lock, moves

    moves += 1
    if move_label:
        move_label.config(text=f"Moves: {moves}")

    if flipped_values[0] == flipped_values[1]:
        for b in flipped:
            b.config(bg="#98FB98")  # Green for matched cards
        matched.extend(flipped)
    else:
        for b in flipped:
            b.config(text=" ", bg="#87CEFA")  # Reset cards if no match

    flipped = []
    flipped_values = []
    lock = False

    # Check if all cards are matched
    if len(matched) == total_cards:
        show_win_message()

def show_win_message():
    win_label = tk.Label(window, text="🎉 You Won! 🎉", font=("Helvetica", 16, "bold"),
                         bg="#F0F8FF", fg="green")
    win_label.grid(row=grid_rows + 5, column=0, columnspan=grid_cols, pady=10)

# Start the game
window.mainloop()
