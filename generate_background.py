import pygame
import os

# Initialisiere Pygame
pygame.init()

# Erstelle ein leeres Bild
width, height = 800, 600
screen = pygame.Surface((width, height))
screen.fill((0, 0, 128))  # Fülle das Bild mit einer Farbe (z.B. Dunkelblau)

# Zeichne etwas Text auf das Bild
font = pygame.font.SysFont('Arial', 48)
text = font.render('Welcome to My Game!', True, (255, 255, 255))
text_rect = text.get_rect(center=(width // 2, height // 2))
screen.blit(text, text_rect)

# Stelle sicher, dass der Ordner "backgrounds" existiert
os.makedirs('backgrounds', exist_ok=True)

# Speichere das Bild
pygame.image.save(screen, 'backgrounds/start_screen.png')

print("Das Bild wurde erfolgreich erstellt und gespeichert.")