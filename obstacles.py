import pygame
import os
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((180, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, typ=1, is_boss=False):
        super().__init__()
        # Lade Dein Sprite oder Fallback‑Block
        fn = f"enemy{typ}.png"
        path = os.path.join("sprites", fn)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
        else:
            # Platzhalter-Farbblock
            img = pygame.Surface((50, 50), pygame.SRCALPHA)
            cmap = {1:(0,150,0), 2:(150,0,150), 3:(0,150,150)}
            img.fill(cmap.get(typ, (0,255,0)))

        # Boss: doppelte Größe + Umrandung + Label
        if is_boss:
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w*2, h*2))
            pygame.draw.rect(img, (255,0,0), img.get_rect(), 4)
            font = pygame.font.SysFont(None, 24)
            label = font.render("BOSS", True, (255,0,0))
            img.blit(label, (5,5))

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        # y kann übergeben oder fixiert werden
        self.rect.bottom = y if y else 550

        # Basis‐Speed und Trefferpunkte
        self.speed      = random.choice([3,5,7])
        self.is_boss    = is_boss
        self.hit_points = 2 if is_boss else 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
