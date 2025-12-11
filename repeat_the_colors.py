import tkinter as tk
from PIL import Image, ImageTk
import random
#import time

#Fenster erstellen
window = tk.Tk()
window.title("Repeat the Colors!")
window.geometry("1000x800")

#Anzeige oben
anzeige = tk.Label(window, text="Watch first, repeat afterwards.", font=("Arial", 30))
anzeige.pack(pady=20)

# Frame: Position der Buttons im Fenster
button_frame = tk.Frame(window)
button_frame.pack(pady=80)

#Bilder für Buttons laden

# Bild-Lade-Funktion mit skalierung
def load_image(path, size=(150, 150)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Bilder laden 
cat = load_image("cat.gif")
cat_dark = load_image("cat_geklickt.gif")

cat2 = load_image("cat2.gif")
cat2_dark = load_image("cat2_geklickt.gif")

goose = load_image("goose.gif")
goose_dark = load_image("goose_geklickt.gif")

snowman = load_image("snowman.gif")
snowman_dark = load_image("snowman_geklickt.gif")

#Buttons erstellen

button1 = tk.Button(button_frame, image=cat, borderwidth=10,
                    command=lambda: player_press(1, button1, cat_dark, cat))

button2 = tk.Button(button_frame, image=cat2, borderwidth=10,
                    command=lambda: player_press(2, button2, cat2_dark, cat2))

button3 = tk.Button(button_frame, image=goose, borderwidth=10,
                    command=lambda: player_press(3, button3, goose_dark, goose))

button4 = tk.Button(button_frame, image=snowman, borderwidth=10,
                    command=lambda: player_press(4, button4, snowman_dark, snowman))


# Buttons in einem 2×2 Raster anordnen
button1.grid(row=0, column=0, padx=20, pady=20)
button2.grid(row=0, column=1, padx=20, pady=20)
button3.grid(row=1, column=0, padx=20, pady=20)
button4.grid(row=1, column=1, padx=20, pady=20)

#Buttons abdunkeln Funktion
def flash_button(button, img_dark, img_normal):
    button.config(image=img_dark)
    window.after(200, lambda: button.config(image=img_normal))

#Spielvariablen
sequence = []       # Zug Computer
player_input = []   # Zug Spieler
round_active = False


# Spiel-Logik
def computer_turn():
    global round_active, sequence, player_input

    player_input = []          # Spieler-Eingaben zurücksetzen
    round_active = False       # Spieler darf während Sequenz nicht klicken

    # neuen zufälligen Button hinzufügen
    new_step = random.choice([1, 2, 3, 4])
    sequence.append(new_step)

    # Sequenz visuell abspielen
    play_sequence(0)

def play_sequence(index):
    if index >= len(sequence):
        # danach darf der Spieler klicken
        global round_active
        round_active = True
        return

    step = sequence[index]

    # Zuordnung Button zu Nummern
    button_map = {
        1: (button1, cat_dark, cat),
        2: (button2, cat2_dark, cat2),
        3: (button3, goose_dark, goose),
        4: (button4, snowman_dark, snowman)
    }

    btn, dark_img, normal_img = button_map[step]

    # Button kurz blinken lassen
    flash_button(btn, dark_img, normal_img)

    # Nächsten Schritt nach 700 ms abspielen
    window.after(700, lambda: play_sequence(index + 1))

def player_press(num, button, img_dark, img_normal):
    global round_active, player_input, sequence

    if not round_active:
        return  # Spieler darf nicht klicken bevor Computer fertig ist
    
    # Button blinken lassen
    flash_button(button, img_dark, img_normal)

    # Spieler Eingabe speichern
    player_input.append(num)

    # Prüfen ob korrekt
    if player_input[-1] != sequence[len(player_input)-1]:
        game_over()
        return

    # Checken ob Runde richtig wiederholt
    if len(player_input) == len(sequence):
        window.after(800, computer_turn)

def game_over():
    global sequence, player_input, round_active
    round_active = False
    anzeige.config(text="❌ Game Over! Restarting...")

    # kurze Pause, dann Neustart
    window.after(2000, start_new_game)

def start_new_game():
    global sequence
    sequence = []
    anzeige.config(text="Watch first, repeat afterwards.")
    window.after(1000, computer_turn)


# Spiel starten
start_new_game()

# Fenster anzeigen
window.mainloop()