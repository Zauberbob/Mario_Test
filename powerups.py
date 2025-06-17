import pygame
import os
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, typ):
        super().__init__()
        # Bilddatei je Typ
        mapping = {
            "fly": "fly.png",
            "shield": "shield.png",
            "life": "life.png"
        }
        fn = mapping.get(typ)
        path = os.path.join("sprites", fn) if fn else None
        if fn and os.path.exists(path):
            self.image = pygame.image.load(path).convert_alpha()
        else:
            # Fallback: einfacher Kreis
            r = 20
            surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            if typ == "fly":
                color = (0, 200, 255)
            elif typ == "shield":
                color = (255, 255, 0)
            else:  # life
                color = (255, 0, 255)
            pygame.draw.circle(surf, color, (r, r), r)
            self.image = surf

        self.rect = self.image.get_rect(midbottom=(x, y))
        self.typ = typ
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()