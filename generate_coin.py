# generate_coin.py
import pygame
import os

# Initialisiere Pygame (nur für Surface‑Erzeugung)
pygame.init()

# Größe der Münze
size = 30
surf = pygame.Surface((size, size), pygame.SRCALPHA)

# Außenkreis (Goldgelb) und dunkler Rand
outer_color = (255, 215, 0)   # RGB Gold
border_color = (200, 170, 0)  # dunklerer Rand
center = (size // 2, size // 2)
radius = size // 2 - 2

# Zeichne Rand
pygame.draw.circle(surf, border_color, center, radius + 2)
# Zeichne Münzenfläche
pygame.draw.circle(surf, outer_color, center, radius)

# Optional: kleiner Glanz‑Kreis
pygame.draw.circle(surf, (255, 255, 255, 100),
                   (center[0] - 5, center[1] - 5), radius // 3)

# Stelle sicher, dass der Ordner sprites/ existiert
os.makedirs("sprites", exist_ok=True)
# Speichere die PNG
pygame.image.save(surf, os.path.join("sprites", "coin.png"))

print("Münz‑Icon erzeugt als sprites/coin.png")
