import tkinter as tk
import random

# ------------------- CONFIGURATION -------------------
# Define different difficulty levels
DIFFICULTIES = {
    "Easy": 4,     # 4 pairs = 8 cards
    "Medium": 6,   # 6 pairs = 12 cards
    "Hard": 8      # 8 pairs = 16 cards
}

# Choose difficulty (can change this later to a dropdown)
current_difficulty = "Hard"
num_pairs = DIFFICULTIES[current_difficulty]
grid_cols = 4  # You can calculate this based on difficulty too
grid_rows = (num_pairs * 2) // grid_cols
card_values = [chr(65 + i) for i in range(num_pairs)] * 2  # ['A', 'A', 'B', 'B', ...]

# Shuffle the cards
random.shuffle(card_values)

# ------------------- MAIN WINDOW SETUP -------------------
window = tk.Tk()
window.title("Memory Match Game")
window.configure(bg="#F0F8FF")  # Light blue background

# ------------------- UI ELEMENTS -------------------
# Title Label
title_label = tk.Label(window, text="Memory Match Game", font=("Helvetica", 18, "bold"), bg="#F0F8FF", fg="#333")
title_label.grid(row=0, column=0, columnspan=grid_cols, pady=(10, 20))

# Moves label
moves = 0
move_label = tk.Label(window, text=f"Moves: {moves}", font=("Helvetica", 12), bg="#F0F8FF")
move_label.grid(row=1, column=0, columnspan=grid_cols)

# ------------------- GAME STATE VARIABLES -------------------
buttons = []          # List of all button widgets
flipped = []          # Buttons that are currently flipped
flipped_values = []   # Their corresponding values
matched = []          # Buttons that have been matched
lock = False          # Lock to prevent clicking while checking match

# ------------------- GAME LOGIC -------------------

# Handle card click
def on_card_click(index):
    global lock
    if lock:
        return

    button = buttons[index]
    value = card_values[index]

    # Don't allow flipping matched or already flipped cards
    if button in matched or button in flipped:
        return

    button.config(text=value, bg="#FFD700")  # Show value with yellow background
    flipped.append(button)
    flipped_values.append(value)

    if len(flipped) == 2:
        lock = True
        window.after(1000, check_match)

# Check for a match after 2 cards are flipped
def check_match():
    global flipped, flipped_values, mat_
