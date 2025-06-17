import pygame
import sys
from start_screen import StartScreen

def main():
    pygame.init()
    pygame.mixer.init()

    # Endlosschleife: wir kehren nach Game-Over hierher zurück
    while True:
        start = StartScreen()
        game  = start.run()
        game.run()
        # wenn game.run() endet (Game-Over und kein „Restart“ per R),
        # landen wir hier und starten von vorn

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()