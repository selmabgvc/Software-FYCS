**Korrektheit & Funktionalität**
- Grundfunktionen sind korrekt umgesetzt und funktionieren einwandfrei.

**Fehlerbehandlung & Robustheit**
- Fehleranfällig wenn Eingabe der Ausgabe/Expense ein Komma enthält (Denn dann könnte es falsch "spliten" & nicht richtig ins Excel übertragen) (Zeile 159 & 184)

   = Antwort: Kann der individuelle User selber in Excel konfigurieren.

**Lesbarkeit & Wartbarkeit**
- Im Kommentar "Excel-File", ist aber eigentlich eine CSV (Zeile 76)
- Kategorien + Farbzuordnung ggf. als Mapping/Dictionary definieren statt if/elif-Kette, damit es übersichtlicher, skalierbar & wartbarer ist (Zeile 124ff) 
- Entweder ANSI oder Colorama fürs färben von Text (Zeilen 29ff -> ANSI; Zeile 6 & 8 zum initialisieren & reset vom Terminal)

    = Antwort: - Kommentar geändert
               - If/ Elif Kette aus Zeitgründen und Komplexität nicht umgesetzt
               - Colorama muss nicht mehr installiert werden 

**Effizienz & Darstellung**
- Progress-Bar -> zeigt bei Überbudget trotzdem nur 100% an; nicht visualisiert wie stark drüber (Zeile 55ff)

    = Antwort: Durch die Farbenskala wird das Überschreiten des Budgets bereits angedeutet. Eine visuelle Darstellung der Progress - Bar die über den 100% geht würde komisch ausschauen. 

**Sicherheit**
- Keine sicherheitskritischen Probleme; der Code arbeitet nur lokal mit Dateien.

**Dokumentation**
- Im README sollte ergänzt werden, welche externen Module (z. B. colorama) installiert werden müssen. 

    = Antwort: hat sich erledigt
