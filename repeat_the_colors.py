import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import os

# Versuch, pygame für Musik und Sounds zu verwenden
try:
    import pygame
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

# Hilfsfunktion: alle Dateien liegen im gleichen Ordner wie das Skript
def asset_path(name):
    return name

# Fenster erstellen
window = tk.Tk()
window.title("Repeat the Clicks!")
window.geometry("1000x800")

# Animierten Schneehintergrund (snow.gif) laden
snow_frames = []
try:
    snow_gif = Image.open(asset_path("snow.gif"))
    # Nur jede 2. Frame verwenden, um Last zu reduzieren
    for idx, frame in enumerate(ImageSequence.Iterator(snow_gif)):
        if idx % 2 != 0:
            continue
        frame = frame.resize((1000, 800), Image.LANCZOS)
        snow_frames.append(ImageTk.PhotoImage(frame))
except Exception as e:
    print("Konnte snow.gif nicht laden:", e)
    snow_frames = []

# Label für den Hintergrund über das gesamte Fenster
bg_label = tk.Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()  # Hintergrund nach ganz hinten legen, damit andere Widgets sichtbar sind

# Funktion, um den Schneehintergrund zu animieren
def animate_snow(i=0):
    if snow_frames:
        frame = snow_frames[i % len(snow_frames)]
        bg_label.config(image=frame)
        # Animationsgeschwindigkeit (ms) – größer = weniger CPU-Last
        window.after(200, lambda: animate_snow(i + 1))

# Schneefall starten
animate_snow()

# Schwierigkeitslevel (Easy / Normal / Hard)
difficulty_var = tk.StringVar(value="Normal")

# Einstellungen je Schwierigkeit:
# flash_time  = Dauer, wie lange Button dunkel ist (in ms)
# step_delay  = Pause zwischen einzelnen Schritten der Sequenz (in ms)
difficulty_settings = {
    "Easy":   {"flash_time": 300, "step_delay": 850},
    "Normal": {"flash_time": 220, "step_delay": 600},
    "Hard":   {"flash_time": 130, "step_delay": 420},
}

def get_settings():
    # Aktuelle Einstellungen für den gewählten Schwierigkeitsgrad zurückgeben.
    return difficulty_settings.get(difficulty_var.get(), difficulty_settings["Normal"])

# Welcome Screen / Intro
content_frame = tk.Frame(window, bg="", highlightthickness=0)
content_frame.pack(expand=True)

anzeige = tk.Label(
    content_frame,
    text="🎄 Welcome to Ziska's & Claudia's Game! 🎄\n"
         "Please choose a difficulty level and have fun ✨",
    font=("Helvetica", 24, "bold"),
    fg="#0D3B66",
    justify="center",
    anchor="center",
    wraplength=800
)
anzeige.pack(pady=20)

# Highscore-Datei im Home-Ordner
HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), ".repeat_the_clicks_highscore.txt")

def load_highscore():
    # Highscore aus Datei laden (oder 0, wenn keine Datei existiert).
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            text = f.read().strip()
            return int(text) if text else 0
    except ValueError:
        return 0

def save_highscore(score):
    # Highscore in Datei speichern.
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Highscore laden
highscore = load_highscore()

# Intro-Frame (Difficulty + Christmas + Start)
# >>> Änderung: parent = content_frame statt window
intro_frame = tk.Frame(content_frame)
intro_frame.pack(pady=10)

# Christmas Mode (Hintergrundmusik an/aus)
christmas_mode = tk.BooleanVar(value=True)

# Wird später gesetzt, wenn Musik wirklich vorhanden ist
music_available = False
game_started = False  # damit Musik erst nach Start läuft

def on_christmas_toggle():
    """
    Wird aufgerufen, wenn die Christmas-Checkbox geändert wird.
    Musik nur steuern, wenn:
    - pygame verfügbar
    - Musikdatei existiert
    - das Spiel bereits gestartet wurde
    """
    if not (SOUND_ENABLED and music_available and game_started):
        return
    if christmas_mode.get():
        try:
            pygame.mixer.music.play(-1)  # Musik in Endlosschleife
        except:
            pass
    else:
        pygame.mixer.music.stop()

