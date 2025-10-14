import tkinter as tk
import random

# Sets up the main window
window = tk.Tk()
window.title("Memory Game")

# Creates and shuffle the cards
cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D',
         'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']
random.shuffle(cards)


buttons = []          # Stores all the buttons
flipped = []          # Stores flipped buttons
flipped_values = []   # Stores the values of flipped cards
matched = []          # Stores matched buttons

# Functions that runs when a card is clicked
def on_card_click(index):
    button = buttons[index]
    value = cards[index]

    # The code ignores it if already matched or flipped
    if button in matched or button in flipped:
        return
    
    button.config(text=value)
    flipped.append(button)
    flipped_values.append(value)

    # The code checks it for match if two cards are flipped
    if len(flipped) == 2:
        window.after(1000, check_match)

# The code checks it if the two flipped cards match
def check_match():
    global flipped, flipped_values

    if flipped_values[0] == flipped_values[1]:
        matched.extend(flipped)
    else:
        for button in flipped:
            button.config(text=" ")

    flipped = []
    flipped_values = []

# Creates a button and place it in the grid
def make_button(index):
    button = tk.Button(window, text=" ", width=6, height=3,
                       command=lambda idx=index: on_card_click(idx))
    button.grid(row=index // 4, column=index % 4, padx=5, pady=5)
    buttons.append(button)

# Creates all 16 buttons
for i in range(16):
    make_button(i)

window.mainloop()
