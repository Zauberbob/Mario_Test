import pygame
import sys
from game import StartScreen

def main():
    pygame.init()
    start_screen = StartScreen()
    game = start_screen.run()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
