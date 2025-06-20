# coin.py
import pygame
import os
import random

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        path = os.path.join("sprites", "coin.png")
        if os.path.exists(path):
            self.image = pygame.image.load(path).convert_alpha()
        else:
            # Fallback: gelber Kreis
            surf = pygame.Surface((30,30), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255,215,0), (15,15), 15)
            self.image = surf
        self.rect = self.image.get_rect(midbottom=(x,y))
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