christmas_checkbox = tk.Checkbutton(
    intro_frame,
    text="🎅 Christmas Music",
    variable=christmas_mode,
    command=on_christmas_toggle
)
christmas_checkbox.grid(row=0, column=0, columnspan=2, pady=5)

# Radiobuttons für die Schwierigkeitsgrade (im Intro wählen)
tk.Label(intro_frame, text="Difficulty:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

diff_buttons_frame = tk.Frame(intro_frame)
diff_buttons_frame.grid(row=1, column=1, pady=5, sticky="w")

for name in ["Easy", "Normal", "Hard"]:
    tk.Radiobutton(
        diff_buttons_frame,
        text=name,
        variable=difficulty_var,
        value=name
    ).pack(side=tk.LEFT, padx=5)

# Start-Button im Intro-Bereich
def start_button_click():
    # Startet das erste Spiel, blendet das Intro aus und zeigt das Spielfeld.
    global game_started

    game_started = True
    start_button.config(state="disabled")
    intro_frame.pack_forget()      # Intro-Bereich ausblenden
    show_game_ui()                 # Spielbereich einblenden

    # Musik nur jetzt starten, falls verfügbar und Christmas Music aktiv
    if SOUND_ENABLED and music_available and christmas_mode.get():
        try:
            pygame.mixer.music.play(-1)
        except:
            pass

    start_new_game()

start_button = tk.Button(
    intro_frame,
    text="Start Game",
    font=("Arial", 18, "bold"),
    command=start_button_click
)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# Spiel-Frame (wird erst nach Start angezeigt)
game_frame = tk.Frame(window)

# Labels für Highscore, aktuellen Score, Runde und Leben
highscore_label = tk.Label(game_frame, text=f"Highscore: {highscore}", font=("Arial", 18))
score_label = tk.Label(game_frame, text="Score: 0", font=("Arial", 18))
round_label = tk.Label(game_frame, text="Round: 1", font=("Arial", 18))
lives_label = tk.Label(game_frame, text="", font=("Arial", 18), fg="#D62828")

# Frame, in dem die 4 Buttons liegen (Spielfläche)
button_frame = tk.Frame(game_frame)

def show_game_ui():
    # Blendet den Spielbereich (Labels + Buttons) ein.
    game_frame.pack(pady=20)
    highscore_label.pack()
    score_label.pack()
    round_label.pack()
    lives_label.pack(pady=5)
    button_frame.pack(pady=40)

# Bild-Lade-Funktion
def load_image(path, size=(150, 150)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Tierbilder laden
cat = load_image(asset_path("cat.gif"))
cat_dark = load_image(asset_path("cat_geklickt.gif"))

cat2 = load_image(asset_path("cat2.gif"))
cat2_dark = load_image(asset_path("cat2_geklickt.gif"))

goose = load_image(asset_path("goose.gif"))
goose_dark = load_image(asset_path("goose_geklickt.gif"))

snowman = load_image(asset_path("snowman.gif"))
snowman_dark = load_image(asset_path("snowman_geklickt.gif"))

# Sounds (click-sound, game-over, ggf. Musik)
click_sound = None
game_over_sound = None

if SOUND_ENABLED:
    try:
        pygame.mixer.init()

        # Hintergrundmusik (optional) – "background_music.mp3"
        music_path = asset_path("background_music.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            music_available = True

        # Klick- und Game-Over-Sounds
        click_sound = pygame.mixer.Sound(asset_path("click-sound.mp3"))
        game_over_sound = pygame.mixer.Sound(asset_path("game-over.mp3"))

    except Exception as e:
        print("Sound problem:", e)
        SOUND_ENABLED = False

# Spielvariablen
sequence = []       # Liste der vom Computer erzeugten Schritte (1–4)
player_input = []   # Schritte, die der Spieler eingibt
round_active = False
lives = 3

def update_lives_label():
    # Leben als Herzen aktualisieren.
    global lives
    if lives < 0:
        lives = 0
    lives_label.config(text="Lives: " + "❤️" * lives)

def reset_score_round_labels():
    # Score und Runde zurücksetzen.
    score_label.config(text="Score: 0")
    round_label.config(text="Round: 1")

def flash_button(button, img_dark, img_normal):
    # Button für kurze Zeit abdunkeln (ohne Größenänderung, damit sich nichts verschiebt).
    settings = get_settings()
    flash_time = settings["flash_time"]

    button.config(image=img_dark)
    window.after(
        flash_time,
        lambda: button.config(image=img_normal)
    )

def lose_life(reason):
    # Ein Leben verlieren, ggf. Game Over auslösen, sonst Sequenz wiederholen.
    global lives, round_active, player_input

    lives -= 1    # ein Leben abziehen
    update_lives_label()
    round_active = False
    player_input = []  # Eingaben zurücksetzen

    if lives <= 0:
        game_over()
    else:
        anzeige.config(text=f"{reason} You lost a life!")
        # gleiche Sequenz nach kurzer Pause erneut anzeigen
        window.after(
            1500,
            lambda: (
                anzeige.config(text="Watch first, repeat afterwards."),
                play_sequence(0)
            )
        )

def player_press(num, button, img_dark, img_normal):
    # Wird aufgerufen, wenn der Spieler einen der vier Buttons klickt.
    global round_active, player_input, sequence

    if not round_active:
        return  # Spieler darf noch nicht klicken bevor Computer fertig ist

    # Klick-Sound abspielen
    if SOUND_ENABLED and click_sound is not None:
        try:
            click_sound.play()
        except:
            pass

    # Button blinken lassen
    flash_button(button, img_dark, img_normal)

    # Spieler Eingabe speichern
    player_input.append(num)

    # Prüfen ob korrekt
    if player_input[-1] != sequence[len(player_input)-1]:
        lose_life("Wrong move!")
        return

    # Checken ob Runde richtig wiederholt
    if len(player_input) == len(sequence):
        score_label.config(text=f"Score: {len(sequence)}")
        round_label.config(text=f"Round: {len(sequence) + 1}")

        if len(sequence) % 3 == 0: # Mischen nach jeder 3.Runde
            shuffle_buttons()

        round_active = False
        window.after(800, computer_turn)

def computer_turn():
    # Zug des Computers: neuen Schritt hinzufügen und Sequenz abspielen.
    global round_active, sequence, player_input

    player_input = []          # Spieler-Eingaben zurücksetzen
    round_active = False       # Spieler darf während Sequenz nicht klicken

    # neuen zufälligen Button hinzufügen
    new_step = random.choice([1, 2, 3, 4])
    sequence.append(new_step)

    # Sequenz visuell abspielen
    play_sequence(0)

def play_sequence(index):
    # Die Sequenz Schritt für Schritt anzeigen.
    global round_active

    if index >= len(sequence):
        # danach darf der Spieler klicken
        round_active = True
        anzeige.config(text="Now repeat!")
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

    # Nächsten Schritt nach Delay abspielen
    settings = get_settings()
    window.after(settings["step_delay"], lambda: play_sequence(index + 1))

def shuffle_buttons():
    # Die vier Buttons zufällig im 2x2 Raster anordnen.
    buttons = [button1, button2, button3, button4]
    positions = [(0,0), (0,1), (1,0), (1,1)]
    random.shuffle(positions)
    for btn, (r,c) in zip(buttons, positions):
        btn.grid(row=r, column=c, padx=20, pady=20)

def show_game_over_overlay():
    # Game-Over-Overlay einblenden (jetzt im gleichen Bereich wie der Welcome-Text).
    game_over_frame.pack(expand=True)
    game_over_frame.lift()  # nach vorne holen

def hide_game_over_overlay():
    # Game-Over-Overlay ausblenden.
    game_over_frame.pack_forget()

def on_play_again():
    # User klickt auf 'Play again' im Game-Over-Screen.
    hide_game_over_overlay()
    start_new_game()

def on_quit_game():
    # User klickt auf 'No' im Game-Over-Screen.
    hide_game_over_overlay()
    # Spielfläche & Intro komplett ausblenden
    game_frame.pack_forget()
    intro_frame.pack_forget()
    # Musik stoppen
    if SOUND_ENABLED:
        try:
            pygame.mixer.music.stop()
        except:
            pass
    # Statuslabel neu zentriert mit Bye-Text anzeigen
    anzeige.pack_forget()
    anzeige.config(text="Okay, bye 👋")
    anzeige.pack(expand=True)

def game_over():
    # Game Over: Score berechnen, Highscore prüfen, Game-Over-Sound und Overlay.
    global sequence, player_input, round_active, highscore, lives

    round_active = False
    score = max(0, len(sequence) - 1)

    # Game-Over-Sound abspielen
    if SOUND_ENABLED and game_over_sound is not None:
        try:
            game_over_sound.play()
        except:
            pass

    # Highscore prüfen
    if score > highscore:
        highscore = score
        save_highscore(highscore)
        highscore_label.config(text=f"Highscore: {highscore}")
        anzeige.config(text="🏆 NEW HIGHSCORE! 🏆")
    else:
        anzeige.config(text=f"Game Over! Your score: {score}")

    # Game-Over-Overlay nach kurzer Pause einblenden
    window.after(1500, show_game_over_overlay)

def start_new_game():
    # Kompletter Neustart: Sequenz leeren, Leben & Anzeigen zurücksetzen, neue Runde starten.
    global sequence, lives

    sequence = []
    lives = 3
    update_lives_label()
    reset_score_round_labels()
    anzeige.config(text="Watch first, repeat afterwards.")

    # erste Runde vom Computer nach kleiner Pause starten
    window.after(1000, computer_turn)

# Buttons mit Bildern und zugehörigen Commands
button1 = tk.Button(
    button_frame,
    image=cat,
    borderwidth=10,
    command=lambda: player_press(1, button1, cat_dark, cat)
)
button2 = tk.Button(
    button_frame,
    image=cat2,
    borderwidth=10,
    command=lambda: player_press(2, button2, cat2_dark, cat2)
)
button3 = tk.Button(
    button_frame,
    image=goose,
    borderwidth=10,
    command=lambda: player_press(3, button3, goose_dark, goose)
)
button4 = tk.Button(
    button_frame,
    image=snowman,
    borderwidth=10,
    command=lambda: player_press(4, button4, snowman_dark, snowman)
)

# Buttons im Raster platzieren (Frame wird erst bei show_game_ui() gepackt)
button1.grid(row=0, column=0, padx=20, pady=20)
button2.grid(row=0, column=1, padx=20, pady=20)
button3.grid(row=1, column=0, padx=20, pady=20)
button4.grid(row=1, column=1, padx=20, pady=20)

# Game-Over-Overlay-Frame
# >>> Änderung: parent = content_frame statt window
game_over_frame = tk.Frame(content_frame, bg="#FFFFFF", bd=2, relief="ridge")

go_label = tk.Label(
    game_over_frame,
    text="GAME OVER",
    font=("Helvetica", 36, "bold"),
    fg="#D62828",
    bg="#FFFFFF"
)
go_label.pack(pady=20)

go_question = tk.Label(
    game_over_frame,
    text="Play again?",
    font=("Arial", 20),
    bg="#FFFFFF"
)
go_question.pack(pady=10)

go_button_frame = tk.Frame(game_over_frame, bg="#FFFFFF")
go_button_frame.pack(pady=10)

go_yes = tk.Button(
    go_button_frame,
    text="Yes",
    font=("Arial", 16),
    width=10,
    command=on_play_again
)
go_yes.pack(side=tk.LEFT, padx=10)

go_no = tk.Button(
    go_button_frame,
    text="No",
    font=("Arial", 16),
    width=10,
    command=on_quit_game
)
go_no.pack(side=tk.LEFT, padx=10)

# Zu Beginn Overlay versteckt lassen
hide_game_over_overlay()

def on_close():
    # Beim Schließen Musik stoppen, pygame beenden und Fenster zerstören.
    if SOUND_ENABLED:
        try:
            pygame.mixer.music.stop()
            pygame.quit()
        except:
            pass
    window.destroy()

# Verhalten beim Schließen überschreiben (rotes X)
window.protocol("WM_DELETE_WINDOW", on_close)

# Leben beim Start initial setzen
update_lives_label()

# Tkinter-Eventloop starten
window.mainloop()
