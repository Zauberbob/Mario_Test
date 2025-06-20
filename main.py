# main.py
import pygame
import sys
import os

# Debug: aktuelles Arbeitsverzeichnis anzeigen
print(">>> Starte Spiel aus:", os.getcwd())
# Debug: sprites‑Ordner Inahlt auflisten, falls vorhanden
sprites_dir = os.path.join(os.getcwd(), "sprites")
if os.path.exists(sprites_dir):
    print(">>> Sprites‑Ordner gefunden. Inhalt:", os.listdir(sprites_dir))
else:
    print(">>> Sprites‑Ordner NICHT gefunden unter", sprites_dir)

from start_screen import StartScreen

def main():
    # Pygame initialisieren
    pygame.init()
    pygame.mixer.init()

    # Endlosschleife: Start‑Screen → Game → Restart/Quit
    while True:
        start = StartScreen()
        game  = start.run()
        action = game.run()

        if action == 'QUIT':
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
