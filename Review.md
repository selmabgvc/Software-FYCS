Review von Selma und Yvonne
 
1. Korrektheit

Der Code funktioniert so wie wir es uns erwartet haben.
 
2. Lesbarkeit

mehr Abstand bei den Kommentaren, würde zu einer besseren Lesbarkeit führen
Einheitliche Kommentierung mit # oder """
--> **Antwort:** Da stimmen wir euch zu; eine einheitliche Kommentierung würde den Lesefluss definitiv verbessern. Wir haben es so gehandhabt, weil die Kommentare teilweise mehrere Zeilen lang waren bzw. Auflistungen zur Erklärung beinhaltet haben und beim # Fließtexte daraus entstehen würden. Wir haben die Kommentare noch einmal überarbeitet und hoffen, dass es jetzt besser ist.
 
3. Code Strukturierung

Klarere Unterscheidung zwischen front und backend
--> **Antwort:** Wir verstehen den Punkt. Bei unserem Spiel ist UI und Logik stark gekoppelt (Callbacks, after(), Button-Objekte). Eine strikte Trennung würde den Code deutlich umfangreicher machen und die Lesbarkeit für unsere Zielgruppe (Anfänger/kleines Projekt) unseres Erachtens verschlechtern. Wir achten stattdessen auf funktionale Trennung (UI vs. Spiellogik-Funktionen) und klare Benennung - weshalb wir auch viele Kommentare eingebaut haben, damit klar ist, was die einzelnen Code-Abschnitte ausführen.

Code für Buttoms eventuell vereinfachen, indem man die Buttoms in eine Liste packt und daraus eine Schleife macht
--> **Antwort:** Guter Punkt. Wir haben es zuerst explizit geschrieben, damit Anfänger sofort sehen, welcher Button was macht und welche Komponenten dazugehören. Wir können das aber sauber in einer Schleife lösen, ohne Funktionalität zu verändern. Der Code ist dadurch zwar etwas länger aber für uns persönlich dennoch verständlicher und übersichtlicher.
 
4. Code-Sicherheit

Der Code ist aus unserer Sicht sicher
 
5. Standards

Standards sind an sich da, aber "windows" "buttoms" etc wird statt "__name__ == "__main__"" genutzt
Python Sprache scheint richtig eingesetzt zu werden
--> **Antwort:** Danke für den Hinweis! Für ein einzelnes Skript, das als Spiel direkt gestartet wird, funktioniert es auch ohne und ist somit nicht zwingend notwendig. Trotzdem wäres es sinnvoll, jedoch aus zeitlichen Gründen leider nicht mehr umsetzbar.
 
6. Test

Start Game → Spiel erscheint
Computer zeigt Sequenz → Spieler kann anschließend klicken
Falscher Klick → Herz wird abgezogen, Sequenz wiederholt sich
Nach 3 Runden → Buttons werden gemischt
Game Over → Overlay erscheint, Highscore wird gespeichert
Quit → Musik stoppt, Bye-Text erscheint
Fenster schließen (X) → pygame stoppt, App beendet sauber
 
7. Skalierbarkeit

Der Code reicht vollkommen aus für ein Spiel bzw kleines Projekt, jedoch könnte es für größeres unübersichtlich werden
 
8. Bonuspunkte

Die Musik ist sehr cool
Weihnachtliches Thema
Bilder für die Buttons statt Farben - sehr süß
Verschiedene Levels
Das man mehrere Leben hat

