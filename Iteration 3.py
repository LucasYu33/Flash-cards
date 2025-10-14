import tkinter as tk
from tkinter import messagebox
import random, time

DIFFICULTIES = {"Easy": (4, 4), "Medium": (6, 6), "Hard": (8, 8)}

window = tk.Tk()
window.title("Memory Match Game")
window.configure(bg="#F0F8FF")

buttons, flipped, matched = [], [], []
moves, lock, running, start_time = 0, False, False, 0
player = ""

tk.Label(window, text="Memory Match Game", font=("Helvetica", 18, "bold"), bg="#F0F8FF").pack(pady=5)
top_frame = tk.Frame(window, bg="#F0F8FF")
top_frame.pack()

tk.Label(top_frame, text="Name:", bg="#F0F8FF").grid(row=0, column=0)
name_entry = tk.Entry(top_frame)
name_entry.grid(row=0, column=1)

diff = tk.StringVar(value="Easy")
tk.OptionMenu(top_frame, diff, *DIFFICULTIES).grid(row=0, column=2)
tk.Button(top_frame, text="Start", command=lambda: start_game()).grid(row=0, column=3)
timer_lbl = tk.Label(top_frame, bg="#F0F8FF"); timer_lbl.grid(row=0, column=4)
moves_lbl = tk.Label(top_frame, bg="#F0F8FF"); moves_lbl.grid(row=0, column=5)

frame = tk.Frame(window, bg="#000000")
frame.pack(padx=10, pady=10)

def start_game():
    global buttons, flipped, matched, moves, lock, running, start_time, player, cards
    for w in frame.winfo_children():
        w.destroy()
    buttons.clear(); flipped.clear(); matched.clear()
    moves, lock, running = 0, False, True
    start_time = time.time()
    player = name_entry.get().strip() or "Player"
    r, c = DIFFICULTIES[diff.get()]
    total = r * c
    syms = [chr(i) for i in range(65, 91)]  # A–Z
    pool = (syms * ((total // len(syms)) + 1))[: total // 2]  # repeat alphabet if needed
    cards = pool * 2
    random.shuffle(cards)

    moves_lbl.config(text=f"{player}'s Moves: 0")
    update_timer()

    btn_size = 60 if r <= 4 else 45 if r == 6 else 35
    for i in range(total):
        b = tk.Button(
            frame, text=" ", bg="#87CEFA", font=("Helvetica", 10, "bold"),
            command=lambda i=i: flip(i),
            bd=1, relief="solid", highlightthickness=0
        )
        x, y = (i % c) * btn_size, (i // c) * btn_size
        b.place(x=x, y=y, width=btn_size, height=btn_size)
        buttons.append(b)

    frame.config(width=c * btn_size, height=r * btn_size)
    tk.Button(window, text="Restart", command=start_game, bd=1).pack(pady=5)

def flip(i):
    global lock
    if lock or not running or buttons[i] in matched or buttons[i] in flipped: return
    buttons[i].config(text=cards[i], bg="#FFD700")
    flipped.append(buttons[i])
    if len(flipped) == 2:
        lock = True; window.after(600, check)

def check():
    global flipped, matched, moves, lock
    moves += 1
    moves_lbl.config(text=f"{player}'s Moves: {moves}")
    if flipped[0]['text'] == flipped[1]['text']:
        for b in flipped: b.config(bg="#98FB98"); matched.append(b)
    else:
        for b in flipped: b.config(text=" ", bg="#87CEFA")
    flipped.clear(); lock = False
    if len(matched) == len(buttons): win()

def win():
    global running
    running = False
    t = int(time.time() - start_time)
    messagebox.showinfo("You Win!", f"🎉 {player}, you won in {moves} moves and {t}s!")

def update_timer():
    if running:
        timer_lbl.config(text=f"Time: {int(time.time() - start_time)}s")
        window.after(1000, update_timer)

window.resizable(False, False)
window.eval('tk::PlaceWindow . center')
window.mainloop()
