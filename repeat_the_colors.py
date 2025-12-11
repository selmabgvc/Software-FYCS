import tkinter as tk
#import random
#import time

#Fenster erstellen
window = tk.Tk()
window.title("Repeat the Colors!")
window.geometry("800x600")

#Anzeige oben
anzeige = tk.Label(window, text="Watch first, repeat afterwards.", font=("Arial", 30))
anzeige.pack(pady=20)

# Frame: Position der Buttons im Fenster
button_frame = tk.Frame(window)
button_frame.pack(pady=80)

#Bilder für Buttons laden

cat = tk.PhotoImage(file="cat.png")
cat_dark = tk.PhotoImage(file="cat_geklickt.png")

cat2 = tk.PhotoImage(file="cat2.png")
cat2_dark = tk.PhotoImage(file="cat2_geklickt.png")

goose = tk.PhotoImage(file="goose.png")
goose_dark = tk.PhotoImage(file="goose_geklickt.png")

snowman = tk.PhotoImage(file="snowman.png")
snowman_dark = tk.PhotoImage(file="snowman_geklickt.png")

#Buttons erstellen

button1 = tk.Button(button_frame, image=cat, borderwidth=0)
button2 = tk.Button(button_frame, image=cat2, borderwidth=0)
button3 = tk.Button(button_frame, image=goose, borderwidth=0)
button4 = tk.Button(button_frame, image=snowman, borderwidth=0)

# Buttons in einem 2×2 Raster anordnen
button1.grid(row=0, column=0, padx=20, pady=20)
button2.grid(row=0, column=1, padx=20, pady=20)
button3.grid(row=1, column=0, padx=20, pady=20)
button4.grid(row=1, column=1, padx=20, pady=20)

# Fenster anzeigen
window.mainloop()


import os
print("Working directory:", os.getcwd())